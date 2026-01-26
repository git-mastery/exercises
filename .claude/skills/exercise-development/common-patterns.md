# common-patterns.md

## Setup Examples
See [grocery_shopping/download.py](../../grocery_shopping/download.py) for local repository setup.

See [fork_repo/download.py](../../fork_repo/download.py) for GitHub fork/clone pattern.

## Validation Examples
See [amateur_detective/verify.py](../../amateur_detective/verify.py) for answer-based validation.

See [grocery_shopping/verify.py](../../grocery_shopping/verify.py) for:
- File existence checks
- File content validation
- Commit validation

See [branch_compare/verify.py](../../branch_compare/verify.py) for branch validation.

See [tags_add/verify.py](../../tags_add/verify.py) for tag validation.

## Key Utilities
- `exercise_utils.git` - Git commands
- `exercise_utils.github_cli` - GitHub operations
- `exercise_utils.file` - File operations
- `exercise_utils.gitmastery` - Start tag creation

### With Tags

```python
from exercise_utils.git import tag
from exercise_utils.gitmastery import create_start_tag

def setup(verbose: bool = False):
    init(verbose)
    create_or_update_file("file.txt", "content")
    add(["file.txt"], verbose)
    commit("Initial commit", verbose)
    
    # Create Git-Mastery start tag
    create_start_tag(verbose)
    
    # Create version tags
    tag("v1.0.0", verbose)
```

## GitHub Integration Patterns

### Fork and Clone

```python
from exercise_utils.github_cli import (
    get_github_username,
    has_fork,
    fork_repo,
    get_fork_name,
    clone_repo_with_gh,
)

def setup(verbose: bool = False):
    username = get_github_username(verbose)
    owner = "git-mastery"
    repo_name = "exercise-base"
    
    # Check if fork exists
    if not has_fork(repo_name, owner, username, verbose):
        # Create fork
        fork_repo(
            f"{owner}/{repo_name}",
            f"{username}-{repo_name}",
            verbose,
            default_branch_only=True
        )
    
    # Get fork name and clone
    fork_name = get_fork_name(repo_name, owner, username, verbose)
    clone_repo_with_gh(f"{username}/{fork_name}", verbose, name=repo_name)
```

### Create and Clone Repository

```python
from exercise_utils.github_cli import create_repo, clone_repo_with_gh, delete_repo

def setup(verbose: bool = False):
    username = get_github_username(verbose)
    repo_name = "my-exercise"
    full_name = f"{username}/{repo_name}"
    
    # Clean up if exists
    if has_repo(full_name, is_fork=False, verbose=verbose):
        delete_repo(full_name, verbose)
    
    # Create new repository
    create_repo(repo_name, verbose)
    
    # Clone it
    clone_repo_with_gh(full_name, verbose, name=repo_name)
    
    # Navigate and setup
    os.chdir(repo_name)
    create_or_update_file("README.md", "# My Exercise")
    add(["README.md"], verbose)
    commit("Initial commit", verbose)
```

### Push to Remote

```python
from exercise_utils.git import add_remote, push

def setup(verbose: bool = False):
    username = get_github_username(verbose)
    repo_name = "my-repo"
    
    # Setup local repo
    init(verbose)
    create_or_update_file("README.md", "# Project")
    add(["README.md"], verbose)
    commit("Initial commit", verbose)
    
    # Add remote and push
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    add_remote("origin", remote_url, verbose)
    push("origin", "main", verbose)
```

## Validation Patterns

### Answer-Based Validation

```python
from git_autograder import GitAutograderExercise, GitAutograderOutput, GitAutograderStatus
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

QUESTION_ONE = "What is the answer?"
QUESTION_TWO = "What is another answer?"

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Validate answers
    (
        exercise.answers
        .add_validation(QUESTION_ONE, NotEmptyRule())
        .add_validation(QUESTION_ONE, HasExactValueRule("correct_answer"))
        .add_validation(QUESTION_TWO, NotEmptyRule())
        .add_validation(QUESTION_TWO, HasExactValueRule("another_answer"))
        .validate()
    )
    
    return exercise.to_output(
        ["Congratulations! You got it right!"],
        GitAutograderStatus.SUCCESSFUL
    )
```

### File Existence Check

```python
import os

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    repo_path = exercise.exercise_path
    repo_name = exercise.config.exercise_repo.repo_name
    work_dir = os.path.join(repo_path, repo_name)
    
    file_path = os.path.join(work_dir, "required-file.txt")
    if not os.path.exists(file_path):
        raise exercise.wrong_answer(["The required-file.txt is missing"])
    
    # File exists, continue validation
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

### File Content Validation

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    work_dir = os.path.join(
        exercise.exercise_path,
        exercise.config.exercise_repo.repo_name
    )
    
    file_path = os.path.join(work_dir, "data.txt")
    with open(file_path, "r") as f:
        content = f.read()
    
    # Parse content
    items = {line.strip() for line in content.splitlines() if line.strip()}
    
    # Validate
    if "required_item" not in items:
        raise exercise.wrong_answer(["Missing required item"])
    
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

### Commit Validation

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    main_branch = exercise.repo.branches.branch("main")
    
    # Check commits exist
    if not main_branch.user_commits:
        raise exercise.wrong_answer(["No commits found"])
    
    # Check specific file in last commit
    latest_commit = main_branch.latest_user_commit.commit
    if "file.txt" not in latest_commit.tree:
        raise exercise.wrong_answer(["file.txt not in latest commit"])
    
    # Read file from commit
    file_blob = latest_commit.tree / "file.txt"
    content = file_blob.data_stream.read().decode()
    
    if "expected_content" not in content:
        raise exercise.wrong_answer(["File doesn't contain expected content"])
    
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

### Branch Validation

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Check branch exists
    if not exercise.repo.branches.has_branch("feature"):
        raise exercise.wrong_answer(["Branch 'feature' doesn't exist"])
    
    feature_branch = exercise.repo.branches.branch("feature")
    main_branch = exercise.repo.branches.branch("main")
    
    # Check commits on branch
    if not feature_branch.user_commits:
        raise exercise.wrong_answer(["No commits on feature branch"])
    
    # Check if merged
    feature_commits = {c.commit.hexsha for c in feature_branch.user_commits}
    main_commits = {c.commit.hexsha for c in main_branch.user_commits}
    
    if not feature_commits.issubset(main_commits):
        raise exercise.wrong_answer(["Feature branch not merged into main"])
    
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

### Tag Validation

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Check tag exists
    tags = {tag.name for tag in exercise.repo.repo.tags}
    if "v1.0.0" not in tags:
        raise exercise.wrong_answer(["Tag 'v1.0.0' not found"])
    
    # Get tag
    tag = exercise.repo.repo.tags["v1.0.0"]
    
    # Check tag points to correct commit
    expected_commit = exercise.repo.branches.branch("main").latest_user_commit
    if tag.commit.hexsha != expected_commit.commit.hexsha:
        raise exercise.wrong_answer(["Tag on wrong commit"])
    
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

## File Operation Patterns

### Multi-line Content

```python
from exercise_utils.file import create_or_update_file

def setup(verbose: bool = False):
    create_or_update_file(
        "shopping-list.txt",
        """
        - Milk
        - Eggs
        - Bread
        - Apples
        """
    )
    # Content is auto-dedented
```

### Nested Directories

```python
def setup(verbose: bool = False):
    # Directories created automatically
    create_or_update_file("src/utils/helper.py", "def helper(): pass")
    create_or_update_file("tests/test_helper.py", "def test(): pass")
```

### Append Pattern

```python
from exercise_utils.file import append_to_file

def setup(verbose: bool = False):
    create_or_update_file("log.txt", "Initial entry\n")
    append_to_file("log.txt", "Second entry\n")
    append_to_file("log.txt", "Third entry\n")
```

## Error Handling Patterns

### Multiple Error Messages

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments = []
    
    if not condition_1:
        comments.append("Error 1")
    
    if not condition_2:
        comments.append("Error 2")
    
    if comments:
        raise exercise.wrong_answer(comments)
    
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

### Early Returns

```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Check critical requirement first
    if not os.path.exists(required_file):
        raise exercise.wrong_answer(["Critical file missing"])
    
    # Continue with other checks
    if not condition:
        raise exercise.wrong_answer(["Condition not met"])
    
    return exercise.to_output(["Success!"], GitAutograderStatus.SUCCESSFUL)
```

## Constants Pattern

```python
# Define at module level
QUESTION_ONE = "What is the answer?"
ERROR_FILE_MISSING = "The required file is missing"
ERROR_NOT_COMMITTED = "Changes not committed"
SUCCESS_MESSAGE = "Great work!"

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Use constants
    if not file_exists:
        raise exercise.wrong_answer([ERROR_FILE_MISSING])
    
    return exercise.to_output([SUCCESS_MESSAGE], GitAutograderStatus.SUCCESSFUL)
```
