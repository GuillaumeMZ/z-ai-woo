"""Utilities to move the mouse automatically."""

import ctypes as ct

def move_relative(delta_x: int, delta_y: int) -> None:
    """Moves the mouse relatively to its current position. Parameters delta_x and delta_y are in pixels."""
    class MouseInput(ct.Structure):
        "Mapping to the WINAPI's MOUSEINPUT structure."
        _fields_ = [
            ('dx', ct.c_long),
            ('dy', ct.c_long),
            ('mouseData', ct.c_ulong),
            ('dwFlags', ct.c_ulong),
            ('time', ct.c_ulong),
            ('dwExtraInfo', ct.c_void_p),
        ]

    class Input(ct.Structure):
        "Mapping to the WINAPI's INPUT structure."
        _fields_ = [
            ('type', ct.c_ulong),
            ('mouseInput', MouseInput), #since MOUSEINPUT is bigger in size than KEYBDINPUT and HARDWAREINPUT, doing that (not using a union) is ok
        ]

    INPUT_MOUSE = 0
    MOUSEEVENTF_MOVE = 1

    input_ = Input(INPUT_MOUSE, MouseInput(
        dx=delta_x,
        dy=delta_y,
        mouseData=0,
        dwFlags=MOUSEEVENTF_MOVE,
        time=0,
        dwExtraInfo=None
    ))

    ct.windll.user32.SendInput(1, ct.pointer(input_), ct.sizeof(input_))
