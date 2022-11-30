"""
    Utilities of path and dir operation
"""

import os


def dir_go_up(num_level: int = 2, current_file_dir: str = "default") -> str:
    """
    Go to upper n level of current file directory
    Args:
        num_level: number of level to go up
        current_file_dir: current dir

    Returns:
        dir n level up
    """
    if current_file_dir == "default":
        current_file_dir = os.path.realpath(__file__)
    while num_level != 0:
        current_file_dir = os.path.dirname(current_file_dir)
        num_level -= 1
    return current_file_dir
