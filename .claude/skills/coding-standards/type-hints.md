# type-hints.md

## General Policy
- **All function signatures** must have type hints
- **Public functions** must annotate parameters and return types
- **Internal/private functions** should have type hints when practical
- **Variables** should be typed when type isn't obvious

## Function Signatures

### Required
```python
def commit(message: str, verbose: bool) -> None:
    """Creates a commit with the given message."""
    run_command(["git", "commit", "-m", message], verbose)

def get_github_username(verbose: bool) -> str:
    """Returns the currently authenticated Github user's username."""
    result = run(["gh", "api", "user", "-q", ".login"], verbose)
    if result.is_success():
        return result.stdout.splitlines()[0]
    return ""
```

### Optional Parameters
```python
def clone_repo_with_git(
    repository_url: str, 
    verbose: bool, 
    name: Optional[str] = None
) -> None:
    if name is not None:
        run(["git", "clone", repository_url, name], verbose)
    else:
        run(["git", "clone", repository_url], verbose)
```

### Multiple Types
```python
from typing import Union
import pathlib

def create_or_update_file(
    filepath: str | pathlib.Path,  # Python 3.10+
    contents: Optional[str] = None
) -> None:
    ...

# For Python 3.9 compatibility:
def create_or_update_file(
    filepath: Union[str, pathlib.Path],
    contents: Optional[str] = None
) -> None:
    ...
```

## Collections

### Lists
```python
from typing import List

def add(files: List[str], verbose: bool) -> None:
    run_command(["git", "add", *files], verbose)

def get_commits() -> List[str]:
    return ["abc123", "def456"]
```

### Dictionaries
```python
from typing import Dict

def run(
    command: List[str],
    verbose: bool,
    env: Dict[str, str] = {},
) -> CommandResult:
    ...
```

### Sets
```python
from typing import Set

ORIGINAL_SHOPPING_LIST: Set[str] = {"Milk", "Eggs", "Bread"}
```

## Return Types

### None
```python
def init(verbose: bool) -> None:
    """Initializes the current folder as a Git repository."""
    run_command(["git", "init"], verbose)
```

### Optional
```python
from typing import Optional

def run_command(command: List[str], verbose: bool) -> Optional[str]:
    """Returns stdout or None on failure."""
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError:
        return None
```

### Complex Types
```python
from typing import Tuple, Iterator
from contextlib import contextmanager

@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        # setup
        yield test, rs
```

## Class Attributes

```python
from typing import Optional
from dataclasses import dataclass

@dataclass
class CommandResult:
    result: CompletedProcess[str]
    
    @property
    def stdout(self) -> str:
        return self.result.stdout.strip()
    
    @property
    def returncode(self) -> int:
        return self.result.returncode

class GitAutograderTest:
    def __init__(self, exercise_name: str) -> None:
        self.exercise_name: str = exercise_name
        self.__rs: Optional[RepoSmith] = None
    
    @property
    def rs(self) -> RepoSmith:
        assert self.__rs is not None
        return self.__rs
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
