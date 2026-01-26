# Git-Mastery Exercises - AI Assistant Context

This repository contains modular Git exercises with automated validation. Each exercise teaches specific Git concepts through hands-on practice.

## Quick Start for AI Assistants

This project uses the **Agent Skills** standard for AI documentation. Detailed instructions are in `.claude/skills/`:

- **[project-overview](file:.claude/skills/project-overview/SKILL.md)**: Repository structure, architecture, and workflows
- **[exercise-development](file:.claude/skills/exercise-development/SKILL.md)**: Creating and modifying exercises
- **[exercise-utils](file:.claude/skills/exercise-utils/SKILL.md)**: Shared utility modules reference
- **[coding-standards](file:.claude/skills/coding-standards/SKILL.md)**: Code style and quality guidelines
- **[testing](file:.claude/skills/testing/SKILL.md)**: Testing patterns and best practices

## Repository Structure

```
exercises/
├── <exercise_name>/          # 40+ self-contained exercises
│   ├── download.py           # Setup logic
│   ├── verify.py             # Validation logic
│   ├── test_verify.py        # Pytest tests
│   ├── README.md             # Student instructions
│   └── res/                  # (Optional) Resources
├── hands_on/                 # Exploratory scripts (no validation)
├── exercise_utils/           # Shared utilities
│   ├── git.py                # Git command wrappers
│   ├── github_cli.py         # GitHub CLI wrappers
│   ├── cli.py                # General CLI helpers
│   ├── gitmastery.py         # Git-Mastery specific helpers
│   ├── file.py               # File operations
│   └── test.py               # Test scaffolding
├── .claude/skills/           # AI assistant documentation
├── setup.sh                  # Environment setup
├── test.sh                   # Test runner
└── requirements.txt          # Python dependencies
```

## Key Principles

1. **Use Shared Utilities**: Always use functions from `exercise_utils/` instead of raw subprocess calls
2. **Exercise Isolation**: Each exercise is completely independent and self-contained
3. **Composable Validation**: Use git-autograder's rule system for validation
4. **Comprehensive Testing**: Every exercise must have thorough test coverage
5. **Type Safety**: Use type hints for all functions

## Common Tasks

### Create New Exercise
```bash
./new.sh  # Interactive scaffolding
```

### Test Exercise
```bash
./test.sh <exercise_name>  # Runs pytest with verbose output
```

### Setup Environment
```bash
./setup.sh  # Creates venv and installs dependencies
```

## Tech Stack

- **Python**: 3.8+ (development on 3.13)
- **Testing**: pytest, git-autograder, repo-smith
- **Quality**: ruff (linting/formatting), mypy (type checking)
- **External**: Git CLI, GitHub CLI (gh)

## Development Workflow

1. Understand exercise requirements from issue/discussion
2. Use `./new.sh` to scaffold exercise structure
3. Implement `download.py` (setup), `verify.py` (validation), `README.md` (instructions)
4. Write comprehensive tests in `test_verify.py`
5. Run `./test.sh <exercise>` to verify
6. Ensure code passes: `ruff format . && ruff check . && mypy .`

## Documentation

- **Developer Guide**: https://git-mastery.github.io/developers
- **Exercise Directory**: https://git-mastery.github.io/exercises
- **Contributing**: [.github/CONTRIBUTING.md](.github/CONTRIBUTING.md)

## For More Details

Load the skills in `.claude/skills/` for comprehensive documentation on:
- Repository architecture and patterns
- Exercise development lifecycle
- Utility module API reference
- Coding standards and conventions
- Testing strategies and patterns

Each skill file follows the Agent Skills standard and provides detailed, actionable guidance for working with this repository.
