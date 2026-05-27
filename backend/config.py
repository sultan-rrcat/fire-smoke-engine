from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_DIR = BASE_DIR / "uploads"
OUTPUT_DIR = BASE_DIR / "outputs"
EVENT_DIR = BASE_DIR / "events"
DETECTION_DIR = BASE_DIR / "detections"

MODEL_PATH = BASE_DIR / "models" /"yolov26n" / "best.pt"

CONFIDENCE_THRESHOLD = 0.5
CONSENSUS_WINDOW = 12
MIN_POSITIVE_FRAMES = 8
