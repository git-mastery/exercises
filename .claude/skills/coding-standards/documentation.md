# documentation.md

## Module Docstrings

Every module should have a docstring at the top:

```python
"""Wrapper for Git CLI commands."""

import os
from typing import List
```

**Guidelines:**
- One-line summary of module purpose
- Use triple double quotes `"""`
- End with period

## Function Docstrings

### Simple Functions
One-line docstring for obvious functions:

```python
def tag(tag_name: str, verbose: bool) -> None:
    """Tags the latest commit with the given tag_name."""
    run_command(["git", "tag", tag_name], verbose)

def init(verbose: bool) -> None:
    """Initializes the current folder as a Git repository."""
    run_command(["git", "init", "--initial-branch=main"], verbose)
```

### Complex Functions
Multi-line docstring with details:

```python
def merge(target_branch: str, ff: bool, verbose: bool) -> None:
    """Merges the current branch with the target one.
    
    Forcefully sets --no-edit to avoid requiring the student to enter the commit
    message.
    """
    if ff:
        run_command(["git", "merge", target_branch, "--no-edit"], verbose)
    else:
        run_command(["git", "merge", target_branch, "--no-edit", "--no-ff"], verbose)
```

**Format:**
1. Summary line (< 80 chars)
2. Blank line
3. Additional details, notes, warnings

### With Parameters

For very complex functions, document parameters:

```python
def run(
    command: List[str],
    verbose: bool,
    env: Dict[str, str] = {},
    exit_on_error: bool = False,
) -> CommandResult:
    """Runs the given command, logging the output if verbose is True.
    
    Args:
        command: The command and arguments to run
        verbose: Whether to print output to console
        env: Additional environment variables
        exit_on_error: Exit program on command failure
        
    Returns:
        CommandResult with stdout, returncode, and is_success()
    """
```

**Note:** Parameters are already typed in signature, so docstring parameters are optional unless behavior is non-obvious.

## Class Docstrings

```python
class GitAutograderTestLoader:
    """Test runner factory for exercise validation.
    
    Provides context manager for setting up isolated test environments
    with repo-smith integration.
    """
    
    def __init__(self, exercise_name: str, grade_func: Callable) -> None:
        """Initialize test loader.
        
        Args:
            exercise_name: Name of the exercise being tested
            grade_func: Verification function from verify.py
        """
        self.exercise_name = exercise_name
        self.grade_func = grade_func
```

## Comments

### When to Use

**Good reasons:**
- Explain **why** code exists
- Document workarounds or non-obvious choices
- Warn about edge cases
- Mark TODOs

```python
# Force --initial-branch to ensure 'main' is used instead of system default
run_command(["git", "init", "--initial-branch=main"], verbose)

# TODO(woojiahao): Maybe these should be built from a class like builder
def commit(message: str, verbose: bool) -> None:
    ...

# Avoid interactive prompts in automated exercises
run_command(["git", "merge", target_branch, "--no-edit"], verbose)
```

**Bad reasons:**
- Restating what code does
- Obvious statements
- Commented-out code (delete it instead)

```python
# Bad - obvious from code
# Loop through files
for file in files:
    add(file)

# Bad - redundant
i = i + 1  # Increment i
```

### Comment Style

```python
# Single line comment - space after #

# Multi-line comments should be split
# across multiple lines, each starting
# with # and a space.

# For long explanations, consider if a docstring
# or better variable names would be clearer.
```

### TODO Comments

Format: `# TODO(username): Description`

```python
# TODO(woojiahao): Reconsider if this should be inlined within repo-smith
def create_start_tag() -> None:
    ...
```

## README Files

Every exercise should have a README.md:

```markdown
# Exercise Name

Brief description of what the exercise teaches.

## Objectives

- Learn concept A
- Practice skill B

## Instructions

1. Step one
2. Step two

## Verification

Describe what will be checked.
```

## Constants Documentation

Document error message constants with context:

```python
# Error messages
NO_ADD = "There are no new grocery list items added to the shopping list."
NO_REMOVE = "There are no grocery list items removed from the shopping list."
SHOPPING_LIST_FILE_MISSING = "The shopping-list.txt file should not be deleted."
ADD_NOT_COMMITTED = (
    "New grocery list items added to shopping-list.txt are not committed."
)
```

## Documentation Best Practices

1. **Keep it concise** - Users read code more than docs
2. **Update with code** - Outdated docs are worse than no docs
3. **Prefer clarity** - Good names > comments > docstrings
4. **Document the why** - The code shows the "what" and "how"
5. **Test examples** - Code in docstrings should work

## What NOT to Document

```python
# Don't document obvious type conversions
name = str(raw_name)  # Bad: convert to string

# Don't document standard library usage
files = os.listdir(path)  # Bad: get list of files

# Don't document clear variable assignments
username = get_github_username()  # Bad: get username
```
