import os

from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.git import init, add, commit, tag
from pathlib import Path

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
    """
    hp-checkout-commits (T4L4)
    - Creates a local repo 'things' with multiple commits and tags.
    - Students can practice checking out commits by hash, tag, or HEAD~N references.
    """
    
    target_dir = Path("things")

    # Clean existing sandbox if re-downloading
    if target_dir.exists():
        import shutil
        shutil.rmtree(target_dir)

    # Create sandbox folder
    target_dir.mkdir()
    os.chdir(target_dir)

    # Initialize git repo
    init(verbose)

    # Step 1: Add fruits.txt (first commit)
    with open("fruits.txt", "w") as f:
        f.write("apples\nbananas\ncherries\ndragon fruits\n")
    add(["fruits.txt"], verbose)
    commit("Add fruits.txt", verbose)

    # Step 2: Update fruits.txt and commit
    with open("fruits.txt", "a") as f:
        f.write("elderberries\nfigs\n")
    add(["fruits.txt"], verbose)
    commit("Add elderberries and figs into fruits.txt", verbose)

    # Step 3: Create colours.txt and shapes.txt, commit, tag 0.9
    with open("colours.txt", "w") as f:
        f.write("a file for colours\n")
    with open("shapes.txt", "w") as f:
        f.write("a file for shapes\n")
    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)
    tag("0.9", verbose)

    # Step 4: Update fruits.txt again
    with open("fruits.txt", "w") as f:
        f.write("apples, apricots\nbananas\nblueberries\ncherries\ndragon fruits\nfigs\n")
    add(["fruits.txt"], verbose)
    commit("Update fruits list", verbose)

    # Step 5: Update colours.txt and commit, tag 1.0
    with open("colours.txt", "a") as f:
        f.write("blue\nred\nwhite\n")
    add(["colours.txt"], verbose) 
    commit("colours.txt: Add some colours", verbose)
    tag("1.0", verbose)

    # Step 6: Update shapes.txt and commit
    with open("shapes.txt", "a") as f:
        f.write("circle\noval\nrectangle\nsquare\n")
    add(["shapes.txt"], verbose) 
    commit("shapes.txt: Add some shapes", verbose)
