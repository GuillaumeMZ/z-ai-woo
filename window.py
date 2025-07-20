"""Utilities to interact with windows."""
import ctypes as ct

Handle = ct.c_void_p

def find(window_name: str) -> Handle | None:
    """Finds a window by title. Returns a handle to the window if it exists, and None otherwise."""
    return ct.windll.user32.FindWindowW(None, window_name) or None

def dimensions(window_handle: Handle) -> tuple[int, int]:
    """Returns the size of a window in a tuple. The first element of the tuple is the width of the window, so the second is the height."""
    class RECT(ct.Structure):
        """"Mapping to the WINAPI's RECT structure."""
        _fields_ = [
            ('left', ct.c_ulong),
            ('top', ct.c_ulong),
            ('right', ct.c_ulong),
            ('bottom', ct.c_ulong),
        ]

    rect = RECT()

    ct.windll.user32.GetWindowRect(window_handle, ct.pointer(rect))

    return (rect.right - rect.left, rect.bottom - rect.top)
