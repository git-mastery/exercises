# Git-Mastery Exercises - AI Agent Guide

This repository uses the **Agent Skills** standard for AI documentation. All detailed instructions are in `.claude/skills/`.

## For AI Agents

**Start here**: Load `.claude/skills/` to understand the repository.

Available skills:
- **[project-overview](file:.claude/skills/project-overview/SKILL.md)**: Repository overview, structure, dependencies
- **[exercise-development](file:.claude/skills/exercise-development/SKILL.md)**: Creating exercises (standard vs hands-on)
- **[exercise-utils](file:.claude/skills/exercise-utils/SKILL.md)**: Utility modules API reference
- **[coding-standards](file:.claude/skills/coding-standards/SKILL.md)**: Code style, naming, type hints

**What each skill tells you**:
- `project-overview`: 40+ exercises structure, exercise_utils/ modules, dependencies, common commands
- `exercise-development`: How to create standard exercises (download.py, verify.py, test_verify.py, README.md) and hands-on scripts
- `exercise-utils`: API docs for git.py, github_cli.py, cli.py, file.py, gitmastery.py, test.py modules
- `coding-standards`: ruff/mypy usage, naming conventions, type hints, imports, best practices

## For Human Developers

**When working with AI agents** (GitHub Copilot, Claude, etc.) **on this repository**:

### First Time Setup
1. Ask AI to "read the skills in .claude/skills/ directory"
2. AI will understand: repo structure, coding standards, testing patterns, utility APIs

### Common Workflows

**Creating a new exercise:**
```
"Create a new standard exercise called 'branch-merge-conflict' that teaches handling merge conflicts. 
Follow the patterns in .claude/skills/exercise-development/"
```

**Fixing a test:**
```
"Fix the failing test in amateur_detective/test_verify.py. 
Check .claude/skills/testing/ for test patterns."
```

**Using utility functions:**
```
"Update grocery_shopping/download.py to use exercise_utils functions. 
See .claude/skills/exercise-utils/ for available APIs."
```

**Code review:**
```
"Review this code against coding standards in .claude/skills/coding-standards/"
```

### What AI Knows From Skills

After loading skills, AI understands:
- **Structure**: Each exercise has download.py, verify.py, test_verify.py, README.md
- **Patterns**: Use `exercise_utils.*` instead of subprocess, call `create_start_tag()` last
- **Testing**: Required scenarios (no answers, wrong answers, success), `loader.start()` pattern
- **Standards**: 88-char lines, snake_case, type hints, import order
- **APIs**: All functions in exercise_utils/ (git.py, github_cli.py, etc.)

### Tips for Best Results

1. **Be specific about which skill**: "Follow exercise-development skill for creating download.py"
2. **Reference example files**: Skills already point to examples like [amateur_detective/test_verify.py](amateur_detective/test_verify.py)
3. **Check standards before committing**: "Does this follow coding-standards skill?"
4. **Use for learning**: "Explain the testing patterns from .claude/skills/testing/"

## Quick Reference

```bash
./setup.sh                    # Setup environment
./new.sh                      # Create exercise (interactive)
./test.sh <exercise>          # Test one exercise
pytest . -s -vv               # Test all
ruff format . && ruff check . # Format & lint
```

## Tech Stack

- Python 3.8+, pytest, git-autograder, repo-smith
- ruff (lint/format), mypy (types)
- Git CLI, GitHub CLI (gh)
