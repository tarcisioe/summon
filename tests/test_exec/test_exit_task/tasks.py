from summon.exec import exit
from summon.tasks import task


@task
def test_task(fail: bool = False) -> None:
    if fail:
        exit(1)

    exit()
