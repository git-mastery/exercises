# best-practices.md

## DRY (Don't Repeat Yourself)

### Extract Common Logic

**Bad:**
```python
def fork_repo(repo_name: str, fork_name: str, verbose: bool):
    result = subprocess.run(["gh", "repo", "fork", repo_name], capture_output=True)
    if verbose:
        print(result.stdout)

def delete_repo(repo_name: str, verbose: bool):
    result = subprocess.run(["gh", "repo", "delete", repo_name], capture_output=True)
    if verbose:
        print(result.stdout)
```

**Good:**
```python
def run(command: List[str], verbose: bool) -> CommandResult:
    result = subprocess.run(command, capture_output=True)
    if verbose:
        print(result.stdout)
    return CommandResult(result)

def fork_repo(repo_name: str, fork_name: str, verbose: bool):
    run(["gh", "repo", "fork", repo_name], verbose)

def delete_repo(repo_name: str, verbose: bool):
    run(["gh", "repo", "delete", repo_name], verbose)
```

## Error Handling

### Early Returns

**Good:**
```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    if not os.path.exists(shopping_list_file_path):
        raise exercise.wrong_answer([SHOPPING_LIST_FILE_MISSING])
    
    if not added_items:
        comments.append(NO_ADD)
    
    if not deleted_items:
        comments.append(NO_REMOVE)
    
    if comments:
        raise exercise.wrong_answer(comments)
    
    return exercise.to_output(["Success"], GitAutograderStatus.SUCCESSFUL)
```

### Specific Exceptions

```python
try:
    result = subprocess.run(command, check=True)
except FileNotFoundError:
    # Handle missing command
    pass
except PermissionError:
    # Handle permission issues
    pass
except subprocess.CalledProcessError as e:
    # Handle command failure
    pass
```

## Composition Over Inheritance

### Prefer Helper Classes

**Good:**
```python
class GitMasteryHelper(Helper):
    def __init__(self, repo: Repo, verbose: bool) -> None:
        super().__init__(repo, verbose)
    
    def create_start_tag(self) -> None:
        # Specific functionality
        pass

# Usage
rs.add_helper(GitMasteryHelper)
rs.helper(GitMasteryHelper).create_start_tag()
```

## Function Design

### Single Responsibility

Each function should do **one thing**:

**Bad:**
```python
def setup_and_verify(exercise):
    # Setup
    create_files()
    init_repo()
    # Verify
    check_files()
    check_commits()
    return result
```

**Good:**
```python
def setup(exercise):
    create_files()
    init_repo()

def verify(exercise):
    check_files()
    check_commits()
    return result
```

### Small Functions

Keep functions short (< 50 lines ideally):

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    validate_file_exists(exercise)
    current_list = parse_shopping_list(exercise)
    changes = detect_changes(current_list)
    validate_changes(exercise, changes)
    return success_output(exercise)
```

### Clear Parameters

Limit parameters (< 5 preferred):

**OK:**
```python
def run(command: List[str], verbose: bool) -> CommandResult:
    ...
```

**Many params - consider config object:**
```python
# If you need many parameters:
@dataclass
class MergeConfig:
    target_branch: str
    ff: bool
    message: Optional[str]
    verbose: bool

def merge(config: MergeConfig) -> None:
    ...
```

## Variable Scope

### Keep Scope Small

```python
def verify(exercise):
    # Only define when needed
    repo_path = exercise.exercise_path
    
    if needs_shopping_list:
        # Define close to usage
        shopping_list_path = os.path.join(repo_path, "shopping-list.txt")
        with open(shopping_list_path) as f:
            content = f.read()
```

### Constants at Top

```python
# Module-level constants
QUESTION_ONE = "Which file was added?"
QUESTION_TWO = "Which file was edited?"
REPOSITORY_NAME = "amateur-detective"

def verify(exercise):
    # Use constants
    exercise.answers.add_validation(QUESTION_ONE, NotEmptyRule())
```

## Context Managers

### Use for Resource Management

```python
# File handling
with open(filepath, "r") as f:
    content = f.read()

# Test setup/teardown
with loader.start() as (test, rs):
    rs.files.create_or_update("file.txt", "content")
    output = test.run()
    # Automatic cleanup
```

### Custom Context Managers

```python
from contextlib import contextmanager

@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    with loader.start() as (test, rs):
        # Common setup
        rs.files.create_or_update("shopping-list.txt", initial_content)
        rs.git.add(["shopping-list.txt"])
        rs.git.commit(message="Initial commit")
        rs.helper(GitMasteryHelper).create_start_tag()
        
        yield test, rs
        # Automatic cleanup
```

## Data Structures

### Choose Appropriate Types

```python
# Sets for membership testing
ORIGINAL_SHOPPING_LIST = {"Milk", "Eggs", "Bread"}  # O(1) lookup

# Lists for ordered collections
commits = ["abc123", "def456", "ghi789"]

# Dicts for key-value lookups
mock_answers = {"question1": "answer1", "question2": "answer2"}
```

### Use dataclasses

```python
from dataclasses import dataclass

@dataclass
class CommandResult:
    result: CompletedProcess[str]
    
    def is_success(self) -> bool:
        return self.result.returncode == 0
    
    @property
    def stdout(self) -> str:
        return self.result.stdout.strip()
```

## Testing Best Practices

### One Assertion Per Test

**Good:**
```python
def test_no_answers():
    with loader.start(mock_answers={}) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL)

def test_wrong_answer():
    with loader.start(mock_answers={QUESTION: "wrong"}) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION)]
        )
```

### Descriptive Test Names

```python
# Good - describes what's being tested
def test_no_answers():
    ...

def test_incomplete_answer():
    ...

def test_wrong_question_one():
    ...

def test_valid_answers():
    ...
```

### Use Test Fixtures

```python
@contextmanager
def base_setup():
    """Common setup for all tests."""
    with loader.start() as (test, rs):
        # Setup
        yield test, rs

def test_case_one():
    with base_setup() as (test, rs):
        # Test-specific logic
        ...
```

## Performance Considerations

### Avoid Premature Optimization

- Write clear code first
- Optimize only when needed
- Profile before optimizing

### Use Comprehensions

```python
# Good
current_items = {line[2:].strip() for line in content.splitlines() if line.startswith("- ")}

# Instead of
current_items = set()
for line in content.splitlines():
    if line.startswith("- "):
        current_items.add(line[2:].strip())
```

## Code Smells to Avoid

❌ **Long functions** (> 50 lines)
❌ **Deep nesting** (> 3 levels)
❌ **Magic numbers** (use named constants)
❌ **Mutable defaults** (`def func(items=[]):` ❌)
❌ **Global state**
❌ **Commented-out code** (delete it)
❌ **Unclear variable names** (`x`, `tmp`, `data`)

## Security

### Command Injection

```python
# Good - list arguments
subprocess.run(["git", "commit", "-m", user_message], ...)

# Bad - shell=True with user input
subprocess.run(f"git commit -m '{user_message}'", shell=True)  # ❌
```

### Path Traversal

```python
# Validate paths
file_path = os.path.join(work_dir, filename)
if not file_path.startswith(work_dir):
    raise ValueError("Invalid file path")
```
