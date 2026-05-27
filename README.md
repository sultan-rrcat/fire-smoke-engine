Below is a practical SRS + development guide focused on:

* inference only
* your trained YOLO model
* basic temporal decision engine
* CCTV-ready architecture later
* fast MVP delivery

---

# Smoke Detection Surveillance System

# Software Requirements Specification (SRS)

## Version 1.0

---

# 1. Project Overview

## Objective

Build a web-based smoke detection surveillance application that:

* uploads videos
* runs YOLO smoke detection inference
* applies a basic decision engine
* visualizes detections
* generates annotated videos
* stores events locally
* is architected for future CCTV/RTSP deployment

---

# 2. Tech Stack

| Layer            | Technology              |
| ---------------- | ----------------------- |
| Frontend         | React                   |
| Backend API      | FastAPI                 |
| AI Inference     | PyTorch + YOLO          |
| Video Processing | OpenCV                  |
| Storage          | Local filesystem        |
| State Management | React Context / Zustand |
| Communication    | REST API                |
| Visualization    | Recharts                |
| Deployment       | Docker (later phase)    |

---

# 3. Scope (Phase 1 MVP)

## Included

### Frontend

* video upload
* processing status
* video playback
* annotated playback
* detection timeline
* confidence graph
* event listing

### Backend

* video upload endpoint
* frame extraction
* YOLO inference
* basic decision engine
* annotated video generation
* event generation
* result storage

### AI

* load pretrained YOLO model
* frame-wise inference
* confidence thresholding
* temporal consensus logic

---

## Excluded (Later)

* RTSP streaming
* multi-camera support
* user authentication
* cloud deployment
* segmentation models
* ConvLSTM
* distributed GPU workers
* notification system
* thermal fusion

---

# 4. System Architecture

```text id="7y2y7n"
Frontend (React)
        ↓
FastAPI Backend
        ↓
Inference Pipeline
        ↓
Decision Engine
        ↓
Results Storage
        ↓
Frontend Visualization
```

---

# 5. Functional Requirements

# 5.1 Video Upload

## Description

User uploads a video file for smoke analysis.

## Supported Formats

* mp4
* avi
* mov

## Constraints

* max size: 500MB initially

## API

```http id="h8fr7i"
POST /upload-video
```

---

# 5.2 Video Processing Pipeline

## Description

Backend processes uploaded video frame-by-frame.

## Workflow

```text id="6m0q7u"
Video Upload
    ↓
Save Video
    ↓
Extract Frames
    ↓
YOLO Inference
    ↓
Decision Engine
    ↓
Generate Events
    ↓
Generate Annotated Video
```

---

# 5.3 YOLO Inference

## Description

Run trained YOLO model on extracted frames.

## Output Per Frame

```json id="i5k5vw"
{
  "frame_number": 123,
  "timestamp": 4.1,
  "detections": [
    {
      "class": "smoke",
      "confidence": 0.82,
      "bbox": [x1, y1, x2, y2]
    }
  ]
}
```

---

# 5.4 Basic Decision Engine

## Purpose

Reduce false positives using temporal logic.

---

## Logic

Instead of:

```python id="0qgsj9"
if smoke_detected:
    trigger_alert()
```

Use:

```python id="6bmrf7"
if smoke_detected_in_last_12_frames >= 8:
    trigger_alert()
```

---

## Configurable Parameters

| Parameter               | Default |
| ----------------------- | ------- |
| confidence_threshold    | 0.5     |
| consensus_window        | 12      |
| minimum_positive_frames | 8       |
| cooldown_seconds        | 10      |

---

# 5.5 Event Generation

## Description

Create smoke events.

## Event Object

```json id="ki59cr"
{
  "event_id": "uuid",
  "start_time": 12.3,
  "end_time": 18.7,
  "max_confidence": 0.91,
  "event_type": "smoke"
}
```

---

# 5.6 Annotated Video Generation

## Description

Generate output video with:

* bounding boxes
* confidence scores
* alert state

---

# 5.7 Timeline Visualization

## Description

Frontend displays:

* detection confidence over time
* alert intervals
* smoke events

---

# 6. Non-Functional Requirements

# Performance

| Requirement          | Target                    |
| -------------------- | ------------------------- |
| Upload Response      | <2 sec                    |
| Frame Inference      | Real-time capable         |
| UI Responsiveness    | Smooth playback           |
| Processing Stability | No crashes on long videos |

---

# Scalability

Architecture must support:

* RTSP later
* multi-stream later
* GPU workers later

---

# Reliability

* recover gracefully on invalid videos
* no backend crash on inference failure

---

# Maintainability

Keep:

* inference engine modular
* decision engine isolated
* frontend independent

---

# 7. Frontend Specification

# Pages

---

# 7.1 Upload Page

## Components

* drag & drop upload
* upload progress
* submit button

---

# 7.2 Processing Page

## Components

* processing spinner
* current frame progress
* inference statistics

---

# 7.3 Results Dashboard

## Components

### Video Player

* original video
* annotated video

### Detection Timeline

* smoke confidence graph

### Event Panel

* smoke event list
* timestamps

### Statistics Panel

* total detections
* max confidence
* total alert duration

---

# 8. Backend Specification

# Folder Structure

```text id="k3bl9r"
backend/
│
├── app/
│   ├── api/
│   ├── core/
│   ├── inference/
│   ├── decision_engine/
│   ├── services/
│   ├── utils/
│   └── models/
│
├── uploads/
├── outputs/
├── events/
└── main.py
```

---

# 9. Frontend Folder Structure

```text id="5r7mwb"
frontend/
│
├── src/
│   ├── pages/
│   ├── components/
│   ├── services/
│   ├── hooks/
│   ├── store/
│   └── utils/
```

---

# 10. API Design

# Upload Video

```http id="r9fjlwm"
POST /upload-video
```

Response:

```json id="4ohd1u"
{
  "video_id": "uuid",
  "status": "uploaded"
}
```

---

# Start Processing

```http id="vibd2h"
POST /process-video/{video_id}
```

---

# Get Processing Status

```http id="l7e74g"
GET /status/{video_id}
```

---

# Get Results

```http id="7qnhkg"
GET /results/{video_id}
```

---

# Get Events

```http id="vjy7zl"
GET /events/{video_id}
```

---

# Download Annotated Video

```http id="dclv3y"
GET /download/{video_id}
```

---

# 11. Decision Engine Design

# Input

Frame detections.

---

# Processing

Maintain rolling buffer:

```python id="4i3zlg"
deque(maxlen=12)
```

---

# Example

```python id="0p46df"
detections = [1,1,1,0,1,1,1,1,0,1,1,1]

if sum(detections) >= 8:
    trigger_alert()
```

---

# Future Extensibility

Decision engine should later support:

* temporal AI
* motion analysis
* segmentation confidence
* tracking persistence

---

# 12. Local Storage Design

# uploads/

Original uploaded videos.

---

# outputs/

Annotated videos.

---

# events/

JSON event files.

---

# detections/

Per-frame inference results.

---

# Example Structure

```text id="knc0a6"
storage/
│
├── uploads/
├── outputs/
├── events/
└── detections/
```

---

# 13. YOLO Integration

# Model Loading

```python id="dkkvqi"
from ultralytics import YOLO

model = YOLO("best.pt")
```

---

# Inference

```python id="v6b5qp"
results = model(frame)
```

---

# Detection Extraction

```python id="0op5hm"
for box in results[0].boxes:
    confidence = float(box.conf[0])
```

---

# 14. Recommended Development Phases

# Phase 1 — Core MVP

## Goal

Basic smoke detection app.

## Deliverables

* upload video
* YOLO inference
* annotated output
* basic decision engine

---

# Phase 2 — Visualization Upgrade

## Deliverables

* confidence graph
* timeline
* event replay
* frame statistics

---

# Phase 3 — CCTV Readiness

## Deliverables

* RTSP input abstraction
* stream architecture
* async processing

---

# Phase 4 — Accuracy Upgrade

## Deliverables

* motion filtering
* segmentation
* temporal AI
* tracking

---

# 15. Suggested Development Order

# Week 1

Backend:

* upload API
* frame extraction
* YOLO inference

Frontend:

* upload UI
* processing UI

---

# Week 2

Backend:

* decision engine
* event generation
* annotated video

Frontend:

* results dashboard
* playback

---

# Week 3

Frontend:

* confidence graph
* timeline

Backend:

* performance optimization

---

# 16. Future CCTV Migration Plan

Current:

```text id="l5v4rz"
uploaded video
```

Future:

```text id="9k1br0"
RTSP stream
```

Because architecture is stream-based internally:
no major rewrite required.

---

# 17. Critical Engineering Rules

# DO NOT

* tightly couple frontend and inference
* run inference in request thread
* hardcode thresholds everywhere
* store everything in memory

---

# ALWAYS

* isolate decision engine
* store structured events
* keep inference modular
* design for streaming internally

---

# 18. Recommended Immediate Folder Setup

```text id="j4mbgk"
project-root/
│
├── frontend/
├── backend/
├── storage/
│   ├── uploads/
│   ├── outputs/
│   ├── events/
│   └── detections/
│
└── models/
    └── best.pt
```

---

# 19. Immediate Next Tasks

# Backend

* create FastAPI server
* add upload endpoint
* load YOLO model
* process frames

---

# Frontend

* React upload page
* results dashboard
* annotated video playback

---

# 20. Final Architecture Goal

Eventually your system becomes:

```text id="mnn5e9"
CCTV Stream
    ↓
Inference Engine
    ↓
Decision Engine
    ↓
Event Engine
    ↓
Alert System
    ↓
Operator Dashboard
```

Your MVP should already mimic this structure internally.
