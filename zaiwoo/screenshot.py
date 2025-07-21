"""Utility to take a screenshot of a window and save the pixels inside a numpy HWC array with BGR channels (0-255)."""

import ctypes as ct

import numpy as np
import numpy.typing as npt

from . import window

class ScreenshotException(Exception):
    """An error that happened while trying to take a screenshot."""
    def __init__(self, error_message: str):
        super().__init__(self, error_message)

def take(window_handle: window.Handle) -> npt.NDArray[np.uint8]:
    """Takes a screenshot of the window whose handle is window_handle and returns the pixels in a numpy array of shape (height, width, 3) (in BGR order)."""
    user32 = ct.windll.user32
    gdi32  = ct.windll.gdi32

    # capture screen
    window_dc = user32.GetWindowDC(window_handle)
    if window_dc == 0:
        raise ScreenshotException("Couldn't get the DC for the requested window.")

    in_memory_dc = gdi32.CreateCompatibleDC(window_dc)
    if in_memory_dc == 0:
        raise ScreenshotException("Couldn't create a in-memory DC.")

    width, height = window.dimensions(window_handle)

    bitmap = gdi32.CreateCompatibleBitmap(window_dc, width, height)
    if bitmap == 0:
        raise ScreenshotException("Couldn't create a compatible bitmap.")

    HGDI_ERROR = 0xFFFFFFFF

    selection_result = gdi32.SelectObject(in_memory_dc, bitmap)
    if selection_result == 0 or selection_result == HGDI_ERROR:
        raise ScreenshotException("Couldn't select an object.")

    SRCCOPY = 0x00CC0020

    blit_result = gdi32.BitBlt(in_memory_dc, 0, 0, width, height, window_dc, 0, 0, SRCCOPY)
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
    user32.ReleaseDC(window_dc)
    gdi32.DeleteDC(in_memory_dc)
    gdi32.DeleteObject(bitmap)

    return np_array
