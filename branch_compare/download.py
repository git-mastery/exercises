from exercise_utils.git import add, commit, checkout
from exercise_utils.file import append_to_file, create_or_update_file

import random


def get_sequence(n=1000, digits=8, seed=None):
    rng = random.Random(seed)
    lo, hi = 10 ** (digits - 1), 10**digits - 1
    return rng.sample(range(lo, hi + 1), k=n)


def get_modified_sequence(seq, digits=8, idx=None, seed=None):
    rng = random.Random(seed)
    n = len(seq)
    if idx is None:
        idx = rng.randrange(n)

    modified = seq.copy()
    seen = set(seq)
    lo, hi = 10 ** (digits - 1), 10**digits - 1

    old = modified[idx]
    new = old
    while new in seen:
        new = rng.randint(lo, hi)
    modified[idx] = new
    return modified


def setup(verbose: bool = False):
    orig_data = get_sequence()
    modified_data = get_modified_sequence(orig_data)

    create_or_update_file("data.txt", "")
    add(["data.txt"], verbose)
    commit("Add empty data.txt", verbose)
    checkout("stream-1", True, verbose)

    join_orig_data = "\n".join(map(str, orig_data))
    append_to_file("data.txt", join_orig_data)

    add(["data.txt"], verbose)
    commit("Add data to data.txt", verbose)

    checkout("main", False, verbose)
    checkout("stream-2", True, verbose)

    join_modified_data = "\n".join(map(str, modified_data))
    append_to_file("data.txt", join_modified_data)

    add(["data.txt"], verbose)
    commit("Add data to data.txt", verbose)

    checkout("main", False, verbose)
