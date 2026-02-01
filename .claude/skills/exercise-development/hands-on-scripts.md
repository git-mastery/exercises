# Creating Hands-On Scripts

Hands-on scripts are simple demonstration scripts that show Git operations without validation or testing.

## When to Create Hands-On Scripts

Use hands-on scripts when:
- Demonstrating how a Git command works
- Showing effects of operations (e.g., what happens when you delete a branch)
- Exploratory learning without right/wrong answers
- Quick demonstrations that don't need validation
- Teaching through observation rather than assessment

## Implementation Steps

### 1. Create Script File

Use the scaffolding script:

```bash
./new.sh
# Choose "hands-on" or "h"
```

**Prompts:**
1. **Hands-on name**: Enter name after "hp-" prefix (e.g., entering "branch-demo" creates "hp-branch-demo")
2. **Requires Git?**: Default yes (if script uses Git commands)
3. **Requires GitHub?**: Default yes (set to no if script doesn't need GitHub CLI)

**Generated file**: `hands_on/<name>.py` with `__requires_git__`, `__requires_github__`, and `download(verbose: bool)` function

**Manual creation** (if needed):
```bash
touch hands_on/my_demo.py
```

### 2. Implement Required Variables

`__requires_git__` and `__requires_github__` flags at top of file.

### 3. Implement download() Function

This is the only required function - it performs the demonstration.

**Examples**: See [hands_on/branch_delete.py](../../../hands_on/branch_delete.py) or [hands_on/add_files.py](../../../hands_on/add_files.py).

### 4. Focus on Demonstration

Key principles:
- **Use verbose output** to show what's happening
- **Add print statements** to guide understanding
- **Leave repository** in an interesting state for exploration
- **Suggest commands** for users to run next

## Common Patterns

See examples in [hands_on/](../../../hands_on/) directory:
- Simple Git operations: [branch_delete.py](../../../hands_on/branch_delete.py)
- Branch operations: [create_branch.py](../../../hands_on/create_branch.py)
- GitHub operations: [remote_branch_pull.py](../../../hands_on/remote_branch_pull.py)
- Merge operations: Any merge-related script in hands_on/

## Best Practices

- Use helpful print statements with verbose flag
- Leave repository in explorable state (multiple branches, commits)
- Guide without prescribing (suggest commands, don't require)

## Hands-On vs Standard Exercise

| Aspect | Hands-On Script | Standard Exercise |
|--------|----------------|-------------------|
| **Purpose** | Demonstrate & explore | Teach & validate |
| **Structure** | Single `.py` file | Complete directory |
| **Files** | Just the script | download, verify, test, README |
| **Validation** | None | Required |
| **Testing** | Manual only | Automated with pytest |
| **Instructions** | Optional comments | Required README.md |
| **Success Criteria** | None | Defined rules |
| **User Action** | Run and observe | Complete and verify |
| **Creation Time** | 5-10 minutes | 1-2 hours |
| **Use Case** | Demos, exploration | Structured learning |

## Testing Hands-On Scripts

No formal tests required, but manually verify by running the script and checking the created state.

## Pre-Commit Checklist

- ✓ Has `__requires_git__` and `__requires_github__`
- ✓ Has `download(verbose: bool)` function
- ✓ Uses utility functions (not raw subprocess)
- ✓ Includes helpful verbose output
- ✓ Creates interesting state to explore
- ✓ Tested manually
- ✓ Follows naming conventions (snake_case)
