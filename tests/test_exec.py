from pathlib import Path
from typing import List

import pytest
from pytest import MonkeyPatch


@pytest.fixture
def executable_base(datadir: Path) -> List[str]:
    return ['python', str(datadir / 'executable.py')]


def test_execute(executable_base: str) -> None:
    from summon.exec import execute, CommandSuccess

    result = execute(executable_base)

    assert isinstance(result, CommandSuccess)


def test_execute_failing_command(executable_base: List[str]) -> None:
    from summon.exec import execute, CommandError

    result = execute([*executable_base, '--fail'])

    assert isinstance(result, CommandError)
    assert result.exit_code == 1


def test_execute_with_raise_error(executable_base: str) -> None:
    from subprocess import CalledProcessError

    from summon.exec import execute

    with pytest.raises(CalledProcessError):
        execute([*executable_base, '--fail'], raise_error=True)


def test_exit_task(datadir: Path, monkeypatch: MonkeyPatch) -> None:
    from subprocess import run

    monkeypatch.chdir(datadir / 'test_exit_task')

    completed = run(['python', '-m', 'summon', 'test-task'])

    assert completed.returncode == 0

    completed = run(['python', '-m', 'summon', 'test-task', '--fail'])

    assert completed.returncode == 1


def test_check_commands_task(datadir: Path, monkeypatch: MonkeyPatch) -> None:
    from subprocess import run

    monkeypatch.chdir(datadir / 'test_check_commands_task')

    completed = run(['python', '-m', 'summon', 'test-task'])

    assert completed.returncode == 0

    completed = run(['python', '-m', 'summon', 'test-task', '--fail-one'])

    assert completed.returncode == 1
