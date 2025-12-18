from sensors_reset.verify import CONTAINS_TASK_THREE_COMMIT
from sensors_reset.verify import CONTAINS_TASK_TWO_COMMIT
from sensors_reset.verify import CONTAINS_TASK_ONE_COMMITS
from git_autograder.status import GitAutograderStatus
from git_autograder.test_utils import assert_output
from git_autograder import GitAutograderTestLoader

from ..verify import verify

REPOSITORY_NAME = "sensors-reset"

loader = GitAutograderTestLoader(__file__, REPOSITORY_NAME, verify)


def test_base():
    with loader.load("specs/base.yml", "start") as output:
        # assert_output(output, GitAutograderStatus.SUCCESSFUL)
        pass


def test_no_changes():
    with loader.load("specs/no_changes.yml", "start") as output:
        # assert_output(
        #     output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_ONE_COMMITS]
        # )
        pass


def test_wrong_task_one_reset():
    with loader.load("specs/wrong_task_one_reset.yml", "start") as output:
        # assert_output(
        #     output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_ONE_COMMITS]
        # )
        pass


def test_wrong_task_two_reset():
    with loader.load("specs/wrong_task_two_reset.yml", "start") as output:
        # assert_output(
        #     output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_TWO_COMMIT]
        # )
        pass


def test_wrong_task_three_reset():
    with loader.load("specs/wrong_task_three_reset.yml", "start") as output:
        # assert_output(
        #     output, GitAutograderStatus.UNSUCCESSFUL, [CONTAINS_TASK_THREE_COMMIT]
        # )
        pass
