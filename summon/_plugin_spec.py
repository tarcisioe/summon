import pluggy


hookspec = pluggy.HookspecMarker("summon")


@hookspec
def register_tasks() -> None:
    """Register tasks using summon.tasks.task."""
