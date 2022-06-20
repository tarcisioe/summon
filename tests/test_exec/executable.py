import typer


APP = typer.Typer()


@APP.command()
def main(fail: bool = False) -> None:
    if fail:
        raise typer.Exit(1)


if __name__ == '__main__':
    APP()
