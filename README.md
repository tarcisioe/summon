Summon
======

Summon is a task runner, inspired by [Invoke](https://www.pyinvoke.org/), but
entirely type-hint compatible.

Summon is built upon [Typer](https://github.com/tiangolo/typer). Summon's tasks are
Typer [commands](https://typer.tiangolo.com/tutorial/commands/))!

Summon will run tasks from a `tasks.py` file, but also accepts plugins, powered
by [pluggy](https://pluggy.readthedocs.io/en/stable/), meaning that shared
tasks can be separated on a plugin package.
