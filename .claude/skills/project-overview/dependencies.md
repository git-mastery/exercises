# Dependencies & Environment

## Python Requirements

### Version Support
- **Minimum**: Python 3.8
- **Recommended**: Python 3.13
- **Compatibility**: Code must work on 3.8+

## Core Dependencies

From `requirements.txt`:

### Functional Dependencies
```
git-autograder==6.*     # Exercise validation framework
PyYAML                  # YAML parsing
```

### Test Dependencies
```
pytest                  # Testing framework
repo-smith              # Repository state creation
```

### Developer Tools
```
ruff                    # Linting and formatting
mypy                    # Static type checking
PyGithub                # GitHub API interactions
requests                # HTTP library
types-requests          # Type stubs for requests
```

## External Requirements

### Required Tools
- **Git CLI**: Version 2.0+ recommended
  - Used by all exercises
  - Must be in system PATH
  
- **GitHub CLI (gh)**: Latest version
  - Required for exercises with `__requires_github__ = True`
  - Must be authenticated: `gh auth login`

### Operating System
- **Linux**: Fully supported
- **macOS**: Fully supported
- **Windows**: Supported (use Git Bash or WSL for shell scripts)

## Environment Setup

### Quick Setup
```bash
# Run provided script
./setup.sh
```

### Manual Setup
```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
# Linux/macOS:
source venv/bin/activate

# Windows:
source venv/Scripts/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### Verify Installation
```bash
# Check Python version
python --version  # Should be 3.8+

# Check Git
git --version

# Check GitHub CLI (if needed)
gh --version
gh auth status

# Run tests to verify setup
./test.sh amateur_detective
```

## Package Details

### git-autograder (v6.*)
**Purpose**: Exercise validation framework

**Key Components**:
- `GitAutograderExercise`: Exercise context
- `GitAutograderOutput`: Validation results
- `GitAutograderStatus`: Success/failure states
- Validation rules: `NotEmptyRule`, `HasExactValueRule`, etc.

**Usage**: Required for all `verify.py` implementations

### pytest
**Purpose**: Testing framework

**Usage**:
- All exercise tests in `test_verify.py`
- Run via `./test.sh <exercise_name>`
- Supports fixtures, parameterization, markers

### repo-smith
**Purpose**: Repository state creation for testing

**Key Components**:
- `RepoSmith`: Repository manipulation
- `Helper`: Base helper class
- Specification-based repo creation

**Usage**: Used in test setup and `exercise_utils/test.py`

### ruff
**Purpose**: Fast Python linter and formatter

**Usage**:
```bash
# Format code
ruff format .

# Check for issues
ruff check .

# Auto-fix issues
ruff check --fix .
```

**Configuration**: Follows Black defaults (88 char line length)

### mypy
**Purpose**: Static type checking

**Usage**:
```bash
# Type check specific module
mypy exercise_utils/

# Type check exercise
mypy amateur_detective/
```

**Configuration**: Requires type hints on all functions

## Dependency Management

### Updating Dependencies
```bash
# Update all packages
pip install -r requirements.txt --upgrade

# Update specific package
pip install --upgrade git-autograder
```

### Freezing Dependencies
```bash
# Generate locked requirements
pip freeze > requirements-lock.txt
```

### Checking for Issues
```bash
# Check for security vulnerabilities
pip audit

# Check for outdated packages
pip list --outdated
```

## Development Environment

### Recommended Setup
1. Python 3.13 with virtual environment
2. Git 2.40+ 
3. GitHub CLI 2.0+
4. VS Code or PyCharm
5. ruff and mypy installed globally or in venv

### Optional Tools
- **GitHub Desktop**: For visual Git operations
- **pytest-xdist**: Parallel test execution
- **pre-commit**: Git hooks for quality checks

## Common Issues

### Git Not Found
```bash
# Add Git to PATH or install
# Windows: Download from git-scm.com
# Linux: apt install git or yum install git
# macOS: brew install git
```

### GitHub CLI Not Authenticated
```bash
# Authenticate
gh auth login

# Follow prompts to login
```

### Wrong Python Version
```bash
# Use specific Python version
python3.13 -m venv venv
source venv/bin/activate
```

### Module Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```
