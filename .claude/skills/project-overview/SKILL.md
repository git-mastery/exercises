---
name: project-overview
description: Overview of Git-Mastery exercises repository. Use when first learning about the project.
user-invocable: false
---

# Git-Mastery Exercises

## Overview
40+ modular Git exercises with automated validation using pytest and git-autograder.

## Exercise Types

### Standard Exercises (40+ directories)
```
<exercise_name>/
├── download.py           # Setup logic
├── verify.py             # Validation with git-autograder
├── test_verify.py        # Pytest tests
├── README.md             # Instructions
└── res/                  # Optional resources
```

**Categories**:
- History: `amateur_detective/`, `view_commits/`
- Branching: `branch_bender/`, `branch_delete/`, `bonsai_tree/`
- Working Dir: `sensors_checkout/`, `sensors_diff/`, `sensors_reset/`
- Staging: `staging_intervention/`, `stage_fright/`
- Merging: `conflict_mediator/`, `merge_squash/`
- Remotes: `fetch_and_pull/`, `push_over/`, `fork_repo/`
- Tags: `tags_add/`, `tags_push/`

### Hands-On Scripts (`hands_on/`)
Single-file demonstrations without validation. Examples: `add_files.py`, `branch_delete.py`.

## Shared Utilities (`exercise_utils/`)
- **git.py**: Git command wrappers
- **github_cli.py**: GitHub CLI wrappers
- **cli.py**: CLI execution helpers
- **gitmastery.py**: Start tag creation
- **test.py**: Test scaffolding
- **file.py**: File operations

## Dependencies
- Python 3.8+
- git-autograder 6.*, repo-smith, pytest
- ruff, mypy (dev tools)
- Git CLI, GitHub CLI (gh)

## Common Commands
```bash
./setup.sh                       # Setup venv
./test.sh <exercise>             # Test exercise
pytest . -s -vv                  # Test all
ruff format . && ruff check .    # Format & lint
./new.sh                         # Create exercise
```
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
