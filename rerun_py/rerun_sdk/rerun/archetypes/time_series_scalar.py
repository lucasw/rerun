# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python.rs
# Based on "crates/re_types/definitions/rerun/archetypes/time_series_scalar.fbs".

# You can extend this class by creating a "TimeSeriesScalarExt" class in "time_series_scalar_ext.py".

from __future__ import annotations

from typing import Any

from attrs import define, field

from .. import components, datatypes
from .._baseclasses import Archetype
from ..error_utils import catch_and_log_exceptions

__all__ = ["TimeSeriesScalar"]


@define(str=False, repr=False, init=False)
class TimeSeriesScalar(Archetype):
    """
    **Archetype**: Log a double-precision scalar that will be visualized as a time-series plot.

    The current simulation time will be used for the time/X-axis, hence scalars
    cannot be timeless!

    Example
    -------
    ### Simple line plot:
    ```python
    import math

    import rerun as rr

    rr.init("rerun_example_scalar", spawn=True)

    for step in range(0, 64):
        rr.set_time_sequence("step", step)
        rr.log("scalar", rr.TimeSeriesScalar(math.sin(step / 10.0)))
    ```
    <center>
    <picture>
      <source media="(max-width: 480px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/480w.png">
      <source media="(max-width: 768px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/768w.png">
      <source media="(max-width: 1024px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/1024w.png">
      <source media="(max-width: 1200px)" srcset="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/1200w.png">
      <img src="https://static.rerun.io/scalar_simple/8bcc92f56268739f8cd24d60d1fe72a655f62a46/full.png" width="640">
    </picture>
    </center>
    """

    def __init__(
        self: Any,
        scalar: components.ScalarLike,
        *,
        radius: components.RadiusLike | None = None,
        color: datatypes.Rgba32Like | None = None,
        label: datatypes.Utf8Like | None = None,
        scattered: components.ScalarScatteringLike | None = None,
    ):
        """
        Create a new instance of the TimeSeriesScalar archetype.

        Parameters
        ----------
        scalar:
             The scalar value to log.
        radius:
             An optional radius for the point.

             Points within a single line do not have to share the same radius, the line
             will have differently sized segments as appropriate.

             If all points within a single entity path (i.e. a line) share the same
             radius, then this radius will be used as the line width too. Otherwise, the
             line will use the default width of `1.0`.
        color:
             Optional color for the scalar entry.

             If left unspecified, a pseudo-random color will be used instead. That
             same color will apply to all points residing in the same entity path
             that don't have a color specified.

             Points within a single line do not have to share the same color, the line
             will have differently colored segments as appropriate.
             If all points within a single entity path (i.e. a line) share the same
             color, then this color will be used as the line color in the plot legend.
             Otherwise, the line will appear gray in the legend.
        label:
             An optional label for the point.

             TODO(#1289): This won't show up on points at the moment, as our plots don't yet
             support displaying labels for individual points.
             If all points within a single entity path (i.e. a line) share the same label, then
             this label will be used as the label for the line itself. Otherwise, the
             line will be named after the entity path. The plot itself is named after
             the space it's in.
        scattered:
             Specifies whether a point in a scatter plot should form a continuous line.

             If set to true, this scalar will be drawn as a point, akin to a scatterplot.
             Otherwise, it will form a continuous line with its neighbors.
             Points within a single line do not have to all share the same scatteredness:
             the line will switch between a scattered and a continuous representation as
             required.
        """

        # You can define your own __init__ function as a member of TimeSeriesScalarExt in time_series_scalar_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(scalar=scalar, radius=radius, color=color, label=label, scattered=scattered)
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            scalar=None,  # type: ignore[arg-type]
            radius=None,  # type: ignore[arg-type]
            color=None,  # type: ignore[arg-type]
            label=None,  # type: ignore[arg-type]
            scattered=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> TimeSeriesScalar:
        """Produce an empty TimeSeriesScalar, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    scalar: components.ScalarBatch = field(
        metadata={"component": "required"},
        converter=components.ScalarBatch._required,  # type: ignore[misc]
    )
    # The scalar value to log.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    radius: components.RadiusBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.RadiusBatch._optional,  # type: ignore[misc]
    )
    # An optional radius for the point.
    #
    # Points within a single line do not have to share the same radius, the line
    # will have differently sized segments as appropriate.
    #
    # If all points within a single entity path (i.e. a line) share the same
    # radius, then this radius will be used as the line width too. Otherwise, the
    # line will use the default width of `1.0`.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    color: components.ColorBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ColorBatch._optional,  # type: ignore[misc]
    )
    # Optional color for the scalar entry.
    #
    # If left unspecified, a pseudo-random color will be used instead. That
    # same color will apply to all points residing in the same entity path
    # that don't have a color specified.
    #
    # Points within a single line do not have to share the same color, the line
    # will have differently colored segments as appropriate.
    # If all points within a single entity path (i.e. a line) share the same
    # color, then this color will be used as the line color in the plot legend.
    # Otherwise, the line will appear gray in the legend.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    label: components.TextBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.TextBatch._optional,  # type: ignore[misc]
    )
    # An optional label for the point.
    #
    # TODO(#1289): This won't show up on points at the moment, as our plots don't yet
    # support displaying labels for individual points.
    # If all points within a single entity path (i.e. a line) share the same label, then
    # this label will be used as the label for the line itself. Otherwise, the
    # line will be named after the entity path. The plot itself is named after
    # the space it's in.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    scattered: components.ScalarScatteringBatch | None = field(
        metadata={"component": "optional"},
        default=None,
        converter=components.ScalarScatteringBatch._optional,  # type: ignore[misc]
    )
    # Specifies whether a point in a scatter plot should form a continuous line.
    #
    # If set to true, this scalar will be drawn as a point, akin to a scatterplot.
    # Otherwise, it will form a continuous line with its neighbors.
    # Points within a single line do not have to all share the same scatteredness:
    # the line will switch between a scattered and a continuous representation as
    # required.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__
