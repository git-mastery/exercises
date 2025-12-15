from exercise_utils.git import tag, tag_with_options


def setup(verbose: bool = False):
    tag_with_options("first-update", ["HEAD~4"], verbose)
    tag("april-update", verbose)
    tag("may-update", verbose)
