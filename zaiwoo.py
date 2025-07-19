from ultralytics import YOLO

model = YOLO("yolo11n.pt")

source = "screen"

model.predict("https://ultralytics.com/images/bus.jpg", save=True, imgsz=320, conf=0.5, device="cuda")