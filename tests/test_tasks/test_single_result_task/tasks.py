from typing import List

from summon.execute import CommandError, CommandSuccess, Result
from summon.tasks import task_with_result


@task_with_result
def test_task(fail: bool = False) -> Result:
    return CommandError("dummy2", 3) if fail else CommandSuccess("dummy2")
