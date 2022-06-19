from pytest import CaptureFixture
from pytest_mock import MockerFixture


def test_task_smoke(capsys: CaptureFixture[str], mocker: MockerFixture) -> None:
    import sys  # noqa
    from summon.tasks import task
    from summon._typer_app import run

    mocker.patch('sys.argv', ['my_program', '--help'])

    @task
    def my_task() -> None:
        pass

    try:
        run()
    except SystemExit as e:
        assert e.code == 0

    captured = capsys.readouterr()

    assert 'my_program' in captured.out
