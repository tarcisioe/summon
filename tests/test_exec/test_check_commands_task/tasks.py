from typing import List

from summon.exec import check_commands, CommandError, CommandSuccess, Result
from summon.tasks import task


@task
@check_commands
def test_task(fail_one: bool = False) -> List[Result]:
    return [
        CommandSuccess('dummy'),
        CommandError('dummy2', 3) if fail_one else CommandSuccess('dummy2'),
        CommandSuccess('dummy3'),
    ]
