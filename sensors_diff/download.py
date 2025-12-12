from exercise_utils.git import add

__resources__ = {
    "south.csv": "south.csv",
    "north.csv": "north.csv",
    "west.csv": "west.csv",
}


def setup(verbose: bool = False):
    add(["north.csv"], verbose)
