"""File-specific utility functions."""

import os
import pathlib
import textwrap
from typing import Optional


def create_or_update_file(
    filepath: str | pathlib.Path, contents: Optional[str] = None
) -> None:
    """Creates or updates a file with the given content."""
    if os.path.dirname(filepath) != "":
        os.makedirs(os.path.dirname(filepath), exist_ok=True)

    if contents is None:
        open(filepath, "a").close()
    else:
        with open(filepath, "w") as file:
            file.write(textwrap.dedent(contents).lstrip())


def append_to_file(filepath: str | pathlib.Path, contents: str) -> None:
    """Appends contents to file."""
    with open(filepath, "a") as file:
        file.write(textwrap.dedent(contents).lstrip())
