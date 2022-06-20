"""Task-creating decorators."""
from typing import Callable, List, TypeVar

from typing_extensions import ParamSpec

from . import execute
from .execute import CommandError, CommandSuccess, Result, all_success

_T = TypeVar("_T")
_P = ParamSpec("_P")
_F = TypeVar("_F", bound=Callable[..., None])
_FWithResult = TypeVar("_FWithResult", bound=Callable[..., Result])
_FWithResults = TypeVar("_FWithResults", bound=Callable[..., List[Result]])


def _check_result(result: Result) -> CommandSuccess:
    """Check a result and raise if it is a `CommandError`."""
    if isinstance(result, CommandError):
        print(
            f'Command "{result.command_line}" failed with error code '
            f"{result.exit_code}."
        )
        execute.exit(result.exit_code)

    return result


def _check_command(
    func: Callable[_P, Result],
) -> Callable[_P, CommandSuccess]:
    """Make a function that returns a Result terminate the app if it failed."""
    from functools import wraps

    @wraps(func)
    def _inner(*args: _P.args, **kwargs: _P.kwargs) -> CommandSuccess:
        return _check_result(func(*args, **kwargs))

    return _inner


def _check_commands(
    func: Callable[_P, List[Result]],
) -> Callable[_P, List[CommandSuccess]]:
    """Make a function that returns Results terminate the app if any of them failed."""
    from functools import wraps

    @wraps(func)
    def _inner(*args: _P.args, **kwargs: _P.kwargs) -> List[CommandSuccess]:
        results = func(*args, **kwargs)

        if all_success(results):
            return results

        for failed in (r for r in results if isinstance(r, CommandError)):
            print(
                f'Command "{failed.command_line}" failed with error code '
                f"{failed.exit_code}."
            )
        execute.exit(1)

    return _inner


def task(func: _F) -> _F:
    """Make a function into a summon task."""
    from ._typer_app import APP

    APP.command()(func)
    return func


def task_with_result(func: _FWithResult) -> _FWithResult:
    """Make a function that return a list of Result into a summon task."""
    from ._typer_app import APP

    APP.command()(_check_command(func))
    return func


def task_with_results(func: _FWithResults) -> _FWithResults:
    """Make a function that return a list of Result into a summon task."""
    from ._typer_app import APP

    APP.command()(_check_commands(func))
    return func
