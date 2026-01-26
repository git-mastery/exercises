# best-practices.md

## DRY
Extract common logic into helpers.

## Error Handling
Use early returns and specific exceptions.

```python
def verify(exercise):
    if not os.path.exists(file_path):
        raise exercise.wrong_answer([FILE_MISSING])
    if not items:
        raise exercise.wrong_answer([NO_ITEMS])
    return exercise.to_output(["Success"], GitAutograderStatus.SUCCESSFUL)
```

## Function Design
- Single responsibility
- < 50 lines
- < 5 parameters
- Early returns

## Context Managers
```python
with open(filepath) as f:
    content = f.read()

with loader.start() as (test, rs):
    # test setup
    ...
```
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
