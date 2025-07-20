"""Utilities to interact with windows."""
import ctypes as ct

Handle = ct.c_void_p

def find_window(window_name: str) -> Handle | None:
    """Finds a window by title. Returns a handle to the window if it exists, and None otherwise."""
    return ct.windll.user32.FindWindowW(None, window_name) or None
