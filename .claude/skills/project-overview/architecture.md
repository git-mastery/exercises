# Repository Architecture

## Exercise Structure

### Standard Exercise Anatomy
```
<exercise_name>/
├── __init__.py           # Python package marker
├── download.py           # Setup logic - creates exercise repo state
├── verify.py             # Validation logic with verify() function
├── test_verify.py        # Pytest tests for verification logic
├── README.md             # Student-facing exercise instructions
└── res/                  # (Optional) Exercise-specific resources
```

**Key Files**:

- **`download.py`**: Sets up initial Git repository state
  - Required variables: `__requires_git__`, `__requires_github__`
  - Required function: `def download(verbose: bool)`
  - Creates start tag using `create_start_tag()`

- **`verify.py`**: Validates student solutions
  - Required function: `def verify(exercise: GitAutograderExercise) -> GitAutograderOutput`
  - Uses composable validation rules from git-autograder
  - Returns success/failure status with messages

- **`test_verify.py`**: Tests the verification logic
  - Uses pytest and `GitAutograderTestLoader`
  - Tests multiple scenarios (no answers, wrong answers, correct answers)
  - Required constant: `REPOSITORY_NAME` matching directory name

- **`README.md`**: Student instructions
  - Scenario/context
  - Task description
  - Progressive hints

### Hands-On Script Anatomy
```
hands_on/
└── <operation>.py        # Single demonstration script
```

**Structure**:
- Required variables: `__requires_git__`, `__requires_github__`
- Required function: `def download(verbose: bool)`
- No validation, tests, or README
- Focus on demonstration and exploration

## Shared Utilities (`exercise_utils/`)

### Module Overview
- **`git.py`**: Git CLI command wrappers
- **`github_cli.py`**: GitHub CLI (gh) wrappers
- **`cli.py`**: General CLI execution helpers
- **`gitmastery.py`**: Git-Mastery specific utilities (start tags)
- **`file.py`**: File operation helpers
- **`test.py`**: Test scaffolding and helpers

### Design Patterns
All utility functions follow consistent patterns:
- Accept `verbose: bool` parameter for output control
- Use type hints for all parameters and returns
- Handle errors consistently (most exit on error)
- Return `CommandResult` or specific types

## Exercise Categories

### History & Investigation
- `amateur_detective/` - Uncover file changes with git status
- `view_commits/` - Exploring commit history
- `log_and_order/` - Understanding git log

### Branching
- `branch_bender/` - Creating and managing branches
- `branch_delete/` - Deleting branches safely
- `branch_rename/` - Renaming branches
- `branch_forward/` - Moving branch pointers
- `bonsai_tree/` - Complex branch structures

### Working Directory
- `sensors_checkout/` - Checking out commits
- `sensors_diff/` - Viewing differences
- `sensors_reset/` - Resetting changes
- `sensors_revert/` - Reverting commits

### Staging Area
- `staging_intervention/` - Managing staged changes
- `stage_fright/` - Understanding the staging area

### Merging
- `conflict_mediator/` - Resolving merge conflicts
- `merge_squash/` - Squash merging
- `merge_undo/` - Undoing merges

### Remotes & Collaboration
- `fetch_and_pull/` - Fetching and pulling changes
- `push_over/` - Pushing to remotes
- `clone_repo/` - Cloning repositories
- `fork_repo/` - Forking on GitHub
- `remote_control/` - Managing remotes

### Tags
- `tags_add/` - Creating tags
- `tags_push/` - Pushing tags
- `tags_update/` - Updating tags

## Integration Points

### External Tools Required
- **Git CLI**: Required for all exercises
- **GitHub CLI (gh)**: Required when `__requires_github__ = True`
- **Python 3.8+**: Runtime environment
- **Bash**: For shell scripts

### CI/CD Integration
- GitHub Actions workflows in `.github/workflows/`
- Automated testing on PR and merge
- Linting and formatting checks

## File Organization Principles

1. **Self-Contained**: Each exercise has all resources in its directory
2. **No Shared State**: Exercises are completely independent
3. **Standard Naming**: Use kebab-case for directories
4. **Python Packages**: Every exercise has `__init__.py`
5. **Resource Isolation**: Exercise-specific resources in `res/`
