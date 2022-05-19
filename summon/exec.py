import shlex
import subprocess
from dataclasses import dataclass
from typing import overload, Callable, List, Literal, Union

import typer


def run_command(
    command: Union[str, List[str]], *args, **kwargs
) -> subprocess.CompletedProcess:
    """Wrapper for subprocess.run to support passing the command as a string."""
    split_command = shlex.split(command) if isinstance(command, str) else command
    return subprocess.run(split_command, check=True, *args, **kwargs)


def command_output(command: Union[str, List[str]]) -> str:
    """Run a command and get its stdout."""
    process = run_command(command, stdout=subprocess.PIPE)
    return process.stdout.decode('utf8')


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


def check_commands(f: Callable[..., List[Result]]) -> Callable[..., List[Result]]:
    """Make a function that returns Results terminate the app if any of them failed."""
    from functools import wraps

    @wraps(f)
    def _inner(*args, **kwargs) -> List[Result]:
        results = f(*args, **kwargs)

        failed_results = [r for r in results if isinstance(r, CommandError)]

        if failed_results:
            for failed in failed_results:
                print(
                    f'Command "{failed.command_line}" failed with error code '
                    f'{failed.exit_code}.'
                )
            raise typer.Exit(code=1)

        return results

    return _inner


@overload
def execute(
    command: Union[str, List[str]], *, raise_error: Literal[True] = True
) -> CommandSuccess:
    """Overload for when raise_error is True.

    In this case, we never return CommandError (we raise the subprocess
    exception)."""


@overload
def execute(command: Union[str, List[str]], *, raise_error: Literal[False]) -> Result:
    """Overload for when raise_error is True.

    In this case, we never raise, and instead we return CommandError."""


def execute(command: Union[str, List[str]], *, raise_error: bool = True) -> Result:
    """Echo and run a command."""
    command_str = command if isinstance(command, str) else ' '.join(command)
    print(f'### Executing: {command_str}')

    try:
        run_command(command)
    except subprocess.CalledProcessError as e:
        if raise_error:
            raise

        return CommandError(command_str, e.returncode)

    return CommandSuccess(command_str)
