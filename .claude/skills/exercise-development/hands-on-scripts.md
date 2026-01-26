# Creating Hands-On Scripts

Hands-on scripts are simple demonstration scripts that show Git operations without validation or testing.

## When to Create Hands-On Scripts

Use hands-on scripts when:
- **Demonstrating** how a Git command works
- **Showing effects** of operations (e.g., what happens when you delete a branch)
- **Exploratory learning** without right/wrong answers
- **Quick demonstrations** that don't need validation
- **Teaching through observation** rather than assessment

## Implementation Steps

### 1. Create Script File

Simply create a new `.py` file in the `hands_on/` directory:

```bash
# No scaffolding needed - just create the file
touch hands_on/my_demo.py
```

### 2. Implement Required Variables

```python
# At top of file
__requires_git__ = True      # Set True if uses Git commands
__requires_github__ = False  # Set True if uses GitHub CLI
```

### 3. Implement download() Function

This is the only required function - it performs the demonstration:

```python
import os
from exercise_utils.git import init, add, commit, checkout
from exercise_utils.file import create_or_update_file

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """Demonstrate creating and switching branches."""
    # Setup initial repository
    os.makedirs("demo-repo")
    os.chdir("demo-repo")
    
    init(verbose)
    create_or_update_file("README.md", "# Demo Project\n")
    add(["README.md"], verbose)
    commit("Initial commit", verbose)
    
    # Demonstrate the concept
    checkout("feature-branch", create_branch=True, verbose=verbose)
    create_or_update_file("feature.txt", "New feature\n")
    add(["feature.txt"], verbose)
    commit("Add feature", verbose)
    
    # Show the result
    if verbose:
        print("\n✓ Created feature-branch with new commit")
        print("Run 'git log --oneline --all --graph' to see the result")
```

### 4. Focus on Demonstration

Key principles:
- **Use verbose output** to show what's happening
- **Add print statements** to guide understanding
- **Leave repository** in an interesting state for exploration
- **Suggest commands** for users to run next

## Common Patterns

### Pattern: Simple Git Operation Demo

```python
import os
from exercise_utils.git import init, checkout
from exercise_utils.file import create_or_update_file

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """Show how to rename a branch."""
    os.makedirs("rename-demo")
    os.chdir("rename-demo")
    
    init(verbose)
    
    if verbose:
        print("\n✓ Repository initialized")
        print("Try running: git branch -m main trunk")
        print("Then: git branch")
```

### Pattern: Branch Operations Demo

```python
import os
from exercise_utils.git import init, checkout, add, commit
from exercise_utils.file import create_or_update_file

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """Demonstrate branch creation and switching."""
    os.makedirs("branch-demo")
    os.chdir("branch-demo")
    
    # Setup
    init(verbose)
    create_or_update_file("main.txt", "Main branch file\n")
    add(["main.txt"], verbose)
    commit("Initial on main", verbose)
    
    # Create feature branch
    checkout("feature", create_branch=True, verbose=verbose)
    create_or_update_file("feature.txt", "Feature file\n")
    add(["feature.txt"], verbose)
    commit("Add feature", verbose)
    
    # Back to main
    checkout("main", create_branch=False, verbose=verbose)
    
    if verbose:
        print("\n✓ Two branches created: main and feature")
        print("Current branch: main")
        print("Try: git log --oneline --all --graph")
```

### Pattern: GitHub Operations Demo

```python
import os
from exercise_utils.git import clone_repo_with_git, checkout, add, commit
from exercise_utils.github_cli import get_github_username, fork_repo, has_repo, delete_repo
from exercise_utils.file import append_to_file

__requires_git__ = True
__requires_github__ = True

def download(verbose: bool):
    """Demonstrate forking and cloning a repository."""
    TARGET_REPO = "git-mastery/sample-repo"
    FORK_NAME = "my-forked-repo"
    
    username = get_github_username(verbose)
    full_repo_name = f"{username}/{FORK_NAME}"
    
    # Clean up if exists
    if has_repo(full_repo_name, True, verbose):
        if verbose:
            print(f"Deleting existing fork: {full_repo_name}")
        delete_repo(full_repo_name, verbose)
    
    # Fork repository
    if verbose:
        print(f"Forking {TARGET_REPO}...")
    fork_repo(TARGET_REPO, FORK_NAME, verbose, True)
    
    # Clone locally
    if verbose:
        print(f"Cloning to local-fork directory...")
    clone_repo_with_git(
        f"https://github.com/{username}/{FORK_NAME}",
        verbose,
        "local-fork"
    )
    
    os.chdir("local-fork")
    
    # Make a change
    checkout("demo-branch", create_branch=True, verbose=verbose)
    append_to_file("README.md", "\n## Demo Addition\n")
    add(["README.md"], verbose)
    commit("Add demo section", verbose)
    
    if verbose:
        print(f"\n✓ Forked {TARGET_REPO} to {username}/{FORK_NAME}")
        print("✓ Cloned to local-fork directory")
        print("✓ Created demo-branch with changes")
        print("\nExplore the repository:")
        print("  git log --oneline")
        print("  git remote -v")
```

### Pattern: Merge Operations Demo

```python
import os
from exercise_utils.git import init, checkout, add, commit, merge
from exercise_utils.file import create_or_update_file

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """Demonstrate merging branches."""
    os.makedirs("merge-demo")
    os.chdir("merge-demo")
    
    # Setup main branch
    init(verbose)
    create_or_update_file("file.txt", "Line 1\n")
    add(["file.txt"], verbose)
    commit("Initial commit", verbose)
    
    # Create and work on feature branch
    checkout("feature", create_branch=True, verbose=verbose)
    create_or_update_file("file.txt", "Line 1\nLine 2 from feature\n")
    add(["file.txt"], verbose)
    commit("Add line 2", verbose)
    
    # Back to main and merge
    checkout("main", create_branch=False, verbose=verbose)
    merge("feature", ff=False, verbose=verbose)
    
    if verbose:
        print("\n✓ Merged feature branch into main")
        print("View the merge: git log --oneline --graph")
```

## Best Practices

### Use Helpful Print Statements

```python
if verbose:
    print("\n=== Demo Complete ===")
    print("✓ Created repository with 2 branches")
    print("\nNext steps:")
    print("  1. cd demo-repo")
    print("  2. git log --oneline --all --graph")
    print("  3. git branch -v")
```

### Leave Repository in Explorable State

```python
# Good - leaves interesting state
checkout("feature", create_branch=True, verbose=verbose)
commit("Feature work", verbose)
checkout("main", create_branch=False, verbose=verbose)
# Now user can explore both branches

# Less useful - ends in empty state
init(verbose)
# Not much to explore
```

### Guide Without Prescribing

```python
if verbose:
    print("\nTry these commands to explore:")
    print("  git status")
    print("  git log")
    print("  git branch")
    # Suggest, don't require
```

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

No formal tests required, but manually verify:

```bash
# 1. Run the script
python hands_on/my_demo.py

# 2. Check created state
cd demo-repo  # or whatever directory it creates
git status
git log --oneline --all --graph
git branch

# 3. Verify it demonstrates the concept clearly
```

## Examples

### Minimal Example
```python
import os
from exercise_utils.git import init

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """Show git init."""
    os.makedirs("init-demo")
    os.chdir("init-demo")
    init(verbose)
    
    if verbose:
        print("\n✓ Git repository initialized")
        print("Run 'git status' to see")
```

### Complete Example with GitHub
```python
import os
from exercise_utils.git import clone_repo_with_git, checkout, add, commit, push
from exercise_utils.github_cli import get_github_username, fork_repo
from exercise_utils.file import append_to_file

__requires_git__ = True
__requires_github__ = True

TARGET_REPO = "git-mastery/sample-repo"
FORK_NAME = "demo-fork"

def download(verbose: bool):
    """Complete GitHub workflow demonstration."""
    username = get_github_username(verbose)
    
    # Fork and clone
    fork_repo(TARGET_REPO, FORK_NAME, verbose, True)
    clone_repo_with_git(
        f"https://github.com/{username}/{FORK_NAME}",
        verbose,
        "demo-repo"
    )
    os.chdir("demo-repo")
    
    # Make changes
    checkout("demo-feature", create_branch=True, verbose=verbose)
    append_to_file("README.md", "\n## Demo Feature\n")
    add(["README.md"], verbose)
    commit("Add demo feature", verbose)
    push("origin", "demo-feature", verbose)
    
    if verbose:
        print("\n=== Demo Complete ===")
        print(f"✓ Forked to {username}/{FORK_NAME}")
        print("✓ Cloned to demo-repo")
        print("✓ Created demo-feature branch")
        print("✓ Pushed changes to GitHub")
        print("\nView on GitHub:")
        print(f"  https://github.com/{username}/{FORK_NAME}")
```

## Quick Checklist

Before committing a hands-on script:
- ✓ Has `__requires_git__` and `__requires_github__`
- ✓ Has `download(verbose: bool)` function
- ✓ Uses utility functions (not raw subprocess)
- ✓ Includes helpful verbose output
- ✓ Creates interesting state to explore
- ✓ Tested manually
- ✓ Follows naming conventions (snake_case)
