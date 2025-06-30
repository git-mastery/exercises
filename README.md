# exercises

## Git-Mastery exercise structure

When you download an exercise, you will get the following folder structure:


## `.gitmastery-exercise.json`

Configuration fields for each exercise:

1. `exercise_name`: name of exercise
2. `tags`: list of tags for exercise
3. `requires_git`: downloading the exercise will check that Git is installed and that `git config` is already done
4. `requires_github`: downloading the exercise will check that Github and Github CLI is installed
5. `base_files`: provides the files to be included outside of the repository, along with `.gitmastery-exercise.json` and `README.md`, most often used for `answers.txt`
6. `exercise_repo`: configuration for what the exercise repository would look like
    1. `repo_type`: `local` (creates and initializes the folder as a Git repository) or `remote` (reference a repository on Github)
    2. `repo_name`: name of repository during cloning
    3. `repo_title`: (only read if `link` is present) link of repository on Github
    4. `create_fork`: (only read if `link` is present) flag to determine if we need to fork the repository to the student's machine, otherwise it just clones the repository
    5. `init`: (only read if `custom` is present) flag to determine if we will call `git init` on the exercise repository (useful if we don't want to start out with a Git repository)


## TODOs

- [X] Add validation for exercise configuration (e.g. cannot fork + not require Github) - to run as CI
