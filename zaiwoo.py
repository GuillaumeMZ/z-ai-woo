from ultralytics import YOLO

import screenshot

model = YOLO("yolo11n.pt")

source = screenshot.take()

model.predict(source, save=True, imgsz=320, conf=0.5, device="cuda")