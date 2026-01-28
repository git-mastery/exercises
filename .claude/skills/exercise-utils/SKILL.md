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

**Most common functions**:
- Git: `init()`, `add()`, `commit()`, `checkout()`, `merge()`, `push()`
- GitHub: `fork_repo()`, `get_github_username()`, `clone_repo_with_gh()`
- File: `create_or_update_file()`, `append_to_file()`
- Start tag: `create_start_tag()` (always last in download.py)
- Testing: `GitAutograderTestLoader`, `assert_output()`

**Examples**: See [grocery_shopping/download.py](../../../grocery_shopping/download.py) and [amateur_detective/test_verify.py](../../../amateur_detective/test_verify.py).

## Common Patterns

**Complete exercise setup**: See [grocery_shopping/download.py](../../../grocery_shopping/download.py)

**GitHub fork pattern**: See [fork_repo/download.py](../../../fork_repo/download.py)

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
