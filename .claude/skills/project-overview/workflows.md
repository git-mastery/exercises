# Development Workflows

## Common Tasks

### Setup Development Environment
```bash
# One-time setup
./setup.sh

# This creates venv and installs dependencies
# Equivalent to:
python -m venv venv
source venv/bin/activate  # or venv/Scripts/activate on Windows
pip install -r requirements.txt
```

### Test an Exercise
```bash
# Test specific exercise
./test.sh <exercise_name>

# Example
./test.sh amateur_detective

# Runs: python -m pytest <exercise>/test_verify.py -s -vv
```

### Create New Exercise
```bash
# Use interactive scaffolding
./new.sh

# Prompts for:
# 1. Exercise name (kebab-case)
# 2. Tags (space-separated)
# 3. Exercise configuration

# Generates complete directory structure
```

### Run All Tests
```bash
# Test all exercises
pytest . -s -vv

# Test specific test function
pytest amateur_detective/test_verify.py::test_correct_answers -s -vv

# Stop at first failure
pytest . -x -s -vv
```

### Test Downloads
```bash
# Test all download.py scripts
./test-download.sh

# Verifies each download script executes without errors
```

### Code Quality Checks
```bash
# Format code
ruff format .

# Check linting
ruff check .

# Auto-fix issues
ruff check --fix .

# Type checking
mypy exercise_utils/
mypy <exercise_name>/

# Run all checks
ruff format . && ruff check . && mypy .
```

## Development Scripts

### `setup.sh`
**Purpose**: Initial environment setup

**What it does**:
- Creates Python virtual environment
- Activates the venv
- Installs all dependencies from requirements.txt

**When to use**: First time setup or after clean clone

### `test.sh <exercise_name>`
**Purpose**: Test specific exercise

**What it does**:
- Activates virtual environment
- Runs pytest on exercise's test_verify.py
- Shows verbose output (-s -vv flags)

**Example**:
```bash
./test.sh amateur_detective
./test.sh branch_bender
```

### `test-download.sh`
**Purpose**: Validate all download scripts

**What it does**:
- Tests each exercise's download.py
- Verifies scripts execute without errors
- Doesn't validate correctness, just execution

**When to use**: Before committing changes to download scripts

### `new.sh`
**Purpose**: Scaffold new exercise

**What it does**:
- Interactive prompts for exercise details
- Creates directory structure
- Generates template files:
  - `__init__.py`
  - `download.py`
  - `verify.py`
  - `test_verify.py`
  - `README.md`
  - `res/` directory

**When to use**: Starting a new exercise implementation

### `dump.sh`
**Purpose**: Development utility

**What it does**: Repository-specific utility (check source for details)

## Exercise Development Workflow

### Standard Exercise
```bash
# 1. Create exercise discussion issue on GitHub
# 2. Wait for approval
# 3. Request remote repository if needed

# 4. Generate scaffolding
./new.sh
# Enter: exercise-name, tags, config

# 5. Implement download.py
# - Setup repository state
# - Create start tag

# 6. Write README.md
# - Scenario and task
# - Progressive hints

# 7. Implement verify.py
# - Add validation rules
# - Return appropriate status

# 8. Write test_verify.py
# - Test all scenarios
# - No answers, wrong answers, correct answers

# 9. Test locally
./test.sh exercise-name

# 10. Verify quality
ruff format .
ruff check .
mypy exercise-name/

# 11. Commit and push
git add exercise-name/
git commit -m "Add exercise-name exercise"
git push
```

### Hands-On Script
```bash
# 1. Create file
touch hands_on/my_demo.py

# 2. Implement
# - Add __requires_git__ and __requires_github__
# - Implement download(verbose: bool)
# - Add helpful print statements

# 3. Test manually
python hands_on/my_demo.py

# 4. Verify created state
cd demo-repo  # or whatever it creates
git status
git log

# 5. Commit
git add hands_on/my_demo.py
git commit -m "Add my_demo hands-on script"
git push
```

## Testing Workflow

### Test-Driven Development
```bash
# 1. Write test_verify.py first
# - Define expected behavior
# - Test failure cases

# 2. Run tests (they fail)
./test.sh exercise-name

# 3. Implement verify.py
# - Make tests pass one by one

# 4. Refactor
# - Clean up code
# - Tests still pass
```

### Debugging Tests
```bash
# Run single test with full output
pytest exercise/test_verify.py::test_name -s -vv

# Add print statements in test
def test_something():
    output = test.run()
    print(f"Status: {output.status}")
    print(f"Messages: {output.messages}")
    assert_output(...)

# Run with Python debugger
pytest exercise/test_verify.py --pdb
```

## Git Workflow

### Branch Strategy
```bash
# Create feature branch
git checkout -b feature/new-exercise

# Make changes
# ... implement exercise ...

# Commit frequently
git add exercise-name/
git commit -m "Add download logic"

git add exercise-name/
git commit -m "Add verification rules"

# Push and create PR
git push origin feature/new-exercise
```

### Commit Messages
```bash
# Good commit messages
git commit -m "Add amateur_detective exercise"
git commit -m "Fix validation in branch_bender"
git commit -m "Update exercise_utils git module docs"

# Bad commit messages
git commit -m "updates"
git commit -m "fix"
git commit -m "wip"
```

## CI/CD Workflow

### What Runs on PR
1. All pytest tests
2. Ruff linting
3. Ruff formatting check
4. Type checking with mypy

### Pre-Push Checklist
```bash
# Run same checks as CI locally
./test.sh <exercise>           # Tests pass
ruff format .                   # Code formatted
ruff check .                    # No lint errors
mypy <exercise>/                # Type hints valid
```

## Troubleshooting Workflows

### Tests Failing Locally
```bash
# 1. Check Python environment
which python
python --version

# 2. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 3. Run single test with verbose output
pytest exercise/test_verify.py::test_name -s -vv

# 4. Check for import errors
python -c "from exercise_utils.git import add; print('OK')"
```

### Download Script Not Working
```bash
# 1. Test manually with verbose
python -c "from exercise.download import download; download(True)"

# 2. Check Git/GitHub CLI
git --version
gh auth status

# 3. Check working directory
pwd
ls -la
```

### Can't Run Scripts
```bash
# Make scripts executable (Linux/macOS)
chmod +x setup.sh test.sh new.sh

# Use sh/bash explicitly
bash setup.sh
bash test.sh amateur_detective
```

## Performance Tips

### Faster Testing
```bash
# Test only specific file
pytest amateur_detective/test_verify.py

# Run tests in parallel (requires pytest-xdist)
pytest -n auto

# Skip slow tests (if marked)
pytest -m "not slow"
```

### Faster Development
- Use pytest watch mode: `pytest-watch`
- Keep virtual environment activated
- Use IDE integration for testing
- Cache pip packages: `pip install --cache-dir=.cache`
