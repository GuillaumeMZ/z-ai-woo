"""Utilities to interact with monitors."""
import ctypes as ct

def dimensions() -> tuple[int, int]:
    """Returns the dimensions of the primary monitor in a tuple. """
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    return (
        ct.windll.user32.GetSystemMetrics(SM_CXSCREEN),
        ct.windll.user32.GetSystemMetrics(SM_CYSCREEN),
    )
