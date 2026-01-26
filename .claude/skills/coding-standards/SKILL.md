---
name: coding-standards
description: Code style and quality guidelines. Use when writing or reviewing code to ensure consistency.
---

# Coding Standards

## Tools
```bash
ruff format .                 # Format code
ruff check .                  # Check linting
ruff check --fix .           # Auto-fix issues
mypy <directory>/            # Type checking
```

## Style
- **88 char** line length
- **4 spaces** indentation
- **Double quotes** for strings
- 2 blank lines between functions

## Naming
- **Functions/Variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Classes**: `PascalCase`
- **Tests**: `test_description`
- **Directories**: `kebab-case`
- Actions: `create_*`, `add_*`, `remove_*`
- Queries: `get_*`, `has_*`, `is_*`

## Type Hints
Always include on function signatures:
```python
def func(name: str, count: int, verbose: bool) -> None:
    ...

def get_data(path: Optional[str] = None) -> List[str]:
    ...
```

## Imports
Order: stdlib → third-party → local (blank lines between)
```python
import os
from typing import List

from git_autograder import GitAutograderExercise

from exercise_utils.git import commit
```

## Documentation
```python
def tag(tag_name: str, verbose: bool) -> None:
    """Tags the latest commit with the given tag_name."""
    ...
```

## Best Practices
- **DRY**: Extract common logic
- **Early returns**: Check errors first
- **Single responsibility**: Functions < 50 lines, < 5 params
- **Context managers**: Use `with` for resources
- **Constants at top**: Module-level `UPPER_CASE`

## Anti-Patterns

### ❌ Don't
```python
# Raw subprocess
import subprocess
subprocess.run(["git", "add", "file.txt"])

# No type hints
def process(data):
    return data.strip()

# Magic values
if count > 5:
    pass
```

### ✅ Do
```python
# Use wrappers
from exercise_utils.git import add
add(["file.txt"], verbose)

# Type hints
def process(data: str) -> str:
    return data.strip()

# Named constants
MAX_RETRIES = 5
if count > MAX_RETRIES:
    pass
```

## Pre-Commit Checklist

- ✓ `ruff format .` - Code formatted
- ✓ `ruff check .` - No lint errors
- ✓ `mypy .` - Type hints valid
- ✓ Docstrings on public functions
- ✓ No hardcoded values
- ✓ Imports organized

## Related Skills

- **[exercise-development](../exercise-development/SKILL.md)** - Applying standards
- **[exercise-utils](../exercise-utils/SKILL.md)** - Using utilities correctly
- **[testing](../testing/SKILL.md)** - Test code standards
