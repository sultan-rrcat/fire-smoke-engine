from ultralytics import YOLO
from config import MODEL_PATH
from core.logging import setup_logging

logger = setup_logging()

logger.info(f"Model loading started ... ")
model = YOLO(str(MODEL_PATH))
logger.info(f"Model: {MODEL_PATH} loaded sucessfully.")

def run_inference(frame):
    results = model(frame)
    detections = []
    for box in results[0].boxes:
        confidence = float(box.conf[0])
        if confidence < 0.5:
            continue
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append({
            "confidence":confidence,
            "bbox":[x1, y1, x2, y2]
        })
    return detections
