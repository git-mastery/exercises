import os
import stat

from repo_smith.repo_smith import RepoSmith

from exercise_utils.test import GitMasteryHelper


def setup(rs: RepoSmith):
    for i in range(1, 101):
        if i == 77:
            continue
        rs.files.create_or_update(f"file{i}.txt")

    rs.git.add(all=True)
    rs.git.commit(message="Change 1")

    rs.files.append("file14.txt", "This is a change")

    rs.files.create_or_update("file77.txt")
    for i in range(1, 101):
        os.chmod(f"file{i}.txt", stat.S_IREAD)

    rs.helper(GitMasteryHelper).create_start_tag()
