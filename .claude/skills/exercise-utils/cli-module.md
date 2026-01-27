# cli-module.md

## Overview
Utilities for running CLI commands with error handling.

See [exercise_utils/cli.py](../../../exercise_utils/cli.py) for implementation.

## Key Functions
- `run(command, verbose, env={}, exit_on_error=False)` → `CommandResult`
  - Returns result with `.stdout`, `.returncode`, `.is_success()`
- `run_command(command, verbose)` → `str | exits`
  - Simple runner, exits on failure
- `run_command_no_exit(command, verbose)` → `str | None`
  - Returns None on failure

## Usage Examples
See usages in:
- [exercise_utils/git.py](../../../exercise_utils/git.py)
- [exercise_utils/github_cli.py](../../../exercise_utils/github_cli.py)
