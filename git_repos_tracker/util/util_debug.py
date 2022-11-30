"""
    Utilities of debug mode
"""
import sys

def is_debugging():
    """
    Check if program is running by a debugger
    Returns: True if in debugging mode

    """
    get_trace = getattr(sys, 'gettrace', None)
    return get_trace()
