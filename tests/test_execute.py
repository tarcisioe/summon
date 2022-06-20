"""Tests for the `summon.execute` module."""
from pathlib import Path
from typing import List

import pytest


@pytest.fixture
def executable_base(datadir: Path) -> List[str]:
    """Base command line for running a test executable."""
    import sys

    return [sys.executable, str(datadir / "executable.py")]


def test_execute(executable_base: str) -> None:
    """Executing a successful command should return success."""
    from summon.execute import CommandSuccess, execute

    result = execute(executable_base)

    assert isinstance(result, CommandSuccess)


def test_execute_failing_command(executable_base: List[str]) -> None:
    """Executing a failing command should return an error."""
    from summon.execute import CommandError, execute

    result = execute([*executable_base, "--fail"])

    assert isinstance(result, CommandError)
    assert result.exit_code == 1


def test_execute_with_raise_error(executable_base: str) -> None:
    """Executing a failing command with `raise_error` should raise."""
    from subprocess import CalledProcessError

    from summon.execute import execute

    with pytest.raises(CalledProcessError):
        execute([*executable_base, "--fail"], raise_error=True)
