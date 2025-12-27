from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    COMMITS_REVERTED_WRONG_ORDER,
    COMMITS_UNREVERTED,
    INCORRECT_READINGS,
    MISSING_FILE,
    verify,
)

REPOSITORY_NAME = "sensors-revert"


loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)

CLONE_URL = "https://github.com/git-mastery/gm-sensors"


def test_base():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.revert("dbac57019977296abff9e4f687f587c4a2d24f02")
        rs.git.revert("59505167b47f35c12d21bc61d731226b394a5341")

        output = test.run()
        assert_output(output, GitAutograderStatus.SUCCESSFUL)


def test_no_revert():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_UNREVERTED],
        )


def test_wrong_order_revert():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.revert("59505167b47f35c12d21bc61d731226b394a5341")
        rs.git.revert("dbac57019977296abff9e4f687f587c4a2d24f02")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_REVERTED_WRONG_ORDER],
        )


def test_missing_files():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        for file in ["east", "north", "south", "west"]:
            rs.files.delete(f"{file}.csv")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [
                MISSING_FILE.format(filename="east.csv"),
                MISSING_FILE.format(filename="north.csv"),
                MISSING_FILE.format(filename="south.csv"),
                MISSING_FILE.format(filename="west.csv"),
            ],
        )


def test_incorrect_readings():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.revert("dbac57019977296abff9e4f687f587c4a2d24f02")
        rs.git.revert("59505167b47f35c12d21bc61d731226b394a5341")
        rs.files.create_or_update(
            "east.csv", "4821\n9304\n1578\n6042\n7189\n2463\n8931\n5710\n"
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [INCORRECT_READINGS],
        )


def test_no_revert_commit():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.files.create_or_update(
            "east.csv",
            """
            4821
            9304
            1578
            6042
            7189
            2463
            8931
            5710
            4428
            3097
            8652
            1904
            7485
            6379
            5140
            9836
            2057
            4719
            3568
            8243
            """,
        )
        rs.files.create_or_update(
            "north.csv",
            """
            6841
            2307
            9754
            4169
            5823
            3086
            7592
            8420
            1679
            5034
            2918
            7645
            8501
            4576
            9208
            3461
            5789
            6940
            1235
            8890
            """,
        )
        rs.files.create_or_update(
            "south.csv",
            """
            7412
            5068
            8921
            3754
            2809
            6197
            4530
            9674
            1185
            7326
            5401
            8937
            2640
            7083
            5914
            3208
            8745
            4069
            1592
            6831
            """,
        )
        rs.files.create_or_update(
            "west.csv",
            """
            5193
            8042
            6721
            4389
            2075
            9510
            3648
            7281
            5904
            1837
            4416
            9032
            7765
            6208
            3589
            8471
            2940
            1683
            7352
            5129
            """,
        )

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_UNREVERTED],
        )


def test_only_jan_14_reverted():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.revert("dbac57019977296abff9e4f687f587c4a2d24f02")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_UNREVERTED],
        )


def test_only_jan_13_reverted():
    with loader.start(clone_from=CLONE_URL) as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.revert("59505167b47f35c12d21bc61d731226b394a5341")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.UNSUCCESSFUL,
            [COMMITS_REVERTED_WRONG_ORDER],
        )
