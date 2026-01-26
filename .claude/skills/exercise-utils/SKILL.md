---
name: exercise-utils
description: Reference for shared utility modules. Use when working with Git commands, GitHub operations, or need API details for utility functions.
---

# Exercise Utils Reference

## Overview
The `exercise_utils/` package provides reusable wrappers for common operations. **Always use these instead of raw subprocess calls.**

## Quick Navigation

### Module References
📄 **[git-module.md](git-module.md)** - Git command wrappers (`init`, `add`, `commit`, `checkout`, `merge`, `push`, etc.)

📄 **[github-module.md](github-module.md)** - GitHub CLI wrappers (`fork_repo`, `create_repo`, `delete_repo`, etc.)

📄 **[cli-module.md](cli-module.md)** - General CLI execution (`run`, `run_command`, `CommandResult`)

📄 **[file-module.md](file-module.md)** - File operations (`create_or_update_file`, `append_to_file`)

📄 **[gitmastery-module.md](gitmastery-module.md)** - Git-Mastery specific (`create_start_tag`)

📄 **[test-module.md](test-module.md)** - Test scaffolding (`GitAutograderTestLoader`, `assert_output`)

## Quick Reference

### Most Common Functions

```python
# Git operations
from exercise_utils.git import init, add, commit, checkout
init(verbose)
add(["file.txt"], verbose)
commit("Initial commit", verbose)
checkout("branch-name", create_branch=True, verbose=verbose)

# GitHub operations  
from exercise_utils.github_cli import fork_repo, get_github_username
username = get_github_username(verbose)
fork_repo("owner/repo", "fork-name", verbose)

# File operations
from exercise_utils.file import create_or_update_file, append_to_file
create_or_update_file("file.txt", "content")
append_to_file("log.txt", "new entry\n")

# Start tag (always last in download.py)
from exercise_utils.gitmastery import create_start_tag
create_start_tag(verbose)

# Testing
from exercise_utils.test import GitAutograderTestLoader, assert_output
loader = GitAutograderTestLoader(REPO_NAME, verify)
with loader.start(mock_answers={}) as (test, _):
    output = test.run()
    assert_output(output, status, messages)
```

## Common Patterns

### Complete Exercise Setup
```python
from exercise_utils.git import init, add, commit
from exercise_utils.file import create_or_update_file
from exercise_utils.gitmastery import create_start_tag

def download(verbose: bool):
    create_or_update_file("README.md", "# Project\n")
    init(verbose)
    add(["README.md"], verbose)
    commit("Initial commit", verbose)
    create_start_tag(verbose)  # Always last
```

### GitHub Fork Pattern
```python
from exercise_utils.github_cli import get_github_username, fork_repo
from exercise_utils.git import clone_repo_with_git

username = get_github_username(verbose)
fork_repo("git-mastery/repo", "my-fork", verbose)
clone_repo_with_git(f"https://github.com/{username}/my-fork", verbose)
```

## Key Principles

1. **Always pass verbose parameter** - All functions accept it
2. **Use wrappers, not subprocess** - Never call git/gh directly
3. **Type hints required** - All functions are fully typed
4. **Errors handled** - Most functions exit on error

## Module Dependencies

```
cli.py          # No dependencies (base module)
├── git.py      # Depends on cli
├── github_cli.py  # Depends on cli
├── file.py     # No dependencies
├── gitmastery.py  # Depends on cli
└── test.py     # Depends on git, file, gitmastery
```

## Related Skills

- **[exercise-development](../exercise-development/SKILL.md)** - Using utilities in exercises
- **[coding-standards](../coding-standards/SKILL.md)** - Code conventions
- **[testing](../testing/SKILL.md)** - Using test utilities
