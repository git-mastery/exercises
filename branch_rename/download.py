from exercise_utils.git import checkout, empty_commit


def setup(verbose: bool = False):
    empty_commit("Initialize project", verbose)
    empty_commit("Add React boilerplate", verbose)

    checkout("login", True, verbose)
    empty_commit("Implement login feature", verbose)

    checkout("main", False, verbose)
    empty_commit("Create homepage", verbose)

    checkout("login", False, verbose)
    empty_commit("Fix login password bug", verbose)
    checkout("main", False, verbose)
