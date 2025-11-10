from exercise_utils.git import tag


def setup(verbose: bool = False):    
    tag("first-update", verbose, "HEAD~4")
    tag("april-update", verbose)
    tag("may-update", verbose)
