from exercise_utils.test import GitAutograderTestLoader, assert_output
from git_autograder.status import GitAutograderStatus

from .verify import (
    MISSING_BRANCH,
    MISSING_COMMIT,
    WRONG_CONTENT,
    WRONG_START,
    verify,
)

REPOSITORY_NAME = "branch-previous"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I heard someone knocking at the door.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention knocking")

        rs.git.checkout("sleep-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I fell asleep on the couch.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_visitor_missing_branch():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("sleep-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I fell asleep on the couch.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_BRANCH.format(branch_name="visitor-line")],
        )


def test_sleep_missing_branch():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I heard someone knocking at the door.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention knocking")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_BRANCH.format(branch_name="sleep-line")],
        )


def test_visitor_wrong_start_first_commit():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD~2", branch=True)

        rs.files.append("story.txt", "I heard someone knocking at the door.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention knocking")

        rs.git.checkout("sleep-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I fell asleep on the couch.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_START.format(branch_name="visitor-line")],
        )


def test_visitor_wrong_start_third_commit():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD", branch=True)

        rs.files.append("story.txt", "I heard someone knocking at the door.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention knocking")

        rs.git.checkout("sleep-line", start_point="HEAD~2", branch=True)

        rs.files.append("story.txt", "I fell asleep on the couch.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [WRONG_START.format(branch_name="visitor-line")],
        )


def test_visitor_wrong_content():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "Wrong content here.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention knocking")

        rs.git.checkout("sleep-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I fell asleep on the couch.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                WRONG_CONTENT.format(
                    branch_name="visitor-line",
                    expected_content="I heard someone knocking at the door.",
                )
            ],
        )


def test_sleep_wrong_content():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I heard someone knocking at the door.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention knocking")

        rs.git.checkout("sleep-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "Wrong content here.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                WRONG_CONTENT.format(
                    branch_name="sleep-line",
                    expected_content="I fell asleep on the couch.",
                )
            ],
        )


def test_visitor_missing_commit():
    with loader.start() as (test, rs):
        rs.files.create_or_update("story.txt", "It was a dark and stormy night.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe night")

        rs.files.append("story.txt", "I was alone in my room.")
        rs.git.add(all=True)
        rs.git.commit(message="Describe location")

        rs.files.append("story.txt", "I heard a strange noise.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention noise")

        rs.git.checkout("visitor-line", start_point="HEAD~1", branch=True)

        rs.git.checkout("sleep-line", start_point="HEAD~1", branch=True)

        rs.files.append("story.txt", "I fell asleep on the couch.")
        rs.git.add(all=True)
        rs.git.commit(message="Mention sleeping")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [MISSING_COMMIT.format(branch_name="visitor-line")],
        )
