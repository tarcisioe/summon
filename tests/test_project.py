from pathlib import Path

from pytest_mock import MockerFixture


def test_reverse_directory_search(datadir: Path, mocker: MockerFixture) -> None:
    from summon.project import reverse_directory_search

    test_dir = datadir / "reverse_directory_search"
    expected_path = test_dir / "searched_for"

    # Make datadir work as root.
    mocker.patch("pathlib.Path.anchor", datadir)

    assert reverse_directory_search("searched_for", test_dir) == expected_path
    assert (
        reverse_directory_search("searched_for", test_dir / "subdir") == expected_path
    )
    assert reverse_directory_search("does_not_exist", test_dir / "subdir") is None
