"""Structures containing different game settings required for the aimbot."""
from dataclasses import dataclass

degrees = float

@dataclass
class AspectRatio:
    """Represents the aspect ratio of a game (for instance 16:9)"""
    width: int
    height: int

@dataclass
class GameSettings:
    """Represents different useful settings of a game."""
    screen_width: int
    screen_height: int
    horizontal_fov: degrees
    vertical_fov: degrees
    yaw: float #in degrees/pixel
    sensitivity: float
