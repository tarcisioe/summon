from typer.models import CommandFunctionType


def task(f: CommandFunctionType) -> CommandFunctionType:
    from ._typer_app import APP

    APP.command()(f)
    return f
