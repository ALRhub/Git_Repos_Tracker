import inspect
from typing import Dict
from typing import Tuple

from git import Repo

import git_repos_tracker.util as util


class GitReposTracker:
    def __init__(self, register_func):
        self.repo_path_dict = register_func()

    @staticmethod
    def print_repo_status(git_status: dict, git_commits: dict):
        util.print_wrap_title("Current repository status")
        for repo_key, repo_status in git_status.items():
            if repo_status["clean"]:
                is_clean = ": Clean"
                util.print_line_title(repo_key + is_clean)
                print(f"branch: {repo_status['branch']}")
                print(f"commit: {git_commits[repo_key]}")
            else:
                is_clean = ": Dirty !!!"
                util.print_line_title(repo_key + is_clean)
                for status_key, status_value in repo_status.items():
                    if status_key != "clean":
                        print(f"{status_key}: {status_value}")

        util.print_wrap_title("End of checking repository status")

    def check_clean_git_status(self,
                               check_untracked: bool = True,
                               check_detached: bool = True,
                               print_result: bool = False) -> Tuple[bool, Dict]:
        """
        Check if all repositories are in a clean state without modified files

        Args:
            check_untracked: if check untracked files in a certain repository
            check_detached: if check detached Head in a certain repository
            print_result: print checking result or not

        Returns:
            is_clean: True if all repositories are equivalent to the latest commit
            repo_status_dict: details of the all git repositories' status
        """
        repo_path_dict = self.repo_path_dict
        is_clean = True
        repo_status_dict = dict()

        for repo_name, repo_path in repo_path_dict.items():
            repo = Repo(repo_path)
            assert not repo.bare
            repo_status = dict()
            is_this_repo_clean = True
            repo_status["path"] = repo_path
            try:
                branch = repo.active_branch
            except TypeError:
                branch = repo.head.commit
                if check_detached:
                    is_this_repo_clean = False
                    is_clean = False

            repo_status["branch"] = branch
            repo_head_commit = repo.head.commit

            num_staged = len(repo_head_commit.diff())
            num_modified = len(repo_head_commit.diff(None))
            num_untracked = len(repo.untracked_files)

            # Not clean if one of these conditions is satisfied:
            # - Stage but not committed yet
            # - Modified but not staged yet
            # - Check untracked files and indeed found some untracked file
            if num_staged != 0 or num_modified != 0 \
                    or (check_untracked and num_untracked != 0):
                is_this_repo_clean = False
                is_clean = False

            # Save repository state
            repo_status["num_staged"] = num_staged
            repo_status["num_modified"] = num_modified
            repo_status["num_untracked"] = num_untracked
            repo_status["clean"] = is_this_repo_clean

            repo_status_dict[repo_name] = repo_status
        if print_result:
            self.print_repo_status(repo_status_dict,
                                   self.get_git_repo_commits())

        return is_clean, repo_status_dict

    def get_git_repo_commits(self, ) -> Dict:
        """
        Returns: the head commits of all repositories
        """
        repo_path_dict = self.repo_path_dict
        repo_commit_dict = dict()

        for repo_name, repo_path in repo_path_dict.items():
            repo = Repo(repo_path)
            assert not repo.bare
            # Save repository commits
            repo_commit_dict[repo_name] = str(repo.head.commit)

        return repo_commit_dict

    def checkout_git_commits(self, commits_dict: Dict):
        """
        Checkout repositories to given commits
        Args:
            commits_dict: the dictionary mapping repos to commits

        Returns:
            None
        """
        repo_path_dict = self.repo_path_dict
        for repo_name in commits_dict.keys():
            repo_path = repo_path_dict[repo_name]
            repo = Repo(repo_path)
            assert not repo.bare
            assert not repo.is_dirty(), \
                f"Clean the repo {repo_name} before checkout."
            repo.head.reference = repo.commit(commits_dict[repo_name])
            repo.head.reset(index=True, working_tree=True)
            assert repo.head.is_detached
            print(
                f"{repo_name}: Head is now at commit {commits_dict[repo_name]}")

    def checkout_git_branches(self, branch_dict: Dict):
        """
        Checkout repositories to given branches
        Args:
            branch_dict: the dictionary mapping repos to branches

        Returns:
            None
        """
        repo_path_dict = self.repo_path_dict
        for repo_name in branch_dict.keys():
            repo_path = repo_path_dict[repo_name]
            repo = Repo(repo_path)
            assert not repo.bare
            assert not repo.is_dirty(), \
                f"Clean the repo {repo_name} before checkout."
            eval("repo.heads." + f"{branch_dict[repo_name]}" + ".checkout()")
            assert not repo.head.is_detached
            print(
                f"{repo_name}: Head is now at branch {branch_dict[repo_name]}")
