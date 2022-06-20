import shlex
import subprocess
from dataclasses import dataclass
from typing import Callable, List, NoReturn, Optional, Union, overload

import typer
from typing_extensions import Literal, ParamSpec


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


_P = ParamSpec("_P")
Result = Union[CommandError, CommandSuccess]


class _Exit(typer.Exit):
    """Signal that the program should exit."""


def exit(code: int = 0) -> NoReturn:
    """Exit with a given result code.

    Must be used inside a summon task.
    """
    raise _Exit(code=code)


def check_commands(
    f: Callable[_P, List[Result]],
) -> Callable[_P, List[Result]]:
    """Make a function that returns Results terminate the app if any of them failed."""
    from functools import wraps

    @wraps(f)
    def _inner(*args: _P.args, **kwargs: _P.kwargs) -> List[Result]:
        results = f(*args, **kwargs)

        failed_results = [r for r in results if isinstance(r, CommandError)]

        if failed_results:
            for failed in failed_results:
                print(
                    f'Command "{failed.command_line}" failed with error code '
                    f"{failed.exit_code}."
                )
            exit(1)

        return results

    return _inner


@overload
def execute(
    command: Union[str, List[str]],
    *,
    raise_error: Literal[True],
) -> CommandSuccess:
    """Overload for when raise_error is True.

    In this case, we never return CommandError (we raise the subprocess
    exception)."""


@overload
def execute(
    command: Union[str, List[str]],
    *,
    raise_error: Literal[False] = False,
) -> Result:
    """Overload for when raise_error is True.

    In this case, we never raise, and instead we return CommandError."""


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
    except subprocess.CalledProcessError as e:
        if raise_error:
            raise

        return CommandError(command_str, e.returncode)

    return CommandSuccess(command_str)
