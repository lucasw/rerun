# DO NOT EDIT!: This file was auto-generated by crates/re_types_builder/src/codegen/python.rs:277.

from __future__ import annotations

from typing import Any, Sequence, Union

import numpy as np
import numpy.typing as npt
import pyarrow as pa
from attrs import define, field

from .._baseclasses import (
    BaseExtensionArray,
    BaseExtensionType,
)
from .._converters import (
    to_np_uint8,
)

__all__ = ["TensorId", "TensorIdArray", "TensorIdArrayLike", "TensorIdLike", "TensorIdType"]


@define
class TensorId:
    uuid: npt.NDArray[np.uint8] = field(converter=to_np_uint8)

    def __array__(self, dtype: npt.DTypeLike = None) -> npt.NDArray[Any]:
        return np.asarray(self.uuid, dtype=dtype)


TensorIdLike = TensorId
TensorIdArrayLike = Union[
    TensorId,
    Sequence[TensorIdLike],
]


# --- Arrow support ---


class TensorIdType(BaseExtensionType):
    def __init__(self) -> None:
        pa.ExtensionType.__init__(
            self, pa.list_(pa.field("item", pa.uint8(), nullable=False, metadata={}), 16), "rerun.datatypes.TensorId"
        )


class TensorIdArray(BaseExtensionArray[TensorIdArrayLike]):
    _EXTENSION_NAME = "rerun.datatypes.TensorId"
    _EXTENSION_TYPE = TensorIdType

    @staticmethod
    def _native_to_pa_array(data: TensorIdArrayLike, data_type: pa.DataType) -> pa.Array:
        raise NotImplementedError  # You need to implement "tensorid_native_to_pa_array" in rerun_py/rerun_sdk/rerun/_rerun2/datatypes/_overrides/tensor_id.py


TensorIdType._ARRAY_TYPE = TensorIdArray

# TODO(cmc): bring back registration to pyarrow once legacy types are gone
# pa.register_extension_type(TensorIdType())
