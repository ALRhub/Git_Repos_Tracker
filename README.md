# Git_Repos_Tracker
A lightweighted tool to help track versions of multiple editable git repositories in research experiments. 

# Problem statement
Have you ever experienced a problem like:

"Why can't I reproduce the experiment result of two months ago?"

"I am not sure where is the bug, it can be either in the my RL code or in the RL environment or in Donald Trump's code."

"Damn, I have already spent one week to locate the bug, but still have no idea where is the problem. And each of the debuging experiment will take me half a day." 

"Finally, I found the problem. My code is fine, but my colleague updated their code version, then my experiement cannot work anymore."

# About this tool
It is to help you track multiple git repositories under development, every time you run an experiment, you can use this tool to log the current commits hashcode of each repositories. 

Before you run your experiment seriously, it can check the existance of any uncommited changes in those repositories and raise an error when there are something dirty (modified files, untracked files). In this case, all these changes must be stored in new commits. So you can enforce yourself to track all code details for your experiment.

When you debug your code, it can tolerate the dirty things, so you can do whatever crazy stuff in debug mode and do not have to save them in commits.

When you reproduce your experiment using your latest code and get failure, you can compare the code with the logged old commits. When you want to see the performance using your old code, this tool can help you checkout all the repositories to the old commits by one function call. 

# Feature
- Automatic locate the path to your repositories. So you can run it in different machines without changing the path to the repositories.
- Check git status of all registered repositories and return them in a dictionary. So you can log it as you wish.
- Enforce you to have cleaned repositories before you run experiment.
- Torlerate to dirties when you simply debug your code.
- Auto checkout to certain commits to help reproduce the results. 
- Auto checkout to certain branches to recover your code bases to the latest state. 

# Usage 
- Make sure the repositories are installed through: 

```bash 
pip install -e .
```
Here -e means your code base is in editable mode. 

