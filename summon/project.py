from pathlib import Path
from typing import Optional


def reverse_directory_search(filename: str, search_base: Path) -> Optional[Path]:
    """Search backwards for a file starting on a given directory.

    E.g.: from /a/b/c a file d.txt will be checked in the following order:
        - /a/b/c/d.txt
        - /a/b/d.txt
        - /a/d.txt
        - /d.txt

    Args:
        filename: the name of the file to search for.
        search_base: the directory where to start the search.

    Return:
        the full path, if the file is found, otherwise None
    """
    search_base = search_base.absolute()
    root = Path(search_base.anchor)

    while search_base != root:
        file_path = search_base / filename
        if file_path.exists():
            return file_path
        search_base = search_base.parent

    return None
