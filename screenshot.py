"""Utility to take a screenshot of the screen and save the pixels inside a numpy HWC array with BGR channels (0-255)."""

import ctypes as ct
import numpy as np
import numpy.typing as npt
import monitor

class ScreenshotException(Exception):
    """An error that happened while trying to take a screenshot."""
    def __init__(self, error_message: str):
        super().__init__(self, error_message)

def take() -> npt.NDArray[np.uint8]:
    """Takes a screenshot of the whole screen and returns the pixels in a numpy array of shape (height, width, 3) (in BGR order)."""
    # capture screen
    screen_dc = ct.windll.user32.GetWindowDC(0)
    if screen_dc == 0:
        raise ScreenshotException("Couldn't get the DC for the requested window.")

    in_memory_dc = ct.windll.gdi32.CreateCompatibleDC(screen_dc)
    if in_memory_dc == 0:
        raise ScreenshotException("Couldn't create a in-memory DC.")

    width, height = monitor.dimensions()

    bitmap = ct.windll.gdi32.CreateCompatibleBitmap(screen_dc, width, height)
    if bitmap == 0:
        raise ScreenshotException("Couldn't create a compatible bitmap.")

    HGDI_ERROR = 0xFFFFFFFF

    selection_result = ct.windll.gdi32.SelectObject(in_memory_dc, bitmap)
    if selection_result == 0 or selection_result == HGDI_ERROR:
        raise ScreenshotException("Couldn't select an object.")

    SRCCOPY = 0x00CC0020

    blit_result = ct.windll.gdi32.BitBlt(in_memory_dc, 0, 0, width, height, screen_dc, 0, 0, SRCCOPY)
    if blit_result == 0:
        raise ScreenshotException("BitBlt failed.")

    byte_count = width * height * 4 # 4 = bgra
    bytes_ = (ct.c_uint8 * byte_count)()
    bits = ct.windll.gdi32.GetBitmapBits(bitmap, byte_count, bytes_)
    if bits == 0:
        raise ScreenshotException("GetBitmapBits failed.")

    # convert to numpy array
    np_array = np.ctypeslib.as_array(bytes_)
    np_array = np_array.reshape((height, width, 4))
    # remove alpha channel
    np_array = np_array[:, :, :3]

    # free resources
    ct.windll.gdi32.DeleteDC(in_memory_dc)
    ct.windll.gdi32.DeleteObject(bitmap)

    return np_array
