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
Always include on function signatures. See [exercise_utils/git.py](../../../exercise_utils/git.py) for examples.

## Imports
Order: stdlib → third-party → local (blank lines between). See any exercise file for examples like [grocery_shopping/verify.py](../../../grocery_shopping/verify.py).

## Documentation
One-line docstrings for simple functions. See [exercise_utils/git.py](../../../exercise_utils/git.py) for examples.

## Best Practices
- **DRY**: Extract common logic
- **Early returns**: Check errors first
- **Single responsibility**: Functions < 50 lines, < 5 params
- **Context managers**: Use `with` for resources
- **Constants at top**: Module-level `UPPER_CASE`

## Anti-Patterns

**❌ Don't**:
- Raw subprocess calls
- Missing type hints
- Magic values/hardcoded numbers

**✅ Do**:
- Use exercise_utils wrappers (see [exercise_utils/git.py](../../../exercise_utils/git.py))
- Add type hints on all functions
- Use named constants

**Examples**: See [grocery_shopping/download.py](../../../grocery_shopping/download.py) for proper patterns.

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
