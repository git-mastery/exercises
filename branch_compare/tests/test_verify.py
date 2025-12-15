from git_autograder import GitAutograderStatus, GitAutograderTestLoader, assert_output
from git_autograder.answers.rules.has_exact_value_rule import HasExactValueRule

from ..verify import verify, QUESTION_ONE, QUESTION_TWO, NO_CHANGES_ERROR

REPOSITORY_NAME = "branch-compare"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load(
        "specs/base.yml",
        "start",
        mock_answers={
            QUESTION_ONE: "12345",
            QUESTION_TWO: "98765",
        },
    ) as output:
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_wrong_stream1_diff():
    with loader.load(
        "specs/base.yml",
        "start",
        mock_answers={
            QUESTION_ONE: "99999",
            QUESTION_TWO: "98765",
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_ONE)],
        )


def test_wrong_stream2_diff():
    with loader.load(
        "specs/base.yml",
        "start",
        mock_answers={
            QUESTION_ONE: "12345",
            QUESTION_TWO: "99999",
        },
    ) as output:
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [HasExactValueRule.NOT_EXACT.format(question=QUESTION_TWO)],
        )


def test_changes_made_extra_commit():
    with loader.load("specs/extra_commit_on_stream1.yml", "start") as output:
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NO_CHANGES_ERROR])
