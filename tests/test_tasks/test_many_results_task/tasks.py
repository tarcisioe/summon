from typing import List

from summon.execute import CommandError, CommandSuccess, Result
from summon.tasks import task_with_results


@task_with_results
def test_task(fail_one: bool = False) -> List[Result]:
    return [
        CommandSuccess("dummy"),
        CommandError("dummy2", 3) if fail_one else CommandSuccess("dummy2"),
        CommandSuccess("dummy3"),
    ]
