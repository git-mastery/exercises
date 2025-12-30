from repo_smith.repo_smith import RepoSmith

__requires_git__ = True
__requires_github__ = False


def download(rs: RepoSmith):
    rs.git.run(
        ["git", "clone", "https://github.com/git-mastery/samplerepo-finances.git"]
    )
    rs.files.cd("samplerepo-finances")
    rs.git.run(
        [
            "git",
            "remote",
            "set-url",
            "origin",
            "https://github.com/git-mastery/samplerepo-finances-2.git",
        ],
    )
