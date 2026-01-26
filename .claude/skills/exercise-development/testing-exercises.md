# testing-exercises.md

## Examples
See [amateur_detective/test_verify.py](../../amateur_detective/test_verify.py) - Answer-based exercise tests.

See [grocery_shopping/test_verify.py](../../grocery_shopping/test_verify.py) - Repository state tests with base fixture.

See [view_commits/test_verify.py](../../view_commits/test_verify.py) - Multiple question exercise.

## Minimum Tests
1. Success case
2. No action
3. Wrong approach  
4. Each error message

## Running
```bash
pytest exercise_name/
```

## Answer-Based Exercise Tests

```python
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule
from .verify import QUESTION_ONE, QUESTION_TWO


def test_no_answers():
    with loader.start(mock_answers={QUESTION_ONE: "", QUESTION_TWO: ""}) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                NotEmptyRule.EMPTY.format(question=QUESTION_ONE),
                NotEmptyRule.EMPTY.format(question=QUESTION_TWO),
            ],
        )


def test_wrong_answers():
    with loader.start(
        mock_answers={QUESTION_ONE: "wrong", QUESTION_TWO: "wrong"}
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE),
                HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO),
            ],
        )


def test_correct_answers():
    with loader.start(
        mock_answers={QUESTION_ONE: "correct1", QUESTION_TWO: "correct2"}
    ) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)
```

## Repository State Exercise Tests

### With Base Setup Fixture

```python
from contextlib import contextmanager
from typing import Iterator, Tuple
from exercise_utils.test import GitAutograderTest, GitMasteryHelper
from repo_smith.repo_smith import RepoSmith


@contextmanager
def base_setup() -> Iterator[Tuple[GitAutograderTest, RepoSmith]]:
    """Common setup for all tests."""
    with loader.start() as (test, rs):
        # Initial repository state
        rs.files.create_or_update("file.txt", "initial")
        rs.git.add(["file.txt"])
        rs.git.commit(message="Initial commit")
        rs.helper(GitMasteryHelper).create_start_tag()
        
        yield test, rs


def test_no_changes():
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_CHANGES])


def test_success():
    with base_setup() as (test, rs):
        rs.files.append("file.txt", "new content")
        rs.git.add(["file.txt"])
        rs.git.commit(message="Add content")
        
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)
```

## Testing File Operations

```python
def test_file_missing():
    with base_setup() as (test, rs):
        rs.files.delete("required-file.txt")
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            ["File missing error"]
        )


def test_file_content_wrong():
    with base_setup() as (test, rs):
        rs.files.create_or_update("file.txt", "wrong content")
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            ["Content error"]
        )
```

## Testing Git Operations

```python
def test_not_committed():
    with base_setup() as (test, rs):
        rs.files.append("file.txt", "new content")
        # Missing: git add and commit
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            ["Not committed error"]
        )


def test_branch_missing():
    with base_setup() as (test, rs):
        # Expected branch doesn't exist
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            ["Branch missing error"]
        )


def test_branch_exists():
    with base_setup() as (test, rs):
        rs.git.checkout("feature", create=True)
        rs.files.create_or_update("feature.txt", "content")
        rs.git.add(["feature.txt"])
        rs.git.commit(message="Add feature")
        rs.git.checkout("main")
        
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)
```

## Running Exercise Tests

```bash
# Run all tests for exercise
pytest my_exercise/

# Run specific test
pytest my_exercise/test_verify.py::test_base

# Verbose output
pytest -vv my_exercise/

# Show print statements
pytest -s my_exercise/
```

See [running-tests.md](../../testing/running-tests.md) for detailed testing commands.

## Test Coverage Requirements

- **100% coverage** of verify.py
- **All error messages** must have tests
- **All validation paths** must be tested
- **Edge cases** should be covered

## Common Mistakes

### ❌ Not Testing All Errors

```python
# Missing test for ERROR_2
def test_only_one_error():
    # Tests ERROR_1 but not ERROR_2
    ...
```

### ❌ Not Using Base Setup

```python
# Duplicated setup in every test
def test_1():
    with loader.start() as (test, rs):
        rs.files.create_or_update("file.txt", "content")  # Repeated
        rs.git.add(["file.txt"])  # Repeated
        rs.git.commit(message="Initial")  # Repeated
        ...
```

### ❌ Not Creating Start Tag

```python
# Missing start tag for exercises that need it
def test_without_start_tag():
    with loader.start() as (test, rs):
        rs.files.create_or_update("file.txt", "content")
        rs.git.add(["file.txt"])
        rs.git.commit(message="Commit")
        # Missing: rs.helper(GitMasteryHelper).create_start_tag()
        ...
```

### ❌ Forgetting to Stage Files

```python
def test_commit_without_staging():
    with loader.start() as (test, rs):
        rs.files.create_or_update("file.txt", "content")
        # Missing: rs.git.add(["file.txt"])
        rs.git.commit(message="Commit")  # This will fail!
```

## Debugging Test Failures

### Print Repository State

```python
def test_debug():
    with loader.start() as (test, rs):
        rs.files.create_or_update("file.txt", "content")
        
        # Debug output (run with: pytest -s)
        import os
        print(f"Files: {os.listdir('.')}")
        print(f"Content: {open('file.txt').read()}")
        
        output = test.run()
        print(f"Status: {output.status}")
        print(f"Comments: {output.comments}")
```

### Use Debugger

```python
def test_with_debugger():
    with loader.start() as (test, rs):
        import pdb; pdb.set_trace()
        # Step through test
        output = test.run()
```

## Test Documentation

Document test purpose with docstrings:

```python
def test_no_changes():
    """Test that exercise fails when student makes no changes."""
    with base_setup() as (test, rs):
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_CHANGES])


def test_partial_completion():
    """Test that exercise fails when only some requirements are met."""
    with base_setup() as (test, rs):
        rs.files.append("file.txt", "partial")
        # Missing commit step
        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_COMMITTED])
```

## Complete Test File Example

See existing exercises for complete examples:
- [amateur_detective/test_verify.py](../../amateur_detective/test_verify.py) - Answer-based exercise
- [grocery_shopping/test_verify.py](../../grocery_shopping/test_verify.py) - Repository state exercise with fixture
- [view_commits/test_verify.py](../../view_commits/test_verify.py) - Multiple question exercise
