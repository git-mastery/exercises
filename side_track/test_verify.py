from exercise_utils.test import GitAutograderTestLoader, GitMasteryHelper, assert_output
from git_autograder import GitAutograderStatus

from .verify import (
    CALCULATOR_NOT_FIXED,
    GREET_NOT_FIXED,
    MISSING_BUG_FIX_BRANCH,
    MISSING_COMMITS,
    NOT_ON_MAIN,
    UNCOMMITTED_CHANGES,
    verify,
)

REPOSITORY_NAME = "side-track"

loader = GitAutograderTestLoader(REPOSITORY_NAME, verify)


def test_base():
    with loader.start() as (test, rs):
        rs.git.commit(message="Initial commit", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.checkout("bug-fix", branch=True)
        rs.files.create_or_update(
            "greet.py",
            """
            def greet(name):
                print(f"Hi {name}")
            """,
        )
        rs.git.add("greet.py")
        rs.git.commit(message="Fix greet function", allow_empty=False)
        rs.files.create_or_update(
            "calculator.py",
            """
            def add(a, b):
                return a + b


            def subtract(a, b):
                return a - b


            def divide(a, b):
                return a / b


            def multiply(a, b):
                return a * b
            """,
        )
        rs.git.add("calculator.py")
        rs.git.commit(message="Fix add function", allow_empty=False)
        rs.git.checkout("main")

        output = test.run()
        assert_output(
            output,
            GitAutograderStatus.SUCCESSFUL,
        )


def test_missing_branch():
    with loader.start() as (test, rs):
        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_BUG_FIX_BRANCH]
        )


def test_uncommitted():
    with loader.start() as (test, rs):
        rs.git.checkout("bug-fix", branch=True)
        rs.files.create_or_update("test.txt", "hi")
        rs.git.add("test.txt")
        rs.git.commit(message="Start")
        rs.files.create_or_update("test.txt", "changed")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [UNCOMMITTED_CHANGES])


def test_not_main():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.checkout("bug-fix", branch=True)
        rs.files.create_or_update(
            "greet.py",
            """
            def greet(name):
                print(f"Hi {name}")
            """,
        )
        rs.git.add("greet.py")
        rs.git.commit(message="Fix greet function", allow_empty=False)
        rs.files.create_or_update(
            "calculator.py",
            """
            def add(a, b):
                return a + b
            """,
        )
        rs.git.add("calculator.py")
        rs.git.commit(message="Fix add function", allow_empty=False)

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [NOT_ON_MAIN])


def test_no_bug_fix():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)

        output = test.run()
        assert_output(
            output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_BUG_FIX_BRANCH]
        )


def test_missing_commits():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.checkout("bug-fix", branch=True)
        rs.files.create_or_update(
            "greet.py",
            """
            def greet(name):
                print(f"Hi {name}")
            """,
        )
        rs.files.create_or_update(
            "calculator.py",
            """
            def add(a, b):
                return a + b
            """,
        )
        rs.git.add(all=True)
        rs.git.commit(message="Add", allow_empty=False)
        rs.git.checkout("main")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [MISSING_COMMITS])


def test_greet_not_fixed():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.checkout("bug-fix", branch=True)
        rs.files.create_or_update(
            "greet.py",
            """
            def greet(name):
                print("Hi Alice")
            """,
        )
        rs.files.create_or_update(
            "calculator.py",
            """
            def add(a, b):
                return a + b
            """,
        )
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.add(["greet.py", "calculator.py"])
        rs.git.commit(message="Add")
        rs.git.checkout("main")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [GREET_NOT_FIXED])


def test_add_not_fixed():
    with loader.start() as (test, rs):
        rs.git.commit(message="Empty", allow_empty=True)
        rs.helper(GitMasteryHelper).create_start_tag()
        rs.git.checkout("bug-fix", branch=True)
        rs.files.create_or_update(
            "greet.py",
            """
            def greet(name):
                print("Hi " + name)
            """,
        )
        rs.files.create_or_update(
            "calculator.py",
            """
            def add(a, b):
                return a - b
            """,
        )
        rs.git.commit(message="Empty", allow_empty=True)
        rs.git.add(["greet.py", "calculator.py"])
        rs.git.commit(message="Add")
        rs.git.checkout("main")

        output = test.run()
        assert_output(output, GitAutograderStatus.UNSUCCESSFUL, [CALCULATOR_NOT_FIXED])
