import cv2
import json
from pathlib import Path
from services.inference_service import run_inference
from services.decision_engine import update_decision
from config import (
    OUTPUT_DIR,
    DETECTION_DIR
)

processing_status = {}

def process_video(video_id, video_path):
    try:
        processing_status[video_id] = "processing"
        cap = cv2.VideoCapture(str(video_path))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fps = cap.get(cv2.CAP_PROP_FPS)

        output_path = OUTPUT_DIR / f"{video_id}.mp4"
        writer = cv2.VideoWriter(
            str(output_path),
            cv2.VideoWriter_fourcc(*"mp4v"),
            fps,
            (width, height)
        )

        detections_data = []
        frame_number = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            detections = run_inference(frame)
            alert = update_decision(len(detections)>0)
            for det in detections:
                x1, y1, x2, y2 = det["bbox"]
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 255),
                    2
                )
                cv2.putText(
                    frame,
                    f"Smoke {det['confidence']:.2f}",
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5,
                    (0, 0, 255),
                    2
                )

            if alert:
                cv2.putText(
                    frame,
                    "SMOKE ALERT",
                    (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    3
                )
            
            writer.write(frame)
            detections_data.append({
                "frame":frame_number,
                "detections":detections,
                "alert":alert
            })

            frame_number += 1

        cap.release()
        writer.release()

        detection_file = DETECTION_DIR / f"{video_id}.json"
        with open(detection_file, "w") as f:
            json.dump(detections_data, f)
        processing_status[video_id]="completed"

    except Exception as e:
        processing_status[video_id] = "failed"
        logger.exception(f"Video processing failed: {e}")