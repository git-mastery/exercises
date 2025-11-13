from exercise_utils.cli import run_command
from exercise_utils.gitmastery import create_start_tag

__resources__ = {}


def setup(verbose: bool = False):
    # Marks the start of setup (Git-Mastery internal logging)
    create_start_tag(verbose)

    # Create initial files and commits
    run_command('echo "Scientist" > rick.txt', verbose)
    run_command('git add .', verbose)
    run_command('git commit -m "Add Rick"', verbose)

    run_command('echo "Boy" > morty.txt', verbose)
    run_command('git add .', verbose)
    run_command('git commit -m "Add Morty"', verbose)

    # Create and switch to branch 'others'
    run_command('git switch -c others', verbose)
    run_command('echo "No job" > birdperson.txt', verbose)
    run_command('git add .', verbose)
    run_command('git commit -m "Add Birdperson"', verbose)

    run_command('echo "Cyborg" >> birdperson.txt', verbose)
    run_command('git add .', verbose)
    run_command('git commit -m "Add Cyborg to birdperson.txt"', verbose)

    run_command('echo "Spy" > tammy.txt', verbose)
    run_command('git add .', verbose)
    run_command('git commit -m "Add Tammy"', verbose)

    # Merge back into main
    run_command('git switch main', verbose)
    run_command('git merge others -m "Introduce others"', verbose)