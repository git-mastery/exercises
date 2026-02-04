---
name: exercise-development
description: Guidelines for creating and modifying Git-Mastery exercises. Use when developing new exercises, understanding exercise types, or following exercise patterns.
---

# Exercise Development

## Quick Guide

### Two Types of Content

**Standard Exercises**: Structured learning with validation (1-2 hours to create)
- Complete directory with download, verify, test, README
- Automated validation using git-autograder
- Comprehensive testing required

**Hands-On Scripts**: Quick demonstrations without validation (5-10 min to create)
- Single Python file in `hands_on/`
- No validation, tests, or README
- Focus on demonstration

## When to Use Each Type

| Use Standard Exercise When... | Use Hands-On Script When... |
|------------------------------|----------------------------|
| Need to assess understanding | Just demonstrating a concept |
| Have specific success criteria | Exploring open-ended scenarios |
| Want automated grading | Showing command effects |
| Building structured curriculum | Quick experimentation |

## Detailed Guides

### Standard Exercises
**[standard-exercises.md](standard-exercises.md)** - Complete guide to creating exercises with validation
- Proposal and approval process
- Scaffolding with `./new.sh`
- Implementing download.py, verify.py, test_verify.py, README.md
- Testing and troubleshooting

### Hands-On Scripts
**[hands-on-scripts.md](hands-on-scripts.md)** - Quick guide to creating demonstration scripts
- When and why to create
- Implementation steps
- Common patterns
- Examples

## Quick Start

### Create Standard Exercise
```bash
# 1. Get approval (create GitHub issue)
# 2. Generate scaffolding
./new.sh

# 3. Implement required files:
#    - download.py
#    - verify.py
#    - test_verify.py
#    - README.md

# 4. Test
./test.sh <exercise-name>

# 5. Quality check
ruff format . && ruff check . && mypy <exercise-name>/
```

### Create Hands-On Script
```bash
# Use scaffolding
./new.sh
# Choose "hands-on"

# Implement download(verbose: bool) function
# Test manually
python hands_on/<script_name>.py
```

## Exercise Conventions

### Naming
- **Directories**: kebab-case (`branch-forward`, `conflict-mediator`)
- **Files**: snake_case (`download.py`, `test_verify.py`)
- **Constants**: UPPER_SNAKE_CASE (`QUESTION_ONE`, `REPOSITORY_NAME`)

### Required Elements (Standard Exercises)
- `__init__.py` - Package marker
- `.gitmastery-exercise.json` - Configuration
- `download.py` - `setup(verbose: bool = False)`
- `verify.py` - With `verify()` function
- `test_verify.py` - With `REPOSITORY_NAME` and test functions
- `README.md` - With scenario, task, hints

### Required Elements (Hands-On)
- `__requires_git__` and `__requires_github__` variables
- `download(verbose: bool)` function

## Examples

### Standard Exercise Examples
- **Simple**: `amateur_detective/` - Answer validation
- **Branching**: `branch_bender/` - Branch operations
- **Remote**: `remote_control/` - GitHub integration
- **Complex**: `conflict_mediator/` - Merge conflicts

### Hands-On Examples
- `hands_on/add_files.py` - Staging demonstration
- `hands_on/branch_delete.py` - Branch deletion
- `hands_on/remote_branch_pull.py` - Remote operations

## Related Skills

- **[exercise-utils](../exercise-utils/SKILL.md)** - Utility functions reference
