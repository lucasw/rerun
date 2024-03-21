# DO NOT EDIT! This file was auto-generated by crates/re_types_builder/src/codegen/python/mod.rs
# Based on "crates/re_types/definitions/rerun/blueprint/archetypes/space_view_contents.fbs".

# You can extend this class by creating a "SpaceViewContentsExt" class in "space_view_contents_ext.py".

from __future__ import annotations

from typing import Any

from attrs import define, field

from ... import datatypes
from ..._baseclasses import Archetype
from ...blueprint import components as blueprint_components
from ...error_utils import catch_and_log_exceptions

__all__ = ["SpaceViewContents"]


@define(str=False, repr=False, init=False)
class SpaceViewContents(Archetype):
    """
    **Archetype**: The contents of a `SpaceView`.

    The contents are found by combining a collection of `QueryExpression`s.

    ```diff
    + /world/**           # add everything…
    - /world/roads/**     # …but remove all roads…
    + /world/roads/main   # …but show main road
    ```

    If there is multiple matching rules, the most specific rule wins.
    If there are multiple rules of the same specificity, the last one wins.
    If no rules match, the path is excluded.

    The `/**` suffix matches the whole subtree, i.e. self and any child, recursively
    (`/world/**` matches both `/world` and `/world/car/driver`).
    Other uses of `*` are not (yet) supported.

    Internally, `EntityPathFilter` sorts the rule by entity path, with recursive coming before non-recursive.
    This means the last matching rule is also the most specific one. For instance:
    ```diff
    + /world/**
    - /world
    - /world/car/**
    + /world/car/driver
    ```

    The last rule matching `/world/car/driver` is `+ /world/car/driver`, so it is included.
    The last rule matching `/world/car/hood` is `- /world/car/**`, so it is excluded.
    The last rule matching `/world` is `- /world`, so it is excluded.
    The last rule matching `/world/house` is `+ /world/**`, so it is included.

    Unstable. Used for the ongoing blueprint experimentations.
    """

    def __init__(self: Any, query: datatypes.Utf8ArrayLike):
        """
        Create a new instance of the SpaceViewContents archetype.

        Parameters
        ----------
        query:
            The `QueryExpression` that populates the contents for the `SpaceView`.

            They determine which entities are part of the spaceview.

        """

        # You can define your own __init__ function as a member of SpaceViewContentsExt in space_view_contents_ext.py
        with catch_and_log_exceptions(context=self.__class__.__name__):
            self.__attrs_init__(query=query)
            return
        self.__attrs_clear__()

    def __attrs_clear__(self) -> None:
        """Convenience method for calling `__attrs_init__` with all `None`s."""
        self.__attrs_init__(
            query=None,  # type: ignore[arg-type]
        )

    @classmethod
    def _clear(cls) -> SpaceViewContents:
        """Produce an empty SpaceViewContents, bypassing `__init__`."""
        inst = cls.__new__(cls)
        inst.__attrs_clear__()
        return inst

    query: blueprint_components.QueryExpressionBatch = field(
        metadata={"component": "required"},
        converter=blueprint_components.QueryExpressionBatch._required,  # type: ignore[misc]
    )
    # The `QueryExpression` that populates the contents for the `SpaceView`.
    #
    # They determine which entities are part of the spaceview.
    #
    # (Docstring intentionally commented out to hide this field from the docs)

    __str__ = Archetype.__str__
    __repr__ = Archetype.__repr__  # type: ignore[assignment]