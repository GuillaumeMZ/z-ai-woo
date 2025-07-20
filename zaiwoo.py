from ultralytics import YOLO

import screenshot
import window

model = YOLO("yolo11n.pt")

csgo = window.find("Counter-Strike: Global Offensive")
if csgo is None:
    raise Exception("Couldn't find CS:GO.")

source = screenshot.take(csgo)

model.predict(source, save=True, imgsz=320, conf=0.5, device="cuda")