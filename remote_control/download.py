import os
import shutil


def setup(verbose: bool = False):
    os.chdir("..")
    print(os.listdir())
    shutil.rmtree("deleted/")
