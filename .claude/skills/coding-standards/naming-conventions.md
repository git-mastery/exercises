# naming-conventions.md

## General Rules
- Names should be **descriptive** and **unambiguous**
- Avoid abbreviations except common ones (e.g., `repo`, `config`, `args`)
- Never use single-letter names except loop counters (`i`, `j`) or math formulas

## Functions
**snake_case** - lowercase with underscores

```python
# Good
def create_start_tag(verbose: bool):
    ...

def get_github_username(verbose: bool) -> str:
    ...

def has_fork(repository_name: str, owner_name: str) -> bool:
    ...
```

**Naming patterns:**
- Actions: `create_`, `add_`, `remove_`, `delete_`, `update_`
- Queries: `get_`, `find_`, `has_`, `is_`, `check_`
- Boolean returns: `is_*`, `has_*`, `should_*`, `can_*`

## Variables
**snake_case** - lowercase with underscores

```python
repository_name = "my-repo"
user_commits = []
is_fork = False
file_path = "/path/to/file"
```

## Constants
**UPPER_SNAKE_CASE** - all uppercase with underscores

```python
QUESTION_ONE = "Which file was added?"
SHOPPING_LIST_FILE_MISSING = "The shopping-list.txt file should not be deleted."
ORIGINAL_SHOPPING_LIST = {"Milk", "Eggs", "Bread"}
REPOSITORY_NAME = "amateur-detective"
```

## Classes
**PascalCase** - capitalize each word, no separators

```python
class GitAutograderTest:
    ...

class GitMasteryHelper:
    ...

class CommandResult:
    ...
```

## Modules/Files
**snake_case.py** - lowercase with underscores

```
exercise_utils/
    git.py
    github_cli.py
    file.py
    test.py
```

## Directories
**snake_case** - lowercase with underscores

```
exercises/
    amateur_detective/
    grocery_shopping/
    branch_compare/
    exercise_utils/
```

**Exceptions:**
- Hands-on directories: hyphenated (e.g., `hands_on/`)
- Exercise names: may use hyphens in repo names but underscores in directories

## Test Functions
Prefix with `test_`, describe what's being tested

```python
def test_no_answers():
    ...

def test_wrong_question_one():
    ...

def test_valid_answers():
    ...

def test_incomplete_answer():
    ...
```

## Private/Internal
Prefix with single underscore `_`

```python
class GitAutograderTest:
    def __init__(self):
        self._internal_state = None
        self.__rs: Optional[RepoSmith] = None  # Name mangled

def _internal_helper():
    """Not part of public API"""
    ...
```

## Parameters
**Common parameter names:**
- `verbose: bool` - For output verbosity
- `exercise: GitAutograderExercise` - Exercise instance
- `repo: Repo` - Git repository
- `rs: RepoSmith` - RepoSmith instance
- `test: GitAutograderTest` - Test instance
- `output: GitAutograderOutput` - Verification output

## Examples from Codebase

```python
# Good naming throughout
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo_root = exercise.exercise_path
    repo_folder = exercise.config.exercise_repo.repo_name
    work_dir = os.path.join(repo_root, repo_folder)
    
    shopping_list_file_path = os.path.join(work_dir, "shopping-list.txt")
    if not os.path.exists(shopping_list_file_path):
        raise exercise.wrong_answer([SHOPPING_LIST_FILE_MISSING])
```
