from exercise_utils.git import checkout, empty_commit, push


def setup(verbose: bool = False):
    checkout("improve-loadding", True, verbose)
    empty_commit("Improved loading of page", verbose)

    push("origin", "improve-loadding", verbose)

    checkout("main", False, verbose)
