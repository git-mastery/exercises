# type-hints.md

## Policy
- All function signatures need type hints
- Variables when type isn't obvious

## Common Types
```python
def func(name: str, count: int, verbose: bool) -> None:
    ...

def get_data(path: Optional[str] = None) -> List[str]:
    ...

def process(items: List[str], config: Dict[str, str]) -> Tuple[int, bool]:
    ...
```

## Forward References

```python
from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from git import Repo

class GitMasteryHelper:
    def __init__(self, repo: Repo, verbose: bool) -> None:
        self.repo = repo
```

## Common Imports

```python
from typing import (
    Any,
    Callable,
    Dict,
    Iterator,
    List,
    Optional,
    Set,
    Tuple,
    Union,
)
```

## When to Skip Type Hints

### Lambda functions (optional)
```python
# OK without types
files = sorted(files, key=lambda f: f.name)
```

### Very short internal helpers
```python
# OK for simple one-liners
def _strip(s):
    return s.strip()
```

### Tests with obvious types
```python
# Function signature should be typed
def test_no_answers():
    # Local variables in tests can skip types when obvious
    expected = "error message"
    output = test.run()
```

## Type Checking

Use `mypy` for type checking:

```bash
mypy exercise_utils/
mypy amateur_detective/verify.py
```
