"""Specs for the `pluggy` plugins."""
from typing import Any, Callable, TypeVar, cast

import pluggy

F = TypeVar("F", bound=Callable[..., Any])

hookspec = cast(Callable[[F], F], pluggy.HookspecMarker("summon"))


@hookspec
def register_tasks() -> None:
    """Register tasks using summon.tasks.task."""
