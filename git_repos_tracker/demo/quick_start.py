"""
    A quick start demo to show how it works
"""
import inspect
import git_repos_tracker.util as util
import git_repos_tracker.tracker


def register() -> dict:
    """
    Get pre-registered modules' repository path

    Returns:
        path to the repositories

    """
    module_path_dict = dict()
    repo_path_dict = dict()

    ############################################################################
    # TODO BY YOU: Import the package and locate its path,
    #  Just replace the package like cw2 in the example to your package name
    # Make sure these packages are installed by pip install -e .

    import cw2
    module_path_dict["cw2"] = inspect.getfile(cw2)

    import mp_pytorch
    module_path_dict["mp_pytorch"] = inspect.getfile(mp_pytorch)

    ############################################################################

    # Keep these following codes unchanged
    for module_name, path in module_path_dict.items():
        if "site-packages" in path:
            raise RuntimeError(f"Module {module_name} is in site_packages, "
                               f"thus cannot track its repository.")
        repo_path_dict[module_name] = util.dir_go_up(num_level=2,
                                                     current_file_dir=path)

    return repo_path_dict


def my_cool_experiment():
    """
    Your cool experiment code, can be anything
    Returns:
        Unknown

    """
    pass


if __name__ == "__main__":
    # Instantiate the tracker with your registered function
    tracker = git_repos_tracker.tracker.GitReposTracker(register_func=register)

    # Check cleanness of all registered repositories
    is_clean, repo_status_dict = \
        tracker.check_clean_git_status(print_result=True)

    # You can print or log this git repos commits as you wish
    print(tracker.get_git_repo_commits())

    # Some helper function to enforce clean run but tolerate dirty debug:
    if not util.is_debugging() and not is_clean:
        raise RuntimeError("I am running but I am not clean.")

    else:
        # Run your experiment
        my_cool_experiment()
        print("my experiment is running...")