"""The main zAIwoo algorithm."""

from dataclasses import dataclass
from enum import Enum
import math

from ultralytics import YOLO

from .game_settings import AspectRatio, GameSettings
from . import game_math, mouse, screenshot, window

class Target(Enum):
    """Who zAIwoo must target."""
    TERRORIST = 0
    COUNTERTERRORIST = 1
    BOTH = 2

@dataclass
class Settings:
    """Settings coming from the UI."""
    csgo_handle: window.Handle
    zaiwoo_model: YOLO
    in_game_sensitivity: float
    confidence_threshold: float
    target: Target

class ResultClassType(Enum):
    """The category of a detection result (Counter-terrorist, counter-terrorist head, terrorist, terrorist head)"""
    CT = 0
    CT_HEAD = 1
    T = 2
    T_HEAD = 3

@dataclass
class Result:
    """The result of a detection."""
    x: int
    y: int
    w: int
    h: int
    result_type: ResultClassType
    confidence: float

def _rectangle_middle(x: int, y: int, w: int, h: int) -> tuple[int, int]:
    """Computes the coordinates of the middle of a rectangle."""
    return (int(x + (w / 2)), int(y + (h / 2)))

def _closest(results: list[Result], game_settings: GameSettings) -> Result:
    """Finds the closest bounding box of the center of the screen."""
    min_distance = math.inf
    minimum = None

    center = [game_settings.screen_width / 2, game_settings.screen_height / 2]

    for result in results:
        result_middle_x, result_middle_y = _rectangle_middle(result.x, result.y, result.w, result.h)
        current_distance = math.dist(center, [result_middle_x, result_middle_y])
        if current_distance < min_distance:
            min_distance = current_distance
            minimum = result

    if minimum is None:
        raise Exception("Unreachable: results always has at least 1 element.")

    return minimum

def _to_clean_result(source_result) -> list[Result]:
    """Converts a YOLO result into a legible result."""
    result: list[Result] = []
    
    bounding_boxes = source_result.boxes.xywh.tolist()
    classes = source_result.boxes.cls.tolist()
    confidences = source_result.boxes.conf.tolist()

    for i, bounding_box in enumerate(bounding_boxes):
        result.append(Result(
            x=bounding_box[0],
            y=bounding_box[1],
            w=bounding_box[2],
            h=bounding_box[3],
            result_type=ResultClassType(classes[i]),
            confidence=confidences[i]
        ))

    return result

def _is_same_type(class_type: ResultClassType, target: Target) -> bool:
    if target == Target.BOTH:
        return True

    if target == Target.TERRORIST and class_type in (ResultClassType.T, ResultClassType.T_HEAD):
        return True

    if target == Target.COUNTERTERRORIST and class_type in (ResultClassType.CT, ResultClassType.CT_HEAD):
        return True

    return False

def run(settings: Settings):
    "Run zAIwoo"
    def inner() -> None:
        CSGO_VFOV = 74
        CSGO_YAW = 0.022

        csgo_width, csgo_height = window.dimensions(settings.csgo_handle)
        aspect_ratio = AspectRatio(csgo_width, csgo_height)

        game_settings = GameSettings(
            screen_width=csgo_width,
            screen_height=csgo_height,
            horizontal_fov=game_math.vfov_to_hfov(CSGO_VFOV, aspect_ratio),
            vertical_fov=CSGO_VFOV,
            yaw=CSGO_YAW,
            sensitivity=settings.in_game_sensitivity
        )

        screen = screenshot.take(settings.csgo_handle)

        results = _to_clean_result(settings.zaiwoo_model(screen, verbose=False)[0])
        acceptable_results = [result for result in results if result.confidence >= settings.confidence_threshold]
        targetable_results = [result for result in acceptable_results if _is_same_type(result.result_type, settings.target)]

        if not targetable_results:
            return

        closest_box = _closest(targetable_results, game_settings)

        delta_x, delta_y = (int(closest_box.x - (game_settings.screen_width / 2)), int(closest_box.y - (game_settings.screen_height / 2)))
        effective_delta_x = game_math.distance_to_effective_pixels(delta_x, game_math.DistanceType.HORIZONTAL, game_settings)
        effective_delta_y = game_math.distance_to_effective_pixels(delta_y, game_math.DistanceType.VERTICAL, game_settings)

        mouse.move_relative(effective_delta_x, effective_delta_y)
    return inner
