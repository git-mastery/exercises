from exercise_utils.git import (
    add,
    commit,
    checkout,
    merge_with_message,
)
from exercise_utils.file import (
    create_or_update_file,
    append_to_file,
)

def setup(verbose: bool = False):
    # Create initial files and commits
    create_or_update_file("rick.txt", "Scientist\n")
    add(["rick.txt"], verbose)
    commit("Add Rick", verbose)

    create_or_update_file("morty.txt", "Boy\n")
    add(["morty.txt"], verbose)
    commit("Add Morty", verbose)

    # Create and switch to branch 'others'
    checkout("others", create_branch=True, verbose=verbose)

    create_or_update_file("birdperson.txt", "No job\n")
    add(["birdperson.txt"], verbose)
    commit("Add Birdperson", verbose)

    append_to_file("birdperson.txt", "Cyborg\n")
    add(["birdperson.txt"], verbose)
    commit("Add Cyborg to birdperson.txt", verbose)

    create_or_update_file("tammy.txt", "Spy\n")
    add(["tammy.txt"], verbose)
    commit("Add Tammy", verbose)

    # Merge back into main
    checkout("main", create_branch=False, verbose=verbose)
    merge_with_message("others", ff=True, message="Introduce others", verbose=verbose)