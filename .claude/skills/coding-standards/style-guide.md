# style-guide.md

## Formatting
- **88 char line length**
- **4 spaces** indentation (no tabs)
- **Double quotes** for strings
- 2 blank lines between functions, 1 between methods

## Imports
Order: stdlib → third-party → local (separate with blank lines)

```python
import os
from typing import List

from git_autograder import GitAutograderExercise

from exercise_utils.git import commit
```

## Functions
```python
# Short
def commit(message: str, verbose: bool) -> None:
    ...

# Long - one param per line
def fork_repo(
    repository_name: str,
    fork_name: str,
    verbose: bool,
) -> None:
    ...
```

## Comments
- Explain **why**, not what
- `# TODO(username): Description`
- Minimize - prefer clear code

## File Structure
1. Module docstring
2. Imports
3. Constants (UPPER_CASE)
4. Functions/Classes
