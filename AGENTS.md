# Git-Mastery Exercises - AI Agent Guide

This repository uses the **Agent Skills** standard for AI documentation. All detailed instructions are in `.claude/skills/`.

## For AI Agents

**Workflow**: 
1. Read this AGENTS.md to understand available skills
2. Based on your task, load relevant skills from `.claude/skills/`
3. Reference actual code files linked in skills

**Available skills**:
- **[project-overview](.claude/skills/project-overview/SKILL.md)**: Repository overview, structure, dependencies
- **[exercise-development](.claude/skills/exercise-development/SKILL.md)**: Creating exercises (standard vs hands-on)
- **[exercise-utils](.claude/skills/exercise-utils/SKILL.md)**: Utility modules API reference
- **[coding-standards](.claude/skills/coding-standards/SKILL.md)**: Code style, naming, type hints

**When to load each skill**:
- Creating/modifying exercises → `exercise-development`
- Using utility functions → `exercise-utils`
- Code review/formatting → `coding-standards`
- Understanding repo structure → `project-overview`

**Recommended workflow**:
- **Load only skills needed** for current task (don't load all 4 unnecessarily)
- **Read supporting docs** (*.md files) only when main SKILL.md references them
- **Verify example links** before using code patterns to ensure they match current implementation

**Skill dependencies**:
- **First time?** → Start with `project-overview`
- **Creating exercise?** → `exercise-development` (references `exercise-utils`, `coding-standards`)
- **Using utilities?** → `exercise-utils` (standalone)
- **Code review?** → `coding-standards` (standalone)

## For Human Developers

**Working with AI agents**: Simply state your task. AI will read AGENTS.md, identify needed skills, and load them automatically.

**Example tasks**:
```
"Create a new exercise about merge conflicts"

"Fix the test in amateur_detective/test_verify.py"

"Update grocery_shopping/download.py to use exercise_utils"

"Review this code against our standards"

"Review this code against coding-standards skill"
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

## Quick Reference

```bash
./setup.sh                    # Setup environment
./new.sh                      # Create exercise (interactive)
./test.sh <exercise>          # Test one exercise
pytest . -s -vv               # Test all
ruff format . && ruff check . # Format & lint
```

## Tech Stack

- Python 3.13+, pytest, git-autograder, repo-smith
- ruff (lint/format), mypy (types)
- Git CLI, GitHub CLI (gh)
