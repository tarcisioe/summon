from summon.tasks import task


@task
def hello() -> str:
    print("Hello world")
