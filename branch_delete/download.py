from exercise_utils.git import checkout, empty_commit, merge


def setup(verbose: bool = False):
    empty_commit("Implement loading", verbose)
    empty_commit("Fix loading bug", verbose)

    checkout("optimization-approach-1", True, verbose)
    empty_commit("Apply bubble sort", verbose)
    empty_commit("Fix sorting bug", verbose)

    checkout("main", False, verbose)
    checkout("optimization-approach-2", True, verbose)
    empty_commit("Apply merge sort", verbose)

    checkout("main", False, verbose)
    merge("optimization-approach-1", False, verbose)
