# DO NOT EDIT!: This file was auto-generated by crates/re_types_builder/src/codegen/python.rs:277.

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Sequence, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa
from attrs import define, field

from .._baseclasses import (
    BaseExtensionArray,
    BaseExtensionType,
)
from ._overrides import color_native_to_pa_array, color_rgba_converter  # noqa: F401

__all__ = ["Color", "ColorArray", "ColorArrayLike", "ColorLike", "ColorType"]


@define
class Color:
    """
    An RGBA color tuple with unmultiplied/separate alpha, in sRGB gamma space with linear alpha.

    Float colors are assumed to be in 0-1 gamma sRGB space.
    All other colors are assumed to be in 0-255 gamma sRGB space.
    If there is an alpha, we assume it is in linear space, and separate (NOT pre-multiplied).
    """

    rgba: int = field(converter=color_rgba_converter)

    def __array__(self, dtype: npt.DTypeLike = None) -> npt.NDArray[Any]:
        return np.asarray(self.rgba, dtype=dtype)

    def __int__(self) -> int:
        return int(self.rgba)


if TYPE_CHECKING:
    ColorLike = Union[Color, int, Sequence[int], npt.NDArray[Union[np.uint8, np.float32, np.float64]]]
else:
    ColorLike = Any

ColorArrayLike = Union[
    Color,
    Sequence[ColorLike],
    int,
    Sequence[Sequence[int]],
    npt.NDArray[Union[np.uint8, np.uint32, np.float32, np.float64]],
]


# --- Arrow support ---


class ColorType(BaseExtensionType):
    def __init__(self) -> None:
        pa.ExtensionType.__init__(self, pa.uint32(), "rerun.datatypes.Color")


class ColorArray(BaseExtensionArray[ColorArrayLike]):
    _EXTENSION_NAME = "rerun.datatypes.Color"
    _EXTENSION_TYPE = ColorType

    @staticmethod
    def _native_to_pa_array(data: ColorArrayLike, data_type: pa.DataType) -> pa.Array:
        return color_native_to_pa_array(data, data_type)


ColorType._ARRAY_TYPE = ColorArray

# TODO(cmc): bring back registration to pyarrow once legacy types are gone
# pa.register_extension_type(ColorType())
