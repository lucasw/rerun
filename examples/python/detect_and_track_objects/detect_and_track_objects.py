#!/usr/bin/env python3
"""Example applying simple object detection and tracking on a video."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Final, Sequence

import cv2
import numpy as np
import numpy.typing as npt
import requests
import rerun as rr  # pip install rerun-sdk
import torch
import torchvision
from PIL import Image

DESCRIPTION = """
# Detect and track objects

This is a more elaborate example applying simple object detection and segmentation on a video using the Huggingface
`transformers` library. Tracking across frames is performed using [CSRT](https://arxiv.org/abs/1611.08461) from
OpenCV. The results are visualized using Rerun.

The full source code for this example is available
[on GitHub](https://github.com/rerun-io/rerun/blob/latest/examples/python/detect_and_track_objects).
""".strip()

EXAMPLE_DIR: Final = Path(os.path.dirname(__file__))
DATASET_DIR: Final = EXAMPLE_DIR / "dataset" / "tracking_sequences"
DATASET_URL_BASE: Final = "https://storage.googleapis.com/rerun-example-datasets/tracking_sequences"
CACHE_DIR: Final = EXAMPLE_DIR / "cache"

# panoptic_coco_categories.json comes from:
# https://github.com/cocodataset/panopticapi/blob/7bb4655548f98f3fedc07bf37e9040a992b054b0/panoptic_coco_categories.json
# License: https://github.com/cocodataset/panopticapi/blob/7bb4655548f98f3fedc07bf37e9040a992b054b0/license.txt
COCO_CATEGORIES_PATH = EXAMPLE_DIR / "panoptic_coco_categories.json"

DOWNSCALE_FACTOR = 2
DETECTION_SCORE_THRESHOLD = 0.8

os.environ["TRANSFORMERS_CACHE"] = str(CACHE_DIR.absolute())
from transformers import (  # noqa: E402 module level import not at top of file
    DetrFeatureExtractor,
    DetrForSegmentation,
    SamModel,
    SamProcessor,
)


@dataclass
class Detection:
    """Information about a detected object."""

    class_id: int
    bbox_xywh: list[float]
    image_width: int
    image_height: int

    def scaled_to_fit_image(self, target_image: npt.NDArray[Any]) -> Detection:
        """Rescales detection to fit to target image."""
        target_height, target_width = target_image.shape[:2]
        return self.scaled_to_fit_size(target_width=target_width, target_height=target_height)

    def scaled_to_fit_size(self, target_width: int, target_height: int) -> Detection:
        """Rescales detection to fit to target image with given size."""
        if target_height == self.image_height and target_width == self.image_width:
            return self
        width_scale = target_width / self.image_width
        height_scale = target_height / self.image_height
        target_bbox = [
            self.bbox_xywh[0] * width_scale,
            self.bbox_xywh[1] * height_scale,
            self.bbox_xywh[2] * width_scale,
            self.bbox_xywh[3] * height_scale,
        ]
        return Detection(self.class_id, target_bbox, target_width, target_height)

class Segmentor:
    def __init__(self, device):
        self.device = device
        self.model = SamModel.from_pretrained("facebook/sam-vit-base")
        self.model.to(self.device)
        self.processor = SamProcessor.from_pretrained("facebook/sam-vit-base")

    def segment(self, rgb: cv2.typing.MatLike, frame_idx: int):
        logging.debug("processor")
        # TODO(lucasw) what is this?
        # input_points = [[[450, 600]]] # 2D localization of a window
        logging.debug(f"rgb shape {rgb.shape} {rgb.dtype}")
        inputs = self.processor(rgb,  # input_points=input_points,
                                return_tensors="pt").to(self.device)
        _, _, scaled_height, scaled_width = inputs["pixel_values"].shape
        logging.debug(f"model {scaled_height} {scaled_width}")
        scaled_size = (scaled_width, scaled_height)
        rgb_scaled = cv2.resize(rgb, scaled_size)
        outputs = self.model(**inputs)

        scores = outputs.iou_scores
        logging.debug(scores)

        logging.debug("post-process")
        masks = self.processor.image_processor.post_process_masks(outputs.pred_masks.cpu(),
                                                                  inputs["original_sizes"].cpu(),
                                                                  inputs["reshaped_input_sizes"].cpu())

        logging.debug(len(masks))
        # TODO(lucasw) this isn't working, maybe clues here to how to get it working:
        # https://github.com/huggingface/transformers/blob/main/src/transformers/models/sam/modeling_sam.py
        # or try https://huggingface.co/facebook/sam-vit-base#automatic-mask-generation
        for ind, mask_raw in enumerate(masks):
            # TODO(lucasw) I think these are 0.0-1.0 scores, not sure how to interpret
            mask = (mask_raw.detach().permute(0, 2, 3, 1) * 255).cpu().numpy().astype(np.uint8)[0]
            logging.info(f"max value in mask {np.max(mask)}")
            logging.info(f"{ind} {mask.shape}")
            rr.log(f"segmentation{ind}", rr.Image(mask).compress(jpeg_quality=85))
            # rr.log(f"segmentation{ind}", rr.SegmentationImage(mask))
            # rr.log(f"segmentation{ind}/rgb_scaled", rr.Image(rgb_scaled).compress(jpeg_quality=85))


class Detector:
    """Detects objects to track."""

    def __init__(self, coco_categories: list[dict[str, Any]], device) -> None:
        self.device = device
        logging.info("Initializing neural net for detection and segmentation.")
        self.feature_extractor = DetrFeatureExtractor.from_pretrained("facebook/detr-resnet-50-panoptic")
        self.model = DetrForSegmentation.from_pretrained("facebook/detr-resnet-50-panoptic")

        logging.info(self.device)
        self.model.to(self.device)
        logging.info(type(self.feature_extractor))
        logging.info(dir(self.feature_extractor))
        # self.feature_extractor.to(device)

        self.is_thing_from_id: dict[int, bool] = {cat["id"]: bool(cat["isthing"]) for cat in coco_categories}

    def detect_objects_to_track(self, rgb: cv2.typing.MatLike, frame_idx: int) -> list[Detection]:
        logging.info("Looking for things to track on frame %d", frame_idx)

        logging.debug("Preprocess image for detection network")
        pil_im_small = torchvision.transforms.functional.pil_to_tensor(Image.fromarray(rgb)).to(self.device)
        logging.debug(f"run feature extractor {type(pil_im_small)}")
        inputs = self.feature_extractor(images=pil_im_small, return_tensors="pt")
        logging.debug("done feature extractor")
        _, _, scaled_height, scaled_width = inputs["pixel_values"].shape

        logging.debug(f"Pass image {type(inputs)} to detection network")
        outputs = self.model(**inputs.to(self.device))

        logging.debug("Extracting detections and segmentations from network output")
        processed_sizes = [(scaled_height, scaled_width)]
        segmentation_mask = self.feature_extractor.post_process_semantic_segmentation(outputs, processed_sizes)[0]

        logging.debug("post process object detection")
        detections = self.feature_extractor.post_process_object_detection(
            outputs, threshold=0.8, target_sizes=processed_sizes
        )[0]

        logging.debug("get mask on cpu")
        mask = segmentation_mask.detach().cpu().numpy().astype(np.uint8)

        logging.debug("get boxes/ids/things for logging")
        boxes = detections["boxes"].detach().cpu().numpy()
        class_ids = detections["labels"].detach().cpu().numpy()
        things = [self.is_thing_from_id[id] for id in class_ids]

        logging.debug("make image for viz")
        scaled_size = (scaled_width, scaled_height)
        rgb_scaled = cv2.resize(rgb, scaled_size)

        logging.debug("rr logging")
        rr.log("segmentation/rgb_scaled", rr.Image(rgb_scaled).compress(jpeg_quality=85))
        rr.log("segmentation", rr.SegmentationImage(mask))
        self.log_detections(boxes, class_ids, things)
        logging.debug("rr logging done")

        objects_to_track: list[Detection] = []
        if False:
            for idx, (class_id, is_thing) in enumerate(zip(class_ids, things)):
                if is_thing:
                    x_min, y_min, x_max, y_max = boxes[idx, :]
                    bbox_xywh = [x_min, y_min, x_max - x_min, y_max - y_min]
                    objects_to_track.append(
                        Detection(
                            class_id=class_id,
                            bbox_xywh=bbox_xywh,
                            image_width=scaled_width,
                            image_height=scaled_height,
                        )
                    )

        return objects_to_track

    def log_detections(self, boxes: npt.NDArray[np.float32], class_ids: list[int], things: list[bool]) -> None:
        things_np = np.array(things)
        class_ids_np = np.array(class_ids, dtype=np.uint16)

        thing_boxes = boxes[things_np, :]
        thing_class_ids = class_ids_np[things_np]
        rr.log(
            "segmentation/detections/things",
            rr.Boxes2D(
                array=thing_boxes,
                array_format=rr.Box2DFormat.XYXY,
                class_ids=thing_class_ids,
            ),
        )

        background_boxes = boxes[~things_np, :]
        background_class_ids = class_ids[~things_np]
        rr.log(
            "segmentation/detections/background",
            rr.Boxes2D(
                array=background_boxes,
                array_format=rr.Box2DFormat.XYXY,
                class_ids=background_class_ids,
            ),
        )


class Tracker:
    """
    Each instance takes care of tracking a single object.

    The factory class method `create_new_tracker` is used to give unique tracking id's per instance.
    """

    next_tracking_id = 0
    MAX_TIMES_UNDETECTED = 2

    def __init__(self, tracking_id: int, detection: Detection, bgr: cv2.typing.MatLike) -> None:
        self.tracking_id = tracking_id
        self.tracked = detection.scaled_to_fit_image(bgr)
        self.num_recent_undetected_frames = 0

        self.tracker = cv2.legacy.TrackerCSRT_create()  # type: ignore[attr-defined]
        bbox_xywh_rounded = [int(val) for val in self.tracked.bbox_xywh]
        self.tracker.init(bgr, bbox_xywh_rounded)
        self.log_tracked()

    @classmethod
    def create_new_tracker(cls, detection: Detection, bgr: cv2.typing.MatLike) -> Tracker:
        new_tracker = cls(cls.next_tracking_id, detection, bgr)
        cls.next_tracking_id += 1
        return new_tracker

    def update(self, bgr: cv2.typing.MatLike) -> None:
        if not self.is_tracking:
            return
        success, bbox_xywh = self.tracker.update(bgr)

        if success:
            self.tracked.bbox_xywh = clip_bbox_to_image(
                bbox_xywh=bbox_xywh, image_width=self.tracked.image_width, image_height=self.tracked.image_height
            )
        else:
            logger.info("Tracker update failed for tracker with id #%d", self.tracking_id)
            self.tracker = None

        self.log_tracked()

    def log_tracked(self) -> None:
        if self.is_tracking:
            rr.log(
                f"image/tracked/{self.tracking_id}",
                rr.Boxes2D(
                    array=self.tracked.bbox_xywh,
                    array_format=rr.Box2DFormat.XYWH,
                    class_ids=self.tracked.class_id,
                ),
            )
        else:
            rr.log(f"image/tracked/{self.tracking_id}", rr.Clear(recursive=False))  # TODO(#3381)

    def update_with_detection(self, detection: Detection, bgr: cv2.typing.MatLike) -> None:
        self.num_recent_undetected_frames = 0
        self.tracked = detection.scaled_to_fit_image(bgr)
        self.tracker = cv2.TrackerCSRT_create()  # type: ignore[attr-defined]
        bbox_xywh_rounded = [int(val) for val in self.tracked.bbox_xywh]
        self.tracker.init(bgr, bbox_xywh_rounded)
        self.log_tracked()

    def set_not_detected_in_frame(self) -> None:
        self.num_recent_undetected_frames += 1

        if self.num_recent_undetected_frames >= Tracker.MAX_TIMES_UNDETECTED:
            logging.info(
                "Dropping tracker with id #%d after not being detected %d times",
                self.tracking_id,
                self.num_recent_undetected_frames,
            )
            self.tracker = None
            self.log_tracked()

    @property
    def is_tracking(self) -> bool:
        return self.tracker is not None

    def match_score(self, other: Detection) -> float:
        """Returns bbox IoU if classes match, otherwise 0."""
        if self.tracked.class_id != other.class_id:
            return 0.0
        if not self.is_tracking:
            return 0.0

        other = other.scaled_to_fit_size(target_width=self.tracked.image_width, target_height=self.tracked.image_height)
        tracked_bbox = self.tracked.bbox_xywh
        other_bbox = other.bbox_xywh

        return box_iou(tracked_bbox, other_bbox)


def box_iou(first: list[float], second: list[float]) -> float:
    """Calculate Intersection over Union (IoU) between two 2D rectangles in XYWH format."""
    left = max(first[0], second[0])
    right = min(first[0] + first[2], second[0] + second[2])
    top = min(first[1] + first[3], second[1] + second[3])
    bottom = max(first[1], second[1])

    overlap_width = max(0.0, right - left)
    overlap_height = max(0.0, top - bottom)
    intersection_area = overlap_width * overlap_height

    tracked_area = first[2] * first[3]
    other_area = second[2] * second[3]
    union_area = tracked_area + other_area - intersection_area

    return intersection_area / union_area


def clip_bbox_to_image(bbox_xywh: list[float], image_width: int, image_height: int) -> list[float]:
    x_min = max(0, bbox_xywh[0])
    y_min = max(0, bbox_xywh[1])
    x_max = min(image_width - 1, bbox_xywh[0] + bbox_xywh[2])
    y_max = min(image_height - 1, bbox_xywh[1] + bbox_xywh[3])

    return [x_min, y_min, x_max - x_min, y_max - y_min]


def update_trackers_with_detections(
    trackers: list[Tracker],
    detections: Sequence[Detection],
    label_strs: Sequence[str],
    bgr: cv2.typing.MatLike,
) -> list[Tracker]:
    """
    Tries to match detections to existing trackers and updates the trackers if they match.

    Any detections that don't match existing trackers will generate new trackers.
    Returns the new set of trackers.
    """
    non_updated_trackers = list(trackers)  # shallow copy
    updated_trackers: list[Tracker] = []

    logging.debug("Updating %d trackers with %d new detections", len(trackers), len(detections))
    for detection in detections:
        top_match_score = 0.0
        if non_updated_trackers:
            scores = [tracker.match_score(detection) for tracker in non_updated_trackers]
            best_match_idx = np.argmax(scores)
            top_match_score = scores[best_match_idx]
        if top_match_score > 0.0:
            best_tracker = non_updated_trackers.pop(best_match_idx)
            best_tracker.update_with_detection(detection, bgr)
            updated_trackers.append(best_tracker)
        else:
            updated_trackers.append(Tracker.create_new_tracker(detection, bgr))
            logging.info(
                "Tracking newly detected %s with tracking id #%d",
                label_strs[detection.class_id],
                Tracker.next_tracking_id,
            )

    logging.debug("Updating %d trackers without matching detections", len(non_updated_trackers))
    for tracker in non_updated_trackers:
        tracker.set_not_detected_in_frame()
        tracker.update(bgr)
        if tracker.is_tracking:
            updated_trackers.append(tracker)

    logging.info("Tracking %d objects after updating with %d new detections", len(updated_trackers), len(detections))

    return updated_trackers


def track_objects(video_path: str, *, max_frame_count: int | None) -> None:
    with open(COCO_CATEGORIES_PATH, encoding="utf8") as f:
        coco_categories = json.load(f)
    class_descriptions = [
        rr.AnnotationInfo(id=cat["id"], color=cat["color"], label=cat["name"]) for cat in coco_categories
    ]
    rr.log("/", rr.AnnotationContext(class_descriptions), static=True)

    device = "cpu"  # "cuda:0" if torch.cuda.is_available() else "cpu"
    # detector = Detector(coco_categories=coco_categories, device=device)
    segmentor = Segmentor(device=device)

    logging.info("Loading input video: %s", str(video_path))
    # cap = cv2.VideoCapture(video_path)
    frame_idx = 0

    skip = 1  # 40

    # label_strs = [cat["name"] or str(cat["id"]) for cat in coco_categories]
    # trackers: list[Tracker] = []

    # while cap.isOpened():
    for file_path in os.listdir(video_path):
        file_path = os.path.join(video_path, file_path)
        if not os.path.isfile(file_path):
            continue
        image_path = file_path  # os.fsdecode(file_path)
        if max_frame_count is not None and frame_idx >= max_frame_count:
            break

        # ret, bgr = cap.read()
        # if not ret:
        #     logging.info("End of video")
        #     break

        bgr = cv2.imread(image_path, cv2.IMREAD_COLOR)
        if bgr is None:
            continue

        # TODO(lucasw) rr.log the name
        print(image_path)
        rr.set_time_sequence("frame", frame_idx)
        rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
        # TODO(lucasw) re-compresses what was probably already compressed on disk
        rr.log("image", rr.Image(rgb).compress(jpeg_quality=85))

        # if not trackers or frame_idx % 1 == 0:
        if frame_idx % skip == 0:
            t0 = time.time()
            logging.info(f"frame start: {frame_idx} {t0}")
            # detections = detector.detect_objects_to_track(rgb=rgb, frame_idx=frame_idx)
            segments = segmentor.segment(rgb=rgb, frame_idx=frame_idx)
            logging.info(f"frame finished: {frame_idx} {time.time() - t0}s")
            # trackers = update_trackers_with_detections(trackers, detections, label_strs, bgr)

        # else:
        #     if frame_idx % 10 == 0:
        #         logging.debug("Running tracking update step for frame %d", frame_idx)
        #     for tracker in trackers:
        #         tracker.update(bgr)
        #     trackers = [tracker for tracker in trackers if tracker.is_tracking]

        frame_idx += 1


def get_downloaded_path(dataset_dir: Path, video_name: str) -> str:
    video_file_name = f"{video_name}.mp4"
    destination_path = dataset_dir / video_file_name
    if destination_path.exists():
        logging.info("%s already exists. No need to download", destination_path)
        return str(destination_path)

    source_path = f"{DATASET_URL_BASE}/{video_file_name}"

    logging.info("Downloading video from %s to %s", source_path, destination_path)
    os.makedirs(dataset_dir.absolute(), exist_ok=True)
    with requests.get(source_path, stream=True) as req:
        req.raise_for_status()
        with open(destination_path, "wb") as f:
            for chunk in req.iter_content(chunk_size=8192):
                f.write(chunk)
    return str(destination_path)


def setup_logging() -> None:
    # TODO(lucasw) this locks up
    rerun_handler = rr.LoggingHandler("logs")
    rerun_handler.setLevel(-1)
    logger = logging.getLogger()
    logger.addHandler(rerun_handler)


def main() -> None:
    file_handler = logging.FileHandler(filename='tmp.log')
    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    handlers = [file_handler, stdout_handler]

    logging.basicConfig(
        level=logging.DEBUG,
        format='[%(asctime)s] %(filename)s:%(lineno)d %(levelname)s - %(message)s',
        handlers=handlers
    )

    parser = argparse.ArgumentParser(description="Example applying simple object detection and tracking on a video.")
    parser.add_argument(
        "--video",
        type=str,
        default="horses",
        choices=["horses", "driving", "boats"],
        help="The example video to run on.",
    )
    parser.add_argument("--dataset-dir", type=Path, default=DATASET_DIR, help="Directory to save example videos to.")
    parser.add_argument("--video-path", type=str, default="", help="Full path to video to run on. Overrides `--video`.")
    # parser.add_argument("--addr", type=str, default="127.0.0.1:9876", help="ip address:port")
    parser.add_argument(
        "--max-frame",
        type=int,
        help="Stop after processing this many frames. If not specified, will run until interrupted.",
    )
    rr.script_add_args(parser)
    args = parser.parse_args()

    logging.info(args.addr)
    # rr.init("segment")
    # rr.connect(addr=args.addr)
    rr.script_setup(args, "rerun_example_detect_and_track_objects")

    # setup_logging()

    rr.log("description", rr.TextDocument(DESCRIPTION, media_type=rr.MediaType.MARKDOWN), static=True)

    video_path: str = args.video_path
    if not video_path:
        video_path = get_downloaded_path(args.dataset_dir, args.video)

    track_objects(video_path, max_frame_count=args.max_frame)

    rr.script_teardown(args)


if __name__ == "__main__":
    main()
