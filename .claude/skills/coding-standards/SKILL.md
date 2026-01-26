---
name: coding-standards
description: Code style and quality guidelines. Use when writing or reviewing code to ensure consistency.
---

# Coding Standards

## Overview
Follow these standards to ensure consistency, readability, and maintainability.

## Quick Rules

### Style
- **Line length**: 88 characters (Black/Ruff default)
- **Indentation**: 4 spaces
- **Formatter**: ruff (`ruff format .`)
- **Linter**: ruff (`ruff check .`)
- **Type checker**: mypy

### Naming
- **Functions/variables**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`  
- **Classes**: `PascalCase`
- **Directories**: `kebab-case`

### Type Hints
```python
# Always include types
def my_function(param: str, verbose: bool) -> Optional[str]:
    pass
```

## Detailed Guides

📄 **[style-guide.md](style-guide.md)** - Formatting, line length, imports, indentation

📄 **[naming-conventions.md](naming-conventions.md)** - Functions, classes, files, directories

📄 **[type-hints.md](type-hints.md)** - Using type annotations, common patterns

📄 **[documentation.md](documentation.md)** - Docstrings, comments, when to document

📄 **[best-practices.md](best-practices.md)** - DRY, composition, error handling, patterns

## Quick Checks

```bash
# Format code
ruff format .

# Check linting  
ruff check .

# Auto-fix
ruff check --fix .

# Type check
mypy <directory>/

# All checks
ruff format . && ruff check . && mypy .
```

## Common Patterns

### Import Organization
```python
# 1. Standard library
import os
from typing import List, Optional

# 2. Third party
from git_autograder import GitAutograderExercise

# 3. Local
from exercise_utils.git import add, commit
```

### Function Documentation
```python
def merge_with_message(
    target_branch: str, ff: bool, message: str, verbose: bool
) -> None:
    """Merge target branch with custom message.
    
    Args:
        target_branch: Branch to merge
        ff: Allow fast-forward if True
        message: Custom commit message
        verbose: Print output if True
    """
    pass
```

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
