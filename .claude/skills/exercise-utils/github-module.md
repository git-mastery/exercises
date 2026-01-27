# github-module.md

## Overview
Wrapper functions for GitHub CLI (gh) commands.

See [exercise_utils/github_cli.py](../../../exercise_utils/github_cli.py) for all functions.

## Functions
- `get_github_username(verbose)` → `str`
- `create_repo(repository_name, verbose)`, `delete_repo(repository_name, verbose)`, `clone_repo_with_gh(repository_name, verbose, name=None)`
- `fork_repo(repository_name, fork_name, verbose, default_branch_only=True)`
- `has_repo(repo_name, is_fork, verbose)` → `bool`, `has_fork(repository_name, owner, username, verbose)` → `bool`
- `get_fork_name(repository_name, owner, username, verbose)` → `str`

**Prerequisites:** GitHub CLI (`gh`) installed and authenticated.
