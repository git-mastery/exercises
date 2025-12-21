from git_autograder import (
    GitAutograderOutput,
    GitAutograderExercise,
    GitAutograderStatus,
)

MISSING_FILE = "You are missing the {filename} file."
COMMITS_UNREVERTED = "You have not reverted the commits!"
COMMITS_REVERTED_WRONG_ORDER = "You have reverted the commits in the wrong order!"
INCORRECT_READINGS = "The files contain the wrong readings!"

EXPECTED_EAST = (
    "4821\n9304\n1578\n6042\n7189\n2463\n8931\n5710\n4428\n3097\n8652\n1904\n7485\n6379\n5140\n9836\n2057\n4719\n3568\n8243\n"
)

EXPECTED_NORTH = (
    "6841\n2307\n9754\n4169\n5823\n3086\n7592\n8420\n1679\n5034\n2918\n7645\n8501\n4576\n9208\n3461\n5789\n6940\n1235\n8890\n"
)

EXPECTED_SOUTH = (
    "7412\n5068\n8921\n3754\n2809\n6197\n4530\n9674\n1185\n7326\n5401\n8937\n2640\n7083\n5914\n3208\n8745\n4069\n1592\n6831\n"
)

EXPECTED_WEST = (
    "5193\n8042\n6721\n4389\n2075\n9510\n3648\n7281\n5904\n1837\n4416\n9032\n7765\n6208\n3589\n8471\n2940\n1683\n7352\n5129\n"
)

UNREVERTED_EAST = (
    "4821\n9304\n1578\n6042\n7189\n2463\n8931\n5710\n4428\n3097\n8652\n1904\n7285\n6379\n5140\n9836\n2057\n4719\n3568\n8243\n"
)

UNREVERTED_NORTH = (
    "6841\n2307\n9754\n4169\n5823\n3086\n7592\n8420\n1679\n5034\n2918\n7645\n8301\n4576\n9208\n3461\n5789\n6940\n1235\n8890\n"
)

# Unreverted South and West are equivalent to expected South and West
# UNREVERTED_SOUTH = (
#     "7412\n5068\n8921\n3754\n2809\n6197\n4530\n9674\n1185\n7326\n5401\n8937\n2640\n7083\n5914\n3208\n8745\n4069\n1592\n6831\n"
# )

# UNREVERTED_WEST = (
#     "5193\n8042\n6721\n4389\n2075\n9510\n3648\n7281\n5904\n1837\n4416\n9032\n7765\n6208\n3589\n8471\n2940\n1683\n7352\n5129\n"
# )

# Reverting East and North in the wrong order leads to the same result
# WRONG_ORDER_REVERT_EAST = (
#     "4821\n9304\n1578\n6042\n7189\n2463\n8931\n5710\n4428\n3097\n8652\n1904\n7485\n6379\n5140\n9836\n2057\n4719\n3568\n8243\n"
# )

# WRONG_ORDER_REVERT_NORTH = (
#     "6841\n2307\n9754\n4169\n5823\n3086\n7592\n8420\n1679\n5034\n2918\n7645\n8501\n4576\n9208\n3461\n5789\n6940\n1235\n8890\n"
# )

WRONG_ORDER_REVERT_SOUTH = (
    "7412\n5068\n8921\n3754\n2809\n6197\n4330\n9674\n1185\n7326\n5401\n8937\n2640\n7083\n5914\n3208\n8745\n4069\n1592\n6831\n"
)

WRONG_ORDER_REVERT_WEST = (
    "5193\n8042\n6721\n4389\n2075\n9510\n3638\n7281\n5904\n1837\n4416\n9032\n7765\n6208\n3589\n8471\n2940\n1683\n7352\n5129\n"
)

EAST_PATH = "east.csv"
NORTH_PATH = "north.csv"
SOUTH_PATH = "south.csv"
WEST_PATH = "west.csv"

def verify(exercise: GitAutograderExercise) -> GitAutograderOutput:
    comments = []

    with exercise.repo.files.file_or_none(EAST_PATH) as east_file:
        if east_file is None:
            comments.append(MISSING_FILE.format(filename="east.csv"))
        else:
            east_contents = east_file.read()

    with exercise.repo.files.file_or_none(NORTH_PATH) as north_file:
        if north_file is None:
            comments.append(MISSING_FILE.format(filename="north.csv"))
        else:
            north_contents = north_file.read()

    with exercise.repo.files.file_or_none(SOUTH_PATH) as south_file:
        if south_file is None:
            comments.append(MISSING_FILE.format(filename="south.csv"))
        else:
            south_contents = south_file.read()

    with exercise.repo.files.file_or_none(WEST_PATH) as west_file:
        if west_file is None:
            comments.append(MISSING_FILE.format(filename="west.csv"))
        else:
            west_contents = west_file.read()

    if comments:
        raise exercise.wrong_answer(comments)

    if (east_contents == UNREVERTED_EAST
        and north_contents == UNREVERTED_NORTH):
        raise exercise.wrong_answer([COMMITS_UNREVERTED])

    if (south_contents == WRONG_ORDER_REVERT_SOUTH
        and west_contents == WRONG_ORDER_REVERT_WEST):
        raise exercise.wrong_answer([COMMITS_REVERTED_WRONG_ORDER])

    if not (east_contents == EXPECTED_EAST
        and north_contents == EXPECTED_NORTH
        and south_contents == EXPECTED_SOUTH
        and west_contents == EXPECTED_WEST):
        raise exercise.wrong_answer([INCORRECT_READINGS])

    return exercise.to_output(["Good work reverting commits!"], GitAutograderStatus.SUCCESSFUL)
