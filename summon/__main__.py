from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path

import pluggy

from . import _plugin_spec, _typer_app
from .project import reverse_directory_search


def get_plugin_manager() -> pluggy.PluginManager:
    manager = pluggy.PluginManager("summon")
    manager.add_hookspecs(_plugin_spec)
    manager.load_setuptools_entrypoints("summon")
    return manager


def main() -> None:
    manager = get_plugin_manager()
    manager.hook.register_tasks()  # pylint: disable=no-member
    tasks_file = reverse_directory_search('tasks.py', Path.cwd())
    if tasks_file is not None:
        tasks_spec = spec_from_file_location('_summon_user_tasks', tasks_file)
        assert tasks_spec is not None
        module = module_from_spec(tasks_spec)
        assert tasks_spec.loader is not None
        tasks_spec.loader.exec_module(module)
    _typer_app.APP()


if __name__ == '__main__':
    main()
