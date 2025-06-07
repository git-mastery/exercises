from git_autograder import GitAutograderOutput, GitAutograderRepo, GitAutograderStatus

EXPECTED_FILES = {"alice.txt", "bob.txt", "jim.txt", "joe.txt", "carrey.txt"}


def verify(repo: GitAutograderRepo) -> GitAutograderOutput:
    staged_diff = repo.repo.index.diff("HEAD")

    added_files = set()
    for diff_item in staged_diff:
        added_files.add(diff_item.a_path)

    if len(added_files & EXPECTED_FILES) != len(EXPECTED_FILES):
        missing_files = EXPECTED_FILES.difference(added_files)
        raise repo.wrong_answer([f"Did not add {file}" for file in missing_files])

    return repo.to_output(
        ["Great work! You have successfully checked in all the actors!"],
        status=GitAutograderStatus.SUCCESSFUL,
    )
