---
name: project-overview
description: High-level overview of the Git-Mastery exercises repository. Use when first learning about the project or need quick orientation.
user-invocable: false
---

# Git-Mastery Exercises Repository

## Overview
This repository contains 40+ modular, self-contained Git exercises designed to teach specific Git concepts through hands-on practice with automated validation.

## Repository Purpose
- **Education**: Teach Git concepts through practical, isolated exercises
- **Validation**: Automated testing of student solutions using pytest and git-autograder
- **Modularity**: Each exercise is completely self-contained and independent
- **Consistency**: Shared utilities ensure uniform patterns across all exercises

## Core Architecture

### 1. Exercise Types

#### Standard Exercises (40+ directories)
**Location**: Root directory (e.g., `amateur_detective/`, `branch_bender/`, `conflict_mediator/`)

**Purpose**: Guided exercises with specific objectives, instructions, and automated validation.

**Structure**:
```
<exercise_name>/
├── __init__.py           # Python package marker
├── download.py           # Setup logic - creates exercise repo state
├── verify.py             # Validation logic with verify() function
├── test_verify.py        # Pytest tests for verification logic
├── README.md             # Student-facing exercise instructions
└── res/                  # (Optional) Exercise-specific resources
```

**Key Characteristics**:
- Each exercise has a `download.py` that sets up the initial Git repository state
- `verify.py` contains composable validation rules using git-autograder
- `test_verify.py` uses pytest to test the verification logic
- Exercises may require Git only (`__requires_git__`) or both Git and GitHub (`__requires_github__`)
- Start tags are created using `create_start_tag()` from `exercise_utils/gitmastery.py`

**Example Exercises by Category**:
- **History/Investigation**: `amateur_detective/`, `view_commits/`, `log_and_order/`
- **Branching**: `branch_bender/`, `branch_delete/`, `branch_rename/`, `branch_forward/`, `bonsai_tree/`
- **Working Directory**: `sensors_checkout/`, `sensors_diff/`, `sensors_reset/`, `sensors_revert/`
- **Staging**: `staging_intervention/`, `stage_fright/`
- **Merging**: `conflict_mediator/`, `merge_squash/`, `merge_undo/`
- **Remotes**: `fetch_and_pull/`, `push_over/`, `clone_repo/`, `fork_repo/`, `remote_control/`
- **Tags**: `tags_add/`, `tags_push/`, `tags_update/`

#### Hands-On Scripts
**Location**: `hands_on/` directory

**Purpose**: Exploratory learning scripts that demonstrate Git operations without validation.

**Structure**:
```
hands_on/
├── add_files.py
├── branch_delete.py
├── create_branch.py
├── remote_branch_pull.py
└── ... (20+ standalone scripts)
```

**Key Characteristics**:
- Each file is a standalone Python script demonstrating a specific Git operation
- No `download.py`, `verify.py`, or `test_verify.py` files
- Users run scripts directly to observe Git behavior
- Ideal for experimentation and understanding command effects
- Scripts follow naming pattern: `<git_operation>.py`

### 2. Shared Utilities

**Location**: `exercise_utils/` directory

**Purpose**: Provide consistent, reusable wrappers for common operations across all exercises.

**Core Modules**:

#### `git.py`
- Wrappers for Git CLI commands
- Functions: `add()`, `commit()`, `empty_commit()`, `checkout()`, `merge()`, `tag()`, `init()`, `push()`, `clone_repo_with_git()`, `add_remote()`, `remove_remote()`, `track_remote_branch()`
- All functions accept `verbose: bool` parameter for output control

#### `github_cli.py`
- Wrappers for GitHub CLI (gh) commands
- Functions: `fork_repo()`, `clone_repo_with_gh()`, `delete_repo()`, `create_repo()`, `get_github_username()`, `has_repo()`
- Requires GitHub CLI to be installed and authenticated

#### `cli.py`
- General CLI execution helpers
- Functions: `run()`, `run_command()`, `run_command_no_exit()`
- Returns `CommandResult` dataclass with success status and output

#### `gitmastery.py`
- Git-Mastery specific utilities
- `create_start_tag(verbose: bool)`: Creates exercise start tag from first commit hash
- Tag format: `git-mastery-start-<first_commit_hash>`

#### `test.py`
- Test scaffolding for exercise verification
- `GitMasteryHelper`: Helper class extending repo-smith's Helper
- `GitAutograderTestLoader`: Loads and runs exercise tests
- `GitAutograderTest`: Test wrapper for exercise grading
- `assert_output()`: Assertion helper for validation output

#### `file.py`
- File operation helpers
- Functions for creating, updating, and appending to files consistently

### 3. Dependencies & Environment

**Python Version**: Python 3.8+ (primary development: Python 3.13)

**Core Dependencies** (from `requirements.txt`):
- **git-autograder** (v6.*): Exercise validation framework
- **repo-smith**: Repository state creation and manipulation
- **pytest**: Testing framework
- **PyYAML**: YAML parsing
- **PyGithub**: GitHub API interactions
- **requests**: HTTP library

**Developer Tools**:
- **ruff**: Python linter and formatter
- **mypy**: Static type checker

**External Requirements**:
- Git CLI (required for all exercises)
- GitHub CLI (`gh`) - required for exercises with `__requires_github__ = True`
- Bash environment (for shell scripts)

### 4. Development Workflow

#### Setup Environment
```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/macOS)
source venv/bin/activate

# Activate (Windows)
source venv/Scripts/activate

# Install dependencies
pip install -r requirements.txt
```

Or use the provided script:
```bash
./setup.sh
```

#### Testing Exercises
```bash
# Test specific exercise
./test.sh <exercise_name>

# Example
./test.sh amateur_detective

# This runs: python -m pytest <exercise_name>/test_verify.py -s -vv
```

#### Creating New Exercises
```bash
# Use scaffolding script
./new.sh

# You'll be prompted for:
# 1. Exercise name (kebab-case recommended)
# 2. Tags (space-separated)
# 3. Exercise configuration
```

The script generates the complete exercise structure with all required files.

#### Testing Downloads
```bash
# Test all exercise download scripts
./test-download.sh
```

### 5. Exercise Configuration

Each exercise has a `.gitmastery-exercise.json` file (not present in current structure but referenced in docs):
```json
{
  "exercise_name": "kebab-case-name",
  "tags": ["branch", "merge", "intermediate"]
}
```

### 6. Validation Patterns

Exercises use composable validation with git-autograder:

```python
from git_autograder import GitAutograderExercise, GitAutograderOutput
from git_autograder.answers.rules import HasExactValueRule, NotEmptyRule

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    exercise.answers.add_validation(QUESTION, NotEmptyRule())
    exercise.answers.add_validation(QUESTION, HasExactValueRule("expected"))
    exercise.answers.validate()
    
    return exercise.to_output(
        ["Success message"],
        GitAutograderStatus.SUCCESSFUL
    )
```

### 7. Test Patterns

Tests use `GitAutograderTestLoader` for standardized testing:

```python
from exercise_utils.test import GitAutograderTestLoader, assert_output

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

def test_something():
    with loader.start(mock_answers={QUESTION: "answer"}) as (test, _):
        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
            ["Expected message"]
        )
```

## Important Conventions

### File Organization
- **One exercise per directory**: No shared state between exercises
- **Self-contained resources**: All exercise resources in `res/` subdirectory
- **Standard naming**: Use kebab-case for exercise directories
- **Python packages**: Every exercise directory has `__init__.py`

### Git Operations
- **Use wrappers**: Always use `exercise_utils/git.py` functions, not direct subprocess calls
- **Start tags**: Create using `create_start_tag()` after repository setup
- **Verbose mode**: All utility functions support verbose parameter for debugging

### Testing
- **Test verification logic**: Every `verify.py` must have corresponding `test_verify.py`
- **Use test loader**: Leverage `GitAutograderTestLoader` for consistent test structure
- **Mock answers**: Test various scenarios with different mock answer combinations
- **Assertions**: Use `assert_output()` for standardized validation checking

### Code Quality
- **Type hints**: Use type annotations for all function parameters and returns
- **Docstrings**: Document all utility functions with clear descriptions
- **Error handling**: Wrap CLI operations with proper error handling
- **Consistency**: Follow patterns from existing exercises

## Project Integration

### Documentation
- **README.md**: Main project documentation (currently minimal)
- **summary.md**: Comprehensive repository structure documentation
- **.github/CONTRIBUTING.md**: Contributor guidelines with detailed setup instructions
- **.github/copilot-instructions.md**: AI assistant guidelines (for GitHub Copilot)

### CI/CD
- GitHub Actions workflows in `.github/workflows/`
- Automated testing via `ci.yml`

### Version Control
- **Don't modify**: `.git/`, `.github/`, top-level `README.md`, or scripts unless updating global logic
- **Exercise isolation**: Exercise logic stays in exercise directory
- **Shared improvements**: Common utilities go in `exercise_utils/`

## Quick Reference

### Common Tasks
- **Add new exercise**: `./new.sh`
- **Test exercise**: `./test.sh <exercise_name>`
- **Setup environment**: `./setup.sh`
- **Run single test**: `pytest <exercise>/test_verify.py::test_name -s -vv`

### Key Directories
- `exercise_utils/`: Shared utilities (git, github, cli, test helpers)
- `hands_on/`: Standalone demonstration scripts
- `.github/`: GitHub configuration and templates
- `test-downloads/`: Temporary directory for download testing

### External Documentation
- Developer docs: https://git-mastery.github.io/developers
- Exercise directory: https://git-mastery.github.io/exercises
- Git-Mastery app: https://git-mastery.github.io/app

## Working with This Repository

When modifying this repository:

1. **Understand exercise isolation**: Each exercise is completely independent
2. **Use shared utilities**: Leverage `exercise_utils/` for all Git/GitHub operations
3. **Test thoroughly**: Run `./test.sh <exercise>` after changes
4. **Follow patterns**: Match structure and style of existing exercises
5. **Document changes**: Update relevant documentation when adding features

## Additional Resources

For detailed information, see:
- [exercise-development](./exercise-development/SKILL.md) - Creating and modifying exercises
- [exercise-utils](./exercise-utils/SKILL.md) - Using shared utility modules
- [coding-standards](./coding-standards/SKILL.md) - Code style and quality guidelines
- [testing](./testing/SKILL.md) - Testing strategies and patterns
