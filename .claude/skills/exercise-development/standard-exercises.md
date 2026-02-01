# Creating Standard Exercises

This guide covers the complete process of creating a standard exercise with validation and testing.

## Prerequisites

Before implementing, you must:

1. **Create an exercise discussion issue**
   - Use GitHub issue template: "exercise discussion"
   - Include: exercise name, learning objectives, difficulty level, Git concepts covered
   - Tag with: `exercise discussion`, `help wanted`

2. **Obtain approval**
   - Wait for maintainer review and approval
   - Address any feedback on scope or approach

3. **Request remote repository** (if needed)
   - Use GitHub issue template: "request exercise repository"
   - Some exercises require pre-existing GitHub repositories

## Step 1: Scaffolding

Use the `new.sh` script to generate exercise structure:

```bash
./new.sh
```

**Prompts**:
1. **Exercise name**: Use kebab-case (e.g., `branch-forward`, `merge-squash`)
2. **Tags**: Space-separated (e.g., `branch merge intermediate`)
3. **Configuration**: Exercise-specific settings

**Generated files**:
```
<exercise-name>/
├── __init__.py
├── download.py
├── verify.py
├── test_verify.py
├── README.md
└── res/
```

## Step 2: Implement download.py

**Purpose**: Set up the initial Git repository state for the exercise.

**Examples**:
- Local repo: See [grocery_shopping/download.py](../../../grocery_shopping/download.py)
- GitHub integration: See [fork_repo/download.py](../../../fork_repo/download.py)

**Required function**: `def setup(verbose: bool = False)`

**Key points**:
- Use utility functions from `exercise_utils/` - never raw subprocess calls
- Always call `create_start_tag()` as the final step
- Keep setup simple and focused on learning objectives
- Use verbose parameter for all utility calls

## Step 3: Write README.md

**Purpose**: Student-facing instructions for the exercise.

**Examples**: See any exercise README like [amateur_detective/README.md](../../../amateur_detective/README.md)

**Required sections**:
1. **Title**: Exercise name (h1)
2. **Scenario/Context**: Engaging story that motivates the exercise
3. **Task**: Clear, actionable objectives
4. **Hints**: Progressive disclosure of help (3-5 hints in collapsible details)

**Best practices**:
- Use engaging scenarios that make Git concepts relatable
- Be specific about expected outcomes
- Mention specific Git commands when appropriate
- Keep instructions concise and scannable

## Step 4: Implement verify.py

**Purpose**: Validate student's solution using composable rules.

**Examples**:
- Answer-based: See [amateur_detective/verify.py](../../../amateur_detective/verify.py)
- Repository state: See [grocery_shopping/verify.py](../../../grocery_shopping/verify.py)
- Branch validation: See [branch_compare/verify.py](../../../branch_compare/verify.py)

**Required function**: `def verify(exercise: GitAutograderExercise) -> GitAutograderOutput`

**Validation rule categories**:
- **Answer rules**: `NotEmptyRule`, `HasExactValueRule`, `MatchesPatternRule`
- **Repository rules**: `HasBranchRule`, `HasCommitRule`, `HasRemoteRule`
- **Commit rules**: `HasCommitWithMessageRule`, `CommitCountRule`
- **File rules**: `FileExistsRule`, `FileContentsRule`

**Best practices**:
- Chain validations using fluent API
- Provide clear, actionable success messages
- Use status codes appropriately (SUCCESSFUL, UNSUCCESSFUL)
- Keep validation focused on learning objectives

## Step 5: Write test_verify.py

**Purpose**: Test the verification logic with various scenarios.

**Examples**:
- Answer-based: See [amateur_detective/test_verify.py](../../../amateur_detective/test_verify.py)
- Repository state: See [grocery_shopping/test_verify.py](../../../grocery_shopping/test_verify.py)

**Required setup**:
- `REPOSITORY_NAME = "exercise-name"` (must match directory)
- `loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)`

**Required test scenarios**:
1. No answers/changes
2. Partial answers/completion
3. Wrong answers/approach
4. Mixed (some correct, some wrong)
5. All correct

**Pattern**: Use `loader.start(mock_answers={...})` context manager, then `test.run()` and `assert_output()`

## Step 6: Add Resources (Optional)

**Location**: `res/` subdirectory within exercise

**Common resources**:
- Sample configuration files
- Pre-populated data files
- Scripts that students interact with
- Images or diagrams for README

**Accessing**: Use `Path(__file__).parent / "res"` to get resource directory

## Testing Your Exercise

### Run Tests
```bash
./test.sh <exercise-name>
pytest <exercise-name>/test_verify.py::test_name -s -vv
```

### Manual Testing
1. Run `download.py` to set up exercise
2. Follow instructions in `README.md`
3. Run `verify.py` to check solution
4. Verify success/failure messages are clear

## Troubleshooting

### Tests Failing
1. Run with verbose: `pytest <ex>/test_verify.py -s -vv`
2. Check mock answers match validation rules
3. Verify `REPOSITORY_NAME` matches directory name
4. Ensure imports are correct
5. **Common patterns**:
   - Forgot to call `loader.start()` before `test.run()`
   - Mock answers dictionary keys don't match question text exactly
   - Test function missing `test_` prefix
   - Wrong exercise name in `GitAutograderTestLoader`

### Download Script Errors
1. Check `__requires_git__` and `__requires_github__` flags
2. Verify Git/GitHub CLI is available
3. Test with verbose mode: `setup(verbose=True)`
4. Check file paths are relative to exercise directory

### Validation Not Working
1. Verify validation rules match test expectations
2. Check that `validate()` is called on chain
3. Ensure correct status returned
4. Test with actual exercise setup

### Style/Quality Issues
Run quality checks:
- Format: `ruff format .`
- Lint: `ruff check .`
- Type check: `mypy <exercise-name>/`

See [AGENTS.md](../../../AGENTS.md) for coding standards.

## Pre-Submission Checklist

- ✓ Exercise discussion approved
- ✓ All tests passing: `./test.sh <exercise-name>`
- ✓ Download script tested
- ✓ README clear and complete
- ✓ Code follows conventions
- ✓ No unused imports or files
- ✓ Quality checks pass: `ruff format . && ruff check . && mypy <exercise>/`
