"""Command execution functionality."""
import shlex
import subprocess
from dataclasses import dataclass
from typing import List, NoReturn, Optional, Union, overload

import typer
from typing_extensions import Literal, TypeGuard


def _run(
    command: Union[str, List[str]],
    stdout: Optional[int] = None,
) -> "subprocess.CompletedProcess[bytes]":
    """Wrapper for subprocess.run to support passing the command as a string."""
    split_command = shlex.split(command) if isinstance(command, str) else command
    return subprocess.run(split_command, check=True, stdout=stdout)


@dataclass
class CommandError:
    """Represent that a given command failed."""

    command_line: str
    exit_code: int


@dataclass
class CommandSuccess:
    """Represent that a given command ran successfully."""

    command_line: str


Result = Union[CommandError, CommandSuccess]


class _Exit(typer.Exit):
    """Signal that the program should exit."""


def exit(code: int = 0) -> NoReturn:  # pylint: disable=redefined-builtin
    """Exit with a given result code.

    Must be used inside a summon task.
    """
    raise _Exit(code=code)


def all_success(results: List[Result]) -> TypeGuard[List[CommandSuccess]]:
    """Assert that all Results are `CommandSuccess`es."""
    return all(isinstance(r, CommandSuccess) for r in results)


@overload
def execute(
    command: Union[str, List[str]],
    *,
    raise_error: Literal[True],
) -> CommandSuccess:
    """Overload for when raise_error is True.

    In this case, we never return CommandError (we raise the subprocess
    exception).
    """


@overload
def execute(
    command: Union[str, List[str]],
    *,
    raise_error: Literal[False] = False,
) -> Result:
    """Overload for when raise_error is True.

    In this case, we never raise, and instead we return CommandError.
    """


def execute(
    command: Union[str, List[str]],
    *,
    raise_error: bool = False,
) -> Result:
    """Echo and run a command."""
    command_str = command if isinstance(command, str) else " ".join(command)
    print(f"### Executing: {command_str}")

    try:
        _run(command)
    except subprocess.CalledProcessError as exc:
        if raise_error:
            raise

        return CommandError(command_str, exc.returncode)

    return CommandSuccess(command_str)
