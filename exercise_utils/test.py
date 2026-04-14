import json
import os
import tempfile
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import (
    Any,
    Callable,
    ContextManager,
    Dict,
    Iterator,
    List,
    Literal,
    Optional,
    Self,
    Tuple,
    overload,
)
from unittest import mock

import pytz
from git import Repo
from git_autograder import (
    GitAutograderExercise,
    GitAutograderInvalidStateException,
    GitAutograderOutput,
    GitAutograderStatus,
    GitAutograderWrongAnswerException,
)
from git_autograder.answers import GitAutograderAnswers
from git_autograder.exercise_config import ExerciseConfig
from repo_smith.helpers.helper import Helper
from repo_smith.repo_smith import RepoSmith, create_repo_smith

"""Stores the test utils for exercises."""


class GitMasteryHelper(Helper):
    def __init__(self, repo: Repo, verbose: bool) -> None:
        super().__init__(repo, verbose)

    def create_start_tag(self) -> None:
        # TODO: Reconsider if this should be inlined within repo-smith or separated out
        """Creates the Git-Mastery start tag."""
        assert self.repo is not None
        all_commits = list(self.repo.iter_commits())
        first_commit = list(reversed(all_commits))[0]
        first_commit_hash = first_commit.hexsha[:7]
        start_tag = f"git-mastery-start-{first_commit_hash}"
        self.repo.create_tag(start_tag)


class GitAutograderTest:
    def __init__(
        self,
        exercise_name: str,
        grade_func: Callable[[GitAutograderExercise], GitAutograderOutput],
        clone_from: Optional[str] = None,
        mock_answers: Optional[Dict[str, str]] = None,
        include_remote_repo: bool = False,
    ) -> None:
        self.exercise_name = exercise_name
        self.grade_func = grade_func
        self.clone_from = clone_from
        self.mock_answers = mock_answers
        self.include_remote_repo = include_remote_repo
        self.__rs: Optional[RepoSmith] = None
        self.__rs_remote: Optional[RepoSmith] = None
        self.__rs_context: Optional[ContextManager[RepoSmith]] = None
        self.__rs_remote_context: Optional[ContextManager[RepoSmith]] = None
        self.__temp_dir: Optional[tempfile.TemporaryDirectory] = None
        self.__remote_temp_dir: Optional[tempfile.TemporaryDirectory] = None
        self.__patches: List[mock._patch] = []

    @property
    def rs(self) -> RepoSmith:
        assert self.__rs is not None
        return self.__rs

    @property
    def rs_remote(self) -> Optional[RepoSmith]:
        return self.__rs_remote

    def run(self) -> GitAutograderOutput:
        output: Optional[GitAutograderOutput] = None
        started_at = datetime.now(tz=pytz.UTC)
        try:
            assert self.__temp_dir is not None
            autograder = GitAutograderExercise(exercise_path=self.__temp_dir.name)
            output = self.grade_func(autograder)
        except (
            GitAutograderInvalidStateException,
            GitAutograderWrongAnswerException,
        ) as e:
            output = GitAutograderOutput(
                exercise_name=self.exercise_name,
                started_at=started_at,
                completed_at=datetime.now(tz=pytz.UTC),
                comments=[e.message] if isinstance(e.message, str) else e.message,
                status=(
                    GitAutograderStatus.ERROR
                    if isinstance(e, GitAutograderInvalidStateException)
                    else GitAutograderStatus.UNSUCCESSFUL
                ),
            )
        except Exception as e:
            # Unexpected exception
            output = GitAutograderOutput(
                exercise_name=self.exercise_name,
                started_at=None,
                completed_at=None,
                comments=[str(e)],
                status=GitAutograderStatus.ERROR,
            )

        assert output is not None
        return output

    def __enter__(self) -> Tuple[Self, RepoSmith, RepoSmith | None]:
        # We will mock all accesses to the config to avoid reading the file itself
        # Only the exercise name and repo_name matters, everything else isn't used
        repo_name = "repo"
        fake_config = ExerciseConfig(
            exercise_name=self.exercise_name,
            tags=[],
            requires_git=True,
            requires_github=True,
            base_files={},
            exercise_repo=ExerciseConfig.ExerciseRepoConfig(
                repo_type="local",
                repo_name=repo_name,
                repo_title=None,
                create_fork=None,
                init=True,
                pr_number=None,
                pr_repo_full_name=None,
            ),
            downloaded_at=None,
        )

        answers = [(q, a) for q, a in (self.mock_answers or {}).items()]
        fake_answers = GitAutograderAnswers(
            questions=[v[0] for v in answers],
            answers=[v[1] for v in answers],
            validations={},
        )

        self.__temp_dir = tempfile.TemporaryDirectory()
        assert self.__temp_dir is not None
        read_config_patch = mock.patch(
            "git_autograder.exercise_config.ExerciseConfig.read_config",
            return_value=fake_config,
        )
        has_exercise_config_patch = mock.patch(
            "git_autograder.exercise.GitAutograderExercise.has_exercise_config",
            return_value=True,
        )
        answers_mock_property = mock.patch.object(
            GitAutograderExercise, "answers", new_callable=mock.PropertyMock
        )
        read_config_patch.start()
        has_exercise_config_patch.start()
        answers_mock = answers_mock_property.start()
        answers_mock.return_value = fake_answers
        self.__patches.append(read_config_patch)
        self.__patches.append(has_exercise_config_patch)
        self.__patches.append(answers_mock_property)

        # Create the solution directory named "repo" (name does not matter)
        temp_path = Path(self.__temp_dir.name)
        repo_path = temp_path / repo_name
        os.makedirs(repo_path, exist_ok=True)
        # Force change directory within this context to ensure that we're able to
        # run all commands within the repo
        os.chdir(repo_path)

        if self.clone_from is not None:
            self.__rs_context = create_repo_smith(
                False,
                existing_path=repo_path.absolute().as_posix(),
                clone_from=self.clone_from,
            )
        else:
            self.__rs_context = create_repo_smith(
                False,
                existing_path=repo_path.absolute().as_posix(),
            )
        self.__rs = self.__rs_context.__enter__()
        self.__rs.add_helper(GitMasteryHelper)

        if self.include_remote_repo:
            self.__remote_temp_dir = tempfile.TemporaryDirectory()
            remote_temp_path = Path(self.__remote_temp_dir.name)
            remote_repo_path = remote_temp_path / repo_name
            os.makedirs(remote_repo_path, exist_ok=True)
            self.__rs_remote_context = create_repo_smith(
                False, existing_path=remote_repo_path.absolute().as_posix()
            )
            self.__rs_remote = self.__rs_remote_context.__enter__()
            self.__rs_remote.add_helper(GitMasteryHelper)

        return self, self.rs, self.rs_remote

    def __exit__(
        self,
        exc_type: type | None,
        exc_val: BaseException | None,
        exc_tb: object | None,
    ) -> None:
        for patch in self.__patches:
            patch.stop()

        if self.__rs and self.__rs.repo:
            self.__rs.repo.close()
        if self.__rs_remote and self.__rs_remote.repo:
            self.__rs_remote.repo.close()

        if self.__rs_context is not None:
            self.__rs_context.__exit__(exc_type, exc_val, None)

        if self.__rs_remote_context is not None:
            self.__rs_remote_context.__exit__(exc_type, exc_val, None)

        if self.__temp_dir is not None:
            os.chdir(Path(self.__temp_dir.name).parent)
            self.__temp_dir.cleanup()

        if self.__remote_temp_dir is not None:
            self.__remote_temp_dir.cleanup()


class GitAutograderTestLoader:
    def __init__(
        self,
        exercise_name: str,
        grade_func: Callable[[GitAutograderExercise], GitAutograderOutput],
    ) -> None:
        self.exercise_name = exercise_name
        self.grade_func = grade_func

    @overload
    def start(
        self,
        clone_from: Optional[str] = None,
        mock_answers: Optional[Dict[str, str]] = None,
        include_remote_repo: Literal[False] = False,
    ) -> ContextManager[Tuple[GitAutograderTest, RepoSmith]]: ...

    @overload
    def start(
        self,
        clone_from: Optional[str] = None,
        mock_answers: Optional[Dict[str, str]] = None,
        *,
        include_remote_repo: Literal[True],
    ) -> ContextManager[Tuple[GitAutograderTest, RepoSmith, RepoSmith]]: ...

    @contextmanager
    def start(
        self,
        clone_from: Optional[str] = None,
        mock_answers: Optional[Dict[str, str]] = None,
        include_remote_repo: bool = False,
    ) -> Iterator[Any]:
        test = GitAutograderTest(
            self.exercise_name,
            self.grade_func,
            clone_from,
            mock_answers,
            include_remote_repo,
        )
        if include_remote_repo:
            with test as (ctx, rs, rs_remote):
                yield ctx, rs, rs_remote
        else:
            # extract only rs if include_remote_repo is False
            with test as (ctx, rs, rs_remote):
                yield ctx, rs

    @contextmanager
    def start_mock_exercise(
        self,
        *,
        tags: Optional[List[str]] = None,
        requires_git: bool = True,
        requires_github: bool = True,
        base_files: Optional[Dict[str, str]] = None,
        repo_type: str = "local",
        repo_name: str = "ignore-me",
        init: bool = True,
        create_fork: Optional[bool] = None,
        repo_title: Optional[str] = None,
        has_pr_context: bool = False,
        pr_number: Optional[int] = None,
        pr_repo_full_name: Optional[str] = None,
        downloaded_at: Optional[str] = None,
    ) -> Iterator[GitAutograderExercise]:
        with tempfile.TemporaryDirectory() as temp_dir:
            exercise_path = Path(temp_dir)
            repo_dir = exercise_path / repo_name
            repo_dir.mkdir(parents=True, exist_ok=True)

            if repo_type == "local":
                repo_dir.mkdir(parents=True, exist_ok=True)
                if init:
                    Repo.init(repo_dir)

            exercise_repo: Dict[str, Any] = {
                "repo_type": repo_type,
                "repo_name": repo_name,
                "init": init,
                "create_fork": create_fork,
                "repo_title": repo_title,
            }
            config: Dict[str, Any] = {
                "exercise_name": self.exercise_name,
                "tags": tags or [],
                "requires_git": requires_git,
                "requires_github": requires_github,
                "base_files": base_files or {},
                "exercise_repo": exercise_repo,
                "downloaded_at": downloaded_at,
            }

            if has_pr_context:
                # If the user does not provide PR context, dummy values will be used.
                if pr_number is None:
                    pr_number = 1
                if pr_repo_full_name is None:
                    pr_repo_full_name = "dummy/repo"
                exercise_repo["pr_number"] = pr_number
                exercise_repo["pr_repo_full_name"] = pr_repo_full_name
            with open(exercise_path / ".gitmastery-exercise.json", "w") as f:
                json.dump(config, f)

            if has_pr_context:
                with mock.patch(
                    "git_autograder.pr.fetch_pull_request_data",
                    return_value={},
                ):
                    yield GitAutograderExercise(exercise_path=exercise_path)
            else:
                yield GitAutograderExercise(exercise_path=exercise_path)


def assert_output(
    output: GitAutograderOutput,
    expected_status: GitAutograderStatus,
    expected_comments: List[str] = [],
) -> None:
    assert output.status == expected_status
    assert len(set(output.comments or []) & set(expected_comments)) == len(
        expected_comments
    )
