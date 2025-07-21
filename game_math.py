"""Mathematical utilities for FOV and distance manipulation in 3D video games."""
from enum import Enum
import math

from game_settings import AspectRatio, GameSettings

degrees = float

def tan_deg(deg: degrees) -> float:
    """Computes the tangent of an angle in degrees."""
    return math.tan(math.radians(deg))

def atan_deg(value: float) -> degrees:
    """Computes the arc tangent of a value, returns degrees."""
    return math.degrees(math.atan(value))

def hfov_to_vfov(hfov: degrees, aspect_ratio: AspectRatio) -> degrees:
    """Computes the vertical FOV of a game based on its horizontal FOV hfov."""
    # https://en.wikipedia.org/wiki/Field_of_view_in_video_games
    return 2 * atan_deg(tan_deg(hfov / 2) * (aspect_ratio.height / aspect_ratio.width))

def vfov_to_hfov(vfov: degrees, aspect_ratio: AspectRatio) -> degrees:
    """Computes the vertical FOV of a game based on its horizontal FOV hfov."""
    # https://en.wikipedia.org/wiki/Field_of_view_in_video_games
    return 2 * atan_deg(tan_deg(vfov / 2) * (aspect_ratio.width / aspect_ratio.height))

class DistanceType(Enum):
    """Represents whether a mouse movement is horizontal or vertical."""
    HORIZONTAL = 0
    VERTICAL = 1

def distance_to_effective_pixels(distance: int, distance_type: DistanceType, game_settings: GameSettings) -> int:
    """Compute the number of pixels the mouse must move to go over a distance of distance pixels on the screen."""
    aspect = game_settings.screen_width if distance_type == DistanceType.HORIZONTAL else game_settings.screen_height
    fov = game_settings.horizontal_fov if distance_type == DistanceType.HORIZONTAL else game_settings.vertical_fov

    effective_angle = atan_deg(distance / ((aspect / 2) / tan_deg(fov / 2)))

    # see https://github.com/GuillaumeMZ/understanding-sensitivity to understand the formula
    return int(effective_angle / (game_settings.sensitivity * game_settings.yaw))
