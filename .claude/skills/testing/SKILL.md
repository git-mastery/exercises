---
name: testing
description: Testing guidelines for exercises. Use when writing tests or debugging test failures.
---

# Testing

## Examples
See [amateur_detective/test_verify.py](../../amateur_detective/test_verify.py) - Answer-based tests.
See [grocery_shopping/test_verify.py](../../grocery_shopping/test_verify.py) - Repository state tests with fixtures.

## Basic Structure
```python
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus
from .verify import verify, QUESTION_ONE, ERROR_MESSAGE

loader = GitAutograderTestLoader("exercise-name", verify)

def test_success():
    with loader.start(mock_answers={QUESTION_ONE: "answer"}) as (test, rs):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)
```

## Required Test Scenarios

**Answer-Based:**
1. No answers (all empty)
2. Partial answers (some missing)
3. Wrong answers (test each question)
4. Valid answers (all correct)

**Repository State:**
1. No changes made
2. Partial completion (e.g., only added, not removed)
3. Wrong approach (e.g., changes not committed)
4. File missing/deleted
5. Valid submission

## Common Patterns

### Base Fixture (Repository State)
```python
from contextlib import contextmanager

@contextmanager
def base_setup():
    with loader.start() as (test, rs):
        rs.files.create_or_update("file.txt", "content")
        rs.git.add(["file.txt"])
        rs.git.commit(message="Initial")
        rs.helper(GitMasteryHelper).create_start_tag()
        yield test, rs
```

### Mock Answers (Answer-Based)
```python
def test_no_answers():
    with loader.start(mock_answers={}) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL)

def test_wrong_answer():
    with loader.start(mock_answers={Q1: "wrong"}) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [Q1_ERROR])
```

## RepoSmith (rs) APIs

**File Operations:**
- `rs.files.create_or_update(path, content)`
- `rs.files.append(path, content)`
- `rs.files.delete(path)`
- `rs.files.delete_lines(path, pattern)`

**Git Operations:**
- `rs.git.add(files)`, `rs.git.commit(message="msg")`
- `rs.git.checkout(branch, create=True)`
- `rs.git.merge(branch)`, `rs.git.tag(name)`

**Helper:**
- `rs.helper(GitMasteryHelper).create_start_tag()`

## Assertions
```python
# Success
assert_output(output, GitAutograderStatus.SUCCESSFUL, ["Congratulations!"])

# Failure with specific errors
assert_output(
    output,
    GitAutograderStatus.UNSUCCESSFUL,
    [ERROR_NO_ADD, ERROR_NO_REMOVE]
)
```

## Running Tests
```bash
pytest exercise_name/                    # Run exercise
pytest exercise/test_verify.py::test_x  # Specific test
pytest -s -vv                            # Verbose with output
pytest -x                                # Stop on first fail
pytest --lf                              # Run last failed
pytest -l                                # Show locals on fail
```

## Debug Techniques
```python
import pdb; pdb.set_trace()              # Breakpoint
print(f"Files: {os.listdir('.')}")       # Check state
print(f"Output: {output.comments}")      # Check output
```

### Test Independence
Each test should be independent - no shared state

### Clear Naming
```python
def test_no_answers_provided():
    pass

def test_all_correct_answers():
    pass
```

### Use Constants
```python
# Import from verify module
from .verify import QUESTION_ONE, QUESTION_TWO

# Don't hardcode
mock_answers = {QUESTION_ONE: "answer"}  # ✓
mock_answers = {"Which file?": "answer"}  # ✗
```

## Pre-Test Checklist

- ✓ All scenarios covered
- ✓ `REPOSITORY_NAME` matches directory
- ✓ Constants imported from verify.py
- ✓ Tests pass: `./test.sh <exercise>`
- ✓ Docstrings added
- ✓ No hardcoded values

## Related Skills

- **[exercise-development](../exercise-development/SKILL.md)** - Creating testable exercises
- **[exercise-utils](../exercise-utils/SKILL.md)** - Using test utilities
- **[coding-standards](../coding-standards/SKILL.md)** - Test code style
