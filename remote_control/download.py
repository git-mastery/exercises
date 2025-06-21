import os
import shutil


def setup(verbose: bool = False):
    print(os.getcwd())
    os.chdir("..")
    print(os.listdir())
    print(os.getcwd())
    shutil.rmtree(f"{os.getcwd()}/deleted", ignore_errors=False)
    assert not os.path.exists("deleted"), "Still exists after rmtree!"
