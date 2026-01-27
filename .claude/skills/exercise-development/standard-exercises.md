# Creating Standard Exercises

This guide covers the complete process of creating a standard exercise with validation and testing.

## Prerequisites

Before implementing, you must:

1. **Create an exercise discussion issue**
   - Use GitHub issue template: "exercise discussion"
   - Include: exercise name, learning objectives, difficulty level, Git concepts covered
   - Tag with: `exercise discussion`, `help wanted`

2. **Obtain approval**
   - Wait for maintainer review and approval
   - Address any feedback on scope or approach

3. **Request remote repository** (if needed)
   - Use GitHub issue template: "request exercise repository"
   - Some exercises require pre-existing GitHub repositories

## Step 1: Scaffolding

Use the `new.sh` script to generate exercise structure:

```bash
./new.sh
```

**Prompts**:
1. **Exercise name**: Use kebab-case (e.g., `branch-forward`, `merge-squash`)
2. **Tags**: Space-separated (e.g., `branch merge intermediate`)
3. **Configuration**: Exercise-specific settings

**Generated files**:
```
<exercise-name>/
├── __init__.py
├── download.py
├── verify.py
├── test_verify.py
├── README.md
└── res/
```

## Step 2: Implement download.py

**Purpose**: Set up the initial Git repository state for the exercise.

### Required Function
```python
def setup(verbose: bool = False):
    """Setup the exercise repository."""
    # Implementation here
```

### Pattern: Local Repository Only
```python
import os
from exercise_utils.git import add, commit
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.file import create_or_update_file

def setup(verbose: bool = False):
    # Create initial files
    create_or_update_file("file1.txt", "Initial content")
    create_or_update_file("file2.txt", "More content")
    
    # Setup Git repository
    add(["file1.txt", "file2.txt"], verbose)
    commit("Initial commit", verbose)
    
    # Make changes for exercise
    create_or_update_file("file3.txt", "New file")
    
    # Create start tag (always last step)
    create_start_tag(verbose)
```

### Pattern: With GitHub Integration
```python
import os
from exercise_utils.git import clone_repo_with_git, checkout, add, commit, push
from exercise_utils.github_cli import get_github_username, fork_repo, delete_repo, has_repo
from exercise_utils.file import append_to_file

TARGET_REPO = "git-mastery/sample-repo"
FORK_NAME = "gitmastery-sample-repo"
LOCAL_DIR = "sample-repo"

def setup(verbose: bool = False):
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"
    
    # Clean up existing fork if present
    if has_repo(full_repo_name, True, verbose):
        delete_repo(full_repo_name, verbose)
    
    # Create fork
    fork_repo(TARGET_REPO, FORK_NAME, verbose, False)
    
    # Clone locally
    clone_repo_with_git(f"https://github.com/{full_repo_name}", verbose, LOCAL_DIR)
    os.chdir(LOCAL_DIR)
    
    # Make changes
    checkout("feature-branch", True, verbose)
    append_to_file("README.md", "\nNew content")
    add(["README.md"], verbose)
    commit("Update README", verbose)
    push("origin", "feature-branch", verbose)
```

### Best Practices
- Use utility functions from `exercise_utils/` - never raw subprocess calls
- Keep setup simple and focused on learning objectives
- Use verbose parameter for all utility calls

## Step 3: Write README.md

**Purpose**: Student-facing instructions for the exercise.

### Required Sections

1. **Title**: Exercise name (h1)
2. **Scenario/Context**: Engaging story that motivates the exercise
3. **Task**: Clear, actionable objectives
4. **Hints**: Progressive disclosure of help

### Template
```markdown
# exercise-name

## Scenario
[Engaging story or context that motivates the exercise.
Make it relatable and interesting.]

## Task
[Clear description of what students need to accomplish]

Use `git <command>` to [specific action].

[Additional requirements or constraints]

Update your answers in `answers.txt`.

## Hints

<details>
<summary>Hint 1</summary>

[First level of help - general guidance]

</details>

<details>
<summary>Hint 2</summary>

[Second level - more specific direction]

</details>

<details>
<summary>Hint 3</summary>

[Third level - nearly direct answer]

</details>
```

### Best Practices
- Use engaging scenarios that make Git concepts relatable
- Be specific about expected outcomes
- Provide 3-5 progressive hints
- Mention specific Git commands when appropriate
- Keep instructions concise and scannable

## Step 4: Implement verify.py

**Purpose**: Validate student's solution using composable rules.

### Required Imports
```python
from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule
# Import other rules as needed
```

### Required Function
```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    """Verify the student's solution."""
    # Validation logic here
```

### Pattern: Answer-Based Validation
For exercises where students provide answers in `answers.txt`:

```python
QUESTION_ONE = "Which file was modified?"
QUESTION_TWO = "Which commit was the change made in?"

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.answers.add_validation(QUESTION_ONE, NotEmptyRule())
        .add_validation(QUESTION_ONE, HasExactValueRule("expected_file.txt"))
        .add_validation(QUESTION_TWO, NotEmptyRule())
        .add_validation(QUESTION_TWO, HasExactValueRule("abc123"))
        .validate()
    )
    
    return exercise.to_output(
        ["Congratulations! You solved the exercise!"],
        GitAutograderStatus.SUCCESSFUL,
    )
```

### Pattern: Repository State Validation
For exercises checking Git repository state:

```python
from git_autograder.repo.rules import HasBranchRule, HasCommitWithMessageRule

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.repo.add_validation(HasBranchRule("feature-branch"))
        .add_validation(HasCommitWithMessageRule("Add new feature"))
        .validate()
    )
    
    return exercise.to_output(
        ["Great work! The repository is in the correct state."],
        GitAutograderStatus.SUCCESSFUL,
    )
```

### Validation Rule Categories
- **Answer rules**: `NotEmptyRule`, `HasExactValueRule`, `MatchesPatternRule`
- **Repository rules**: `HasBranchRule`, `HasCommitRule`, `HasRemoteRule`
- **Commit rules**: `HasCommitWithMessageRule`, `CommitCountRule`
- **File rules**: `FileExistsRule`, `FileContentsRule`

### Best Practices
- Chain validations using fluent API
- Provide clear, actionable success messages
- Use status codes appropriately (SUCCESSFUL, UNSUCCESSFUL)
- Test edge cases in your validation logic
- Keep validation focused on learning objectives

## Step 5: Write test_verify.py

**Purpose**: Test the verification logic with various scenarios.

### Required Imports
```python
from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder import GitAutograderStatus
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

from .verify import QUESTION_ONE, QUESTION_TWO, verify
```

### Required Setup
```python
REPOSITORY_NAME = "exercise-name"  # Must match exercise directory name

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)
```

### Required Test Scenarios

#### 1. No Answers
```python
def test_no_answers():
    """Test when student provides no answers."""
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
```

#### 2. Partial Answers
```python
def test_partial_answers():
    """Test when some answers missing."""
    with loader.start(
        mock_answers={QUESTION_ONE: "correct", QUESTION_TWO: ""}
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [NotEmptyRule.EMPTY.format(question=QUESTION_TWO)],
        )
```

#### 3. Wrong Answers
```python
def test_wrong_answers():
    """Test when answers are incorrect."""
    with loader.start(
        mock_answers={QUESTION_ONE: "wrong", QUESTION_TWO: "also_wrong"}
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
```

#### 4. Mixed Answers
```python
def test_mixed_answers():
    """Test mix of correct and incorrect answers."""
    with loader.start(
        mock_answers={QUESTION_ONE: "correct", QUESTION_TWO: "wrong"}
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )
```

#### 5. Correct Answers
```python
def test_correct_answers():
    """Test successful completion with all correct answers."""
    with loader.start(
        mock_answers={QUESTION_ONE: "correct", QUESTION_TWO: "also_correct"}
    ) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
            ["Congratulations! You solved the exercise!"],
        )
```

## Step 6: Add Resources (Optional)

**Location**: `res/` subdirectory within exercise

**Common resources**:
- Sample configuration files
- Pre-populated data files
- Scripts that students interact with
- Images or diagrams for README

**Accessing resources**:
```python
import os
from pathlib import Path

# In download.py
resource_dir = Path(__file__).parent / "res"
sample_file = resource_dir / "sample.txt"

# Copy to exercise directory
import shutil
shutil.copy(sample_file, ".")
```

## Testing Your Exercise

### Run Tests
```bash
./test.sh <exercise-name>
```

### Run Specific Test
```bash
pytest <exercise-name>/test_verify.py::test_correct_answers -s -vv
```

### Manual Testing
1. Run `download.py` to set up exercise
2. Follow instructions in `README.md`
3. Run `verify.py` to check solution
4. Verify success/failure messages are clear

## Troubleshooting

### Tests Failing
1. Run with verbose: `pytest <ex>/test_verify.py -s -vv`
2. Check mock answers match validation rules
3. Verify `REPOSITORY_NAME` matches directory name
4. Ensure imports are correct

### Download Script Errors
1. Check `__requires_git__` and `__requires_github__` flags
2. Verify Git/GitHub CLI is available
3. Test with verbose mode: `download(verbose=True)`
4. Check file paths are relative to exercise directory

### Validation Not Working
1. Verify validation rules match test expectations
2. Check that `validate()` is called on chain
3. Ensure correct status returned
4. Test with actual exercise setup

## Pre-Submission Checklist

- ✓ Exercise discussion approved
- ✓ All tests passing: `./test.sh <exercise-name>`
- ✓ Download script tested
- ✓ README clear and complete
- ✓ Code follows conventions
- ✓ No unused imports or files
- ✓ Quality checks pass: `ruff format . && ruff check . && mypy <exercise>/`
