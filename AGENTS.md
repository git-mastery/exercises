# Git-Mastery Exercises - AI Agent Guide

## Repository Structure

40+ modular Git exercises with automated validation using pytest and git-autograder.

**Exercise types:**
- **Standard exercises** (40+ directories): Complete with download.py, verify.py, test_verify.py, README.md, res/
- **Hands-on scripts** (hands_on/): Single-file demonstrations without validation

**Shared utilities** (exercise_utils/): git.py, github_cli.py, cli.py, file.py, gitmastery.py, test.py

## Available Skills

**[exercise-development](.claude/skills/exercise-development/SKILL.md)**: Creating exercises (standard vs hands-on)
- References: exercise-utils, coding standards
- Use for: implementing download.py, verify.py, test_verify.py, README.md

**[exercise-utils](.claude/skills/exercise-utils/SKILL.md)**: Utility modules API reference
- Standalone: git, github_cli, cli, file, gitmastery, test utilities
- Never use raw subprocess calls

## Quick Commands

```bash
./new.sh                      # Create exercise/hands-on (interactive)
./test.sh <exercise>          # Test one exercise
pytest . -s -vv               # Test all
ruff format . && ruff check . # Format & lint
```

## Coding Standards

**Style**: 88 char lines, 4 spaces, double quotes, 2 blank lines between functions

**Naming**:
- Functions/Variables: snake_case
- Constants: UPPER_SNAKE_CASE
- Classes: PascalCase
- Directories: kebab-case

**Type hints**: Required on all function signatures

**Imports**: Order: stdlib, third-party, local (blank lines between)

**Common mistakes**:
- Don't call git directly, use exercise_utils/git.py
- Don't forget create_start_tag() at end of download.py
- Don't hardcode paths, use Path(__file__).parent
- Don't create tests without test_ prefix

**Pre-commit**: Run ruff format, ruff check, mypy, and ./test.sh

## Contributing Workflow

1. Create "exercise discussion" GitHub issue
2. Wait for approval
3. Use ./new.sh to scaffold
4. Implement files
5. Test thoroughly
6. Submit PR referencing approved issue

## Tech Stack

Python 3.13+, pytest, git-autograder 6.*, repo-smith, ruff, mypy, Git CLI, GitHub CLI (gh)
