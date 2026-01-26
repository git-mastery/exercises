# github-module.md

## Overview
Wrapper functions for GitHub CLI (gh) commands.

See [exercise_utils/github_cli.py](../../exercise_utils/github_cli.py) for all functions.

## Functions
- `get_github_username(verbose)` → `str`
- `create_repo(name, verbose)`, `delete_repo(name, verbose)`, `clone_repo_with_gh(name, verbose, name=None)`
- `fork_repo(repo_name, fork_name, verbose, default_branch_only=True)`
- `has_repo(name, is_fork, verbose)` → `bool`, `has_fork(repo, owner, username, verbose)` → `bool`
- `get_fork_name(repo, owner, username, verbose)` → `str`

**Prerequisites:** GitHub CLI (`gh`) installed and authenticated.

## Usage Examples
See [fork_repo/download.py](../../fork_repo/download.py) for fork/clone pattern.
