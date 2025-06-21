import os
import shutil


def setup(verbose: bool = False):
    print(os.getcwd())
    os.chdir("..")
    print(os.listdir())
    # shutil.rmtree("deleted/")
