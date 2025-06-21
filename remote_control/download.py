import os
import shutil


def setup(verbose: bool = False):
    # TODO: Resolve this bug where the assert doesn't happen but the folder still exists
    os.chdir("..")
    shutil.rmtree(f"{os.getcwd()}/deleted", ignore_errors=False)
    assert not os.path.exists("deleted"), "Still exists after rmtree!"
