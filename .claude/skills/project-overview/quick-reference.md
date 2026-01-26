# Quick Reference

## Essential Commands

```bash
# Setup
./setup.sh                           # Create venv and install deps

# Testing
./test.sh <exercise>                 # Test specific exercise
pytest . -s -vv                      # Test all exercises
pytest <ex>/test_verify.py::test_name  # Test specific function

# Quality
ruff format .                        # Format code
ruff check .                         # Check linting
ruff check --fix .                   # Auto-fix issues
mypy <directory>/                    # Type checking

# Development
./new.sh                             # Create new exercise
./test-download.sh                   # Test all downloads
```

## Directory Structure Quick Map

```
exercises/
├── amateur_detective/         # Example standard exercise
│   ├── __init__.py
│   ├── download.py           # Setup logic
│   ├── verify.py             # Validation
│   ├── test_verify.py        # Tests
│   ├── README.md             # Instructions
│   └── res/                  # Resources
│
├── hands_on/                  # Demonstration scripts
│   ├── add_files.py
│   ├── branch_delete.py
│   └── ...
│
├── exercise_utils/            # Shared utilities
│   ├── git.py                # Git wrappers
│   ├── github_cli.py         # GitHub wrappers
│   ├── cli.py                # CLI helpers
│   ├── gitmastery.py         # Start tags
│   ├── file.py               # File ops
│   └── test.py               # Test helpers
│
├── .claude/skills/            # AI documentation
├── .github/                   # CI/CD
├── setup.sh                   # Setup script
├── test.sh                    # Test script
├── new.sh                     # Scaffolding script
├── requirements.txt           # Dependencies
└── CLAUDE.md                  # AI context entry
```

## File Purposes

| File | Purpose | Required |
|------|---------|----------|
| `__init__.py` | Python package marker | Yes (exercises) |
| `download.py` | Exercise setup | Yes (exercises) |
| `verify.py` | Solution validation | Yes (exercises) |
| `test_verify.py` | Tests for validation | Yes (exercises) |
| `README.md` | Student instructions | Yes (exercises) |
| `res/` | Exercise resources | Optional |

## Common Import Patterns

```python
# Git operations
from exercise_utils.git import init, add, commit, checkout, merge

# GitHub operations
from exercise_utils.github_cli import fork_repo, get_github_username

# File operations
from exercise_utils.file import create_or_update_file, append_to_file

# Git-Mastery specific
from exercise_utils.gitmastery import create_start_tag

# Testing
from exercise_utils.test import GitAutograderTestLoader, assert_output

# Validation
from git_autograder import GitAutograderExercise, GitAutograderOutput
from git_autograder.answers.rules import NotEmptyRule, HasExactValueRule
```

## Required Variables

### In download.py or hands_on scripts
```python
__requires_git__ = True      # Always set this
__requires_github__ = False  # True if uses GitHub CLI
```

### In test_verify.py
```python
REPOSITORY_NAME = "exercise-name"  # Must match directory name exactly
```

## Validation Patterns

### Basic Answer Validation
```python
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    (
        exercise.answers
        .add_validation(QUESTION, NotEmptyRule())
        .add_validation(QUESTION, HasExactValueRule("expected"))
        .validate()
    )
    return exercise.to_output(
        ["Success message"],
        GitAutograderStatus.SUCCESSFUL
    )
```

### Test Pattern
```python
def test_correct():
    with loader.start(mock_answers={QUESTION: "answer"}) as (test, _):
        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL, ["Success"])
```

## Key Conventions

### Naming
- **Directories**: kebab-case (`branch-forward`, `amateur-detective`)
- **Functions**: snake_case (`verify`, `download`, `create_start_tag`)
- **Constants**: UPPER_SNAKE_CASE (`QUESTION_ONE`, `REPOSITORY_NAME`)
- **Classes**: PascalCase (`GitMasteryHelper`, `ExerciseValidator`)

### Exercise Setup Pattern
```python
def setup(verbose: bool = False):
    # 1. Create files
    create_or_update_file("file.txt", "content")
    
    # 2. Initialize Git
    init(verbose)
    add(["file.txt"], verbose)
    commit("Initial commit", verbose)
    
    # 3. Make changes for exercise
    # ... exercise-specific setup ...
    
    # 4. Create start tag (ALWAYS LAST)
    create_start_tag(verbose)
```

### Hands-On Script Pattern
```python
def download(verbose: bool):
    # 1. Setup demo environment
    os.makedirs("demo-repo")
    os.chdir("demo-repo")
    
    # 2. Demonstrate operation
    init(verbose)
    # ... demo-specific operations ...
    
    # 3. Guide user
    if verbose:
        print("\n✓ Demo complete")
        print("Try running: git log")
```

## Common Pitfalls

### ❌ Don't Do
```python
# Raw subprocess calls
import subprocess
subprocess.run(["git", "add", "file.txt"])

# Hardcoded values
exercise.answers.add_validation("Which file?", ...)

# Missing type hints
def verify(exercise):
    pass

# Wrong directory name
REPOSITORY_NAME = "amateur_detective"  # Should be "amateur-detective"
```

### ✅ Do This
```python
# Use utility wrappers
from exercise_utils.git import add
add(["file.txt"], verbose)

# Use constants
QUESTION_ONE = "Which file?"
exercise.answers.add_validation(QUESTION_ONE, ...)

# Include type hints
def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    pass

# Match directory name exactly
REPOSITORY_NAME = "amateur-detective"
```

## Debugging Quick Tips

```bash
# Verbose test output
pytest <ex>/test_verify.py -s -vv

# Run single test
pytest <ex>/test_verify.py::test_name -s -vv

# Python debugger
pytest <ex>/test_verify.py --pdb

# Check imports
python -c "from exercise_utils.git import add; print('OK')"

# Test download manually
python -c "from <ex>.download import download; download(True)"

# Check Git/GitHub CLI
git --version
gh auth status
```

## Status Codes

```python
from git_autograder import GitAutograderStatus

GitAutograderStatus.SUCCESSFUL     # All validations passed
GitAutograderStatus.UNSUCCESSFUL   # Some validations failed
```

## Useful Links

- **Project**: [README.md](../../../README.md)
- **Contributing**: [.github/CONTRIBUTING.md](../../../.github/CONTRIBUTING.md)
- **Developer Docs**: https://git-mastery.github.io/developers
- **Exercise Directory**: https://git-mastery.github.io/exercises

## Need More Help?

- **Architecture details**: [architecture.md](architecture.md)
- **Dependencies & setup**: [dependencies.md](dependencies.md)
- **Development workflows**: [workflows.md](workflows.md)
- **Exercise development**: [../exercise-development/SKILL.md](../exercise-development/SKILL.md)
- **Utility reference**: [../exercise-utils/SKILL.md](../exercise-utils/SKILL.md)
- **Coding standards**: [../coding-standards/SKILL.md](../coding-standards/SKILL.md)
- **Testing guide**: [../testing/SKILL.md](../testing/SKILL.md)
