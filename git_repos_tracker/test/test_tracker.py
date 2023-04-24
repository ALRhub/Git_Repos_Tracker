import inspect

import git_repos_tracker.util as util
from git_repos_tracker.tracker import GitReposTracker


def test_get_git_repo_paths():
    util.print_wrap_title("test_get_git_repo_paths")

    repo_path_dict = register()
    for repo, path in repo_path_dict.items():
        print(f"{repo}: {path}")


def test_print_repo_status(tracker: GitReposTracker):
    util.print_wrap_title("test_print_repo_status")
    is_clean, repo_status_dict = tracker.check_clean_git_status(True)
    tracker.print_repo_status(repo_status_dict, tracker.get_git_repo_commits())


def test_check_clean_git_status(tracker: GitReposTracker):
    util.print_wrap_title("test_check_clean_git_status")
    is_clean, repo_status_dict = tracker.check_clean_git_status(True)
    print(f"is_clean: {is_clean}")
    print(f"repo_status_dict: {repo_status_dict}")


def test_get_git_repo_commits(tracker: GitReposTracker):
    util.print_wrap_title("test_get_git_repo_commits")
    commit_dict = tracker.get_git_repo_commits()
    print(commit_dict)


def test_checkout_git_commits(tracker: GitReposTracker):
    util.print_wrap_title("test_checkout_git_commits")
    commit_dict = {"mp_pytorch": "188c5734f4fb81c37fa00b2b31d11f468d77a774"}
    tracker.checkout_git_commits(commit_dict)


def test_checkout_git_branches(tracker: GitReposTracker):
    util.print_wrap_title("test_checkout_git_branches")
    branch_dict = {"mp_pytorch": "main"}
    tracker.checkout_git_branches(branch_dict)


def register() -> dict:
    """
    Get pre-registered modules' repository path

    Returns:
        path to the repositories

    """
    module_path_dict = dict()
    repo_path_dict = dict()

    # Import the package and locate its path
    import cw2
    module_path_dict["cw2"] = inspect.getfile(cw2)
    import mp_pytorch
    module_path_dict["mp_pytorch"] = inspect.getfile(mp_pytorch)

    for module_name, path in module_path_dict.items():
        if "site-packages" in path:
            raise RuntimeError(f"Module {module_name} is in site_packages, "
                               f"thus cannot track its repository.")
        repo_path_dict[module_name] = util.dir_go_up(num_level=2,
                                                     current_file_dir=path)

    return repo_path_dict


def main():
    tracker = GitReposTracker(register_func=register)

    test_get_git_repo_paths()
    test_check_clean_git_status(tracker)
    test_print_repo_status(tracker)
    test_get_git_repo_commits(tracker)
    test_checkout_git_commits(tracker)
    test_checkout_git_branches(tracker)


if __name__ == "__main__":
    main()
