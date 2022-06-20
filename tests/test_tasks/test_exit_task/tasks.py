from summon import execute
from summon.tasks import task


@task
def test_task(fail: bool = False) -> None:
    if fail:
        execute.exit(1)

    execute.exit()
