"""Tests for the `summon.tasks` module."""
from pathlib import Path

from pytest import MonkeyPatch


def test_exit_task(datadir: Path, monkeypatch: MonkeyPatch) -> None:
    """A task that uses `exit` should cause the return code to be as defined."""
    from subprocess import run

    monkeypatch.chdir(datadir / "test_exit_task")

    completed = run(["python", "-m", "summon", "test-task"], check=False)

    assert completed.returncode == 0

    completed = run(["python", "-m", "summon", "test-task", "--fail"], check=False)

    assert completed.returncode == 1


def test_single_result_task(datadir: Path, monkeypatch: MonkeyPatch) -> None:
    """A task that returns a list of results should fail if one of them fails."""
    from subprocess import run

    monkeypatch.chdir(datadir / "test_single_result_task")

    completed = run(["python", "-m", "summon", "test-task"], check=False)

    assert completed.returncode == 0

    completed = run(["python", "-m", "summon", "test-task", "--fail"], check=False)

    assert completed.returncode == 3


def test_many_results_task(datadir: Path, monkeypatch: MonkeyPatch) -> None:
    """A task that returns a list of results should fail if one of them fails."""
    from subprocess import run

    monkeypatch.chdir(datadir / "test_many_results_task")

    completed = run(["python", "-m", "summon", "test-task"], check=False)

    assert completed.returncode == 0

    completed = run(["python", "-m", "summon", "test-task", "--fail-one"], check=False)

    assert completed.returncode == 1
