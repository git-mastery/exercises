# file-module.md

## Overview
File creation and modification utilities.

See [exercise_utils/file.py](../../../exercise_utils/file.py) for implementation.

## Functions
- `create_or_update_file(filepath, contents=None)` - Create/overwrite file, auto-creates directories
- `append_to_file(filepath, contents)` - Append content to file

**Features:** Auto-dedenting with `textwrap.dedent()`, automatic directory creation.

## Usage Examples
See usages in download.py files across exercises.
