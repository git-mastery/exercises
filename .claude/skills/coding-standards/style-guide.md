# style-guide.md

## Code Formatting

### Line Length
- **Maximum 88 characters** (Black default)
- Break long lines at logical points

### Imports
**Order:**
1. Standard library imports
2. Third-party imports
3. Local application imports

**Separate groups with blank lines:**
```python
import os
from typing import List, Optional

from git_autograder import GitAutograderExercise
from repo_smith.repo_smith import RepoSmith

from exercise_utils.git import commit, checkout
from .verify import verify
```

### String Quotes
- Use **double quotes** `"` for strings by default
- Single quotes `'` acceptable but be consistent within a file
- Use triple quotes `"""` for multiline strings and docstrings

### Whitespace
- 2 blank lines between top-level functions/classes
- 1 blank line between methods in a class
- No trailing whitespace
- End files with single newline

### Indentation
- **4 spaces** (no tabs)
- Continuation lines: align or use hanging indent

```python
# Good - aligned
result = some_function(
    arg1, arg2,
    arg3, arg4
)

# Good - hanging indent
result = some_function(
    arg1,
    arg2,
    arg3,
)
```

## Function/Method Style

### Arguments
```python
# Short - single line
def commit(message: str, verbose: bool) -> None:
    ...

# Long - one per line
def fork_repo(
    repository_name: str,
    fork_name: str,
    verbose: bool,
    default_branch_only: bool = True,
) -> None:
    ...
```

### Return Statements
- Early returns for error conditions
- Main logic with minimal nesting

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if not exercise.repo:
        raise exercise.invalid_state(["No repository found"])
    
    # Main logic here
    return exercise.to_output(["Success"], GitAutograderStatus.SUCCESSFUL)
```

## Comments
- Use sparingly - code should be self-documenting
- Explain **why**, not **what**
- TODO comments: `# TODO(username): Description`

```python
# Good - explains why
if create_branch:
    # Force --initial-branch to ensure 'main' is used
    run_command(["git", "init", "--initial-branch=main"], verbose)

# Bad - restates the code
# Loop through files
for file in files:
    ...
```

## File Organization

### Module Structure
1. Module docstring
2. Imports
3. Constants (UPPER_CASE)
4. Functions/Classes

```python
"""Module description."""

import os
from typing import List

from git_autograder import GitAutograderExercise

ERROR_MESSAGE = "Something went wrong"


def main_function():
    ...
```
