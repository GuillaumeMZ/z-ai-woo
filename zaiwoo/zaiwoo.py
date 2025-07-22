"""The main zAIwoo algorithm."""

from dataclasses import dataclass

from ultralytics import YOLO

from . import window

@dataclass
class Settings:
    """Settings coming from the UI."""
    csgo_handle: window.Handle
    zaiwoo_model: YOLO
    in_game_sensitivity: float
    confidence_threshold: float


def run(settings: Settings):
    "Run zAIwoo"
    def inner():
        print("zaiwoo...", settings.in_game_sensitivity)

    return inner
