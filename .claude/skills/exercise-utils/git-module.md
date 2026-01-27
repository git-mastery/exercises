# git-module.md

## Overview
Wrapper functions for Git CLI commands.

See [exercise_utils/git.py](../../../exercise_utils/git.py) for all functions.

## Functions
- `init(verbose)`, `add(files, verbose)`, `commit(message, verbose)`, `empty_commit(message, verbose)`
- `checkout(branch, create_branch, verbose)`, `merge(target_branch, ff, verbose)`
- `tag(tag_name, verbose)`, `tag_with_options(tag_name, options, verbose)`
- `add_remote(remote, url, verbose)`, `remove_remote(remote, verbose)`, `push(remote, branch, verbose)`
- `track_remote_branch(remote, branch, verbose)`, `clone_repo_with_git(url, verbose, name=None)`
