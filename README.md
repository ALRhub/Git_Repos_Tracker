# Git_Repos_Tracker
A lightweight tool to help track versions of multiple editable git repositories in research experiments. 

# Problem statement
Have you ever experienced a problem like:

"Why can't I reproduce the experiment result of two months ago?"

"I am not sure where is the bug, it can be either in my RL code or in the RL environment or in Donald Trump's code."

"Damn, I have already spent one week to locate the bug, but still have no idea where is the problem. And each of the debuting experiment will take me half a day." 

"Finally, I found the problem. My code is fine, but my colleague updated their code version, then my experiment cannot work anymore."

# About this tool
It is to help you track multiple git repositories under development, every time you run an experiment, you can use this tool to log the current commits hashcode of each repository. 

Before you run your experiment seriously, it can check the existence of any uncommitted changes in those repositories and raise an error when there are something dirty (modified files, untracked files). In this case, all these changes must be stored in new commits. So you can enforce yourself to track all code details for your experiment.

When you debug your code, it can tolerate the dirty things, so you can do whatever crazy stuff in debug mode and do not have to save them in commits.

When you reproduce your experiment using your latest code and get failure, you can compare the code with the logged old commits. When you want to see the performance using your old code, this tool can help you checkout all the repositories to the old commits by one function call. 

# Feature
- Automatic locate the path to your repositories. So you can run it in different machines without changing the path to the repositories.
- Check git status of all registered repositories and return them in a dictionary. So you can log it as you wish.
- Enforce you to have cleaned repositories before you run experiment.
- Tolerate to dirties when you simply debug your code.
- Auto checkout to certain commits to help reproduce the results. 
- Auto checkout to certain branches to recover your code bases to the latest state. 

# Usage 
- Make sure the repositories to be tracked are installed through pip, Here -e means your code base is in editable mode: 

```bash 
pip install -e .
```

- Your repository should not be a site-package


- Register your repositories as python packages (see demo/quick_start.py), e.g.:

```python 

def register() -> dict:
    """
    Get pre-registered modules' repository path

    Returns:
        path to the repositories

    """
    module_path_dict = dict()
    repo_path_dict = dict()

    ############################################################################
    
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
```

- Use this register function to instantiate a tracker

```python
tracker = git_repos_tracker.tracker.GitReposTracker(register_func=register)
```

- Run it before you run your experiment code in the main function

```python
is_clean, repo_status_dict = tracker.check_clean_git_status(print_result=True)
```

- You will see some details of your repos:
```bash
************************************************************
*                Current repository status                 *
************************************************************


====================== cw2: Dirty !!! ======================

path: /home/lige/Codes/Git_Repos_Tracker/test_repos/cw2
branch: master
num_staged: 0
num_modified: 1
num_untracked: 0

================== mp_pytorch: Dirty !!! ===================

path: /home/lige/Codes/Git_Repos_Tracker/test_repos/MP_PyTorch
branch: main
num_staged: 0
num_modified: 1
num_untracked: 0

============ End of checking repository status =============
```

- You can enforce all repos to be clean and give tolerance to debugging mode:

```python 
if not util.is_debugging() and not is_clean:
    raise RuntimeError("I am running but I am not clean.")

else:
    # Run your experiment
    my_cool_experiment()
    print("my experiment is running...")
```

- You can log or print the commits code returned by a dictionary
```python
print(tracker.get_git_repo_commits())
```

- You will get:
```bash
{'cw2': '15b52480fc6fac3e6f094dd29f4348c9eb163c50', 
 'mp_pytorch': '5b6d012890c28d20c884b38208ee43d330dac249'}
```

- When you want to reproduce your experiment, you can checkout one or more repos back to the old commits by:
```python
commit_dict = {"mp_pytorch": "188c5734f4fb81c37fa00b2b31d11f468d77a774"}
tracker.checkout_git_commits(commit_dict)
```