from exercise_utils.git import add
from exercise_utils.file import create_or_update_file


def setup(verbose: bool = False):
    create_or_update_file(
        "west.csv",
        """
        5193
        8042
        6721
        4389
        2075
        9510
        3642
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

    create_or_update_file(
        "north.csv",
        """
        6841
        2307
        9754
        4169
        5823
        3086
        7590
        8420
        1679
        5034
        2918
        7645
        8301
        4576
        9208
        3461
        5789
        6940
        1235
        8890
        """,
    )

    create_or_update_file(
        "south.csv",
        """
        7412
        5068
        8921
        3754
        2809
        6197
        4531
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

    add(["north.csv"], verbose)