from git_autograder import (
    GitAutograderExercise,
    GitAutograderOutput,
    GitAutograderStatus,
)

ALICE_REMOTE_NAME = "alice-upstream"
ALICE_REMOTE_MISSING = f"Remote '{ALICE_REMOTE_NAME}' is missing! Remember to add it and point it to https://github.com/git-mastery/gm-shapes-alice"
ALICE_REMOTE_WRONG = f"Remote '{ALICE_REMOTE_NAME}' is not pointing to https://github.com/git-mastery/gm-shapes-alice, fix that!"
ALICE_NO_FETCH = "You have not fetched Alice's changes yet!"
ALICE_NO_MERGE = "You did not pull Alice's changes to your own main branch!"

BOB_REMOTE_NAME = "bob-upstream"
BOB_REMOTE_MISSING = f"Remote '{BOB_REMOTE_NAME}' is missing! Remember to add it and point it to https://github.com/git-mastery/gm-shapes-bob"
BOB_REMOTE_WRONG = f"Remote '{BOB_REMOTE_NAME}' is not pointing to https://github.com/git-mastery/gm-shapes-bob, fix that!"
BOB_NO_FETCH = "You have not fetched Bob's changes yet!"
BOB_MERGE = "You should not have pulled Bob's changes to your own main branch!"
RESET_EXERCISE = "Reset the exercise using 'gitmastery progress reset' to try again!"


def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    # Checks for Alice
    if not exercise.repo.remotes.has_remote(ALICE_REMOTE_NAME):
        raise exercise.wrong_answer([ALICE_REMOTE_MISSING])

    alice_remote = exercise.repo.remotes.remote(ALICE_REMOTE_NAME)
    if not alice_remote.is_for_repo("git-mastery", "gm-shapes-alice"):
        raise exercise.wrong_answer([ALICE_REMOTE_WRONG])

    local_main_commit = exercise.repo.commits.commit("main")

    alice_main_commit = exercise.repo.commits.commit_or_none("alice-upstream/main")
    if not alice_main_commit:
        raise exercise.wrong_answer([ALICE_NO_FETCH])

    if not local_main_commit.is_child(alice_main_commit):
        # Did not merge
        raise exercise.wrong_answer([ALICE_NO_MERGE])

    # Checks for Bob
    if not exercise.repo.remotes.has_remote(BOB_REMOTE_NAME):
        raise exercise.wrong_answer([BOB_REMOTE_MISSING])

    bob_remote = exercise.repo.remotes.remote(BOB_REMOTE_NAME)
    if not bob_remote.is_for_repo("git-mastery", "gm-shapes-bob"):
        raise exercise.wrong_answer([BOB_REMOTE_WRONG])

    bob_main_commit = exercise.repo.commits.commit_or_none("bob-upstream/main")
    if not bob_main_commit:
        raise exercise.wrong_answer([BOB_NO_FETCH])

    if local_main_commit.is_child(bob_main_commit):
        # Merged
        raise exercise.wrong_answer([BOB_MERGE, RESET_EXERCISE])

    return exercise.to_output(
        ["Great work fetching and pulling different upstreams!"],
        GitAutograderStatus.SUCCESSFUL,
    )
