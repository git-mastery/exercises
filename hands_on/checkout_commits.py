import os

from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag
from exercise_utils.git import init, add, commit, tag
from exercise_utils.file import create_or_update_file, append__to_file
from pathlib import Path

__requires_git__ = True
__requires_github__ = False

def download(verbose: bool):
        
    target_dir = Path("things")

   
    os.makedirs(target_dir, exist_ok=True)
    os.chdir(target_dir)

    init(verbose)

    create_or_update_file(
	"fruits.txt",
   	"""
	apples
    	bananas
    	cherries
    	dragon fruits
    	"""
    )
    add(["fruits.txt"], verbose)
    commit("Add fruits.txt", verbose)

    append_to_file("fruits.txt", """
	elderberries
	figs
	""")
    add(["fruits.txt"], verbose)
    commit("Add elderberries and figs into fruits.txt", verbose)

    create_or_update_file("colours.txt", """
	a file for colours
	""")

    create_or_update_file("shapes.txt", """
	a file for shapes
	""")

    add(["colours.txt", "shapes.txt"], verbose)
    commit("Add colours.txt, shapes.txt", verbose)
    tag("0.9", verbose)

    create_or_update_file("fruits.txt", """
	apples, apricots
	bananas
	blueberries
	cherries
	dragon fruits
	figs
	""")
    add(["fruits.txt"], verbose)
    commit("Update fruits list", verbose)

    append_to_file("colours.txt", """
	blue
	red
	white
	""")
    add(["colours.txt"], verbose) 
    commit("colours.txt: Add some colours", verbose)
    tag("1.0", verbose)

    append_to_file("shapes.txt", """
	circle
	oval
	rectangle
	square
	""")
    add(["shapes.txt"], verbose) 
    commit("shapes.txt: Add some shapes", verbose)
