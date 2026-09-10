# Real-Time Object Detection and Tracking System

A real-time computer vision system that detects objects in video and tracks them across frames using YOLOv8 and ByteTrack, built with Python and OpenCV.

## Overview

This project implements a complete pipeline for real-time object detection and multi-object tracking. It captures video (from a webcam or a video file), runs each frame through a pre-trained YOLOv8 model to detect objects, and applies the ByteTrack tracking algorithm to assign each detected object a persistent ID as it moves across frames.

## Features

- **Real-time video input** via OpenCV (webcam or video file)
- **Pre-trained object detection** using YOLOv8 (80 common object classes — person, car, dog, phone, etc.)
- **Bounding box visualization** with class labels and confidence scores
- **Multi-object tracking** using ByteTrack, assigning a persistent ID to each object
- **Live annotated display** showing labels and tracking IDs in real time

## Tech Stack

| Component | Tool / Library |
|---|---|
| Language | Python 3.10 |
| Video I/O & rendering | OpenCV (`opencv-python`) |
| Object detection | YOLOv8 (`ultralytics`) |
| Object tracking | ByteTrack (bundled with `ultralytics`) |
| Matching/assignment backend | `lapx` |

## Model Choice

| Model | Trade-off | Used for |
|---|---|---|
| `yolov8n.pt` (nano) | Fastest, lowest accuracy | Initial testing |
| `yolov8s.pt` (small) | Balanced speed/accuracy on CPU-only hardware | **Final choice** |

`yolov8s.pt` was selected as the best fit for a CPU-only machine (no dedicated GPU), offering noticeably better detection accuracy than the nano model while still running at usable real-time speeds.

## Tracking Choice

**ByteTrack** was chosen over classic SORT/DeepSORT because:
- It is natively integrated into `ultralytics` (`model.track()`), requiring minimal extra code
- It offers strong accuracy-to-speed trade-offs, making it well suited for CPU-only, real-time use
- It belongs to the same tracking-by-detection family as SORT/DeepSORT, satisfying the assignment's tracking requirement

## Installation

### Local Setup (Windows)

```bash
# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
python -m pip install opencv-python ultralytics numpy lapx
```

> **Note:** If you see a `lap` / null-bytes import error, uninstall `lap` and install `lapx` instead — it's a drop-in, better-maintained replacement:
> ```bash
> python -m pip uninstall lap -y
> python -m pip install lapx
> ```

> **Note:** Never move a virtual environment folder after creating it — the `pip.exe` and other launcher scripts contain hardcoded paths and will break. If this happens, use `python -m pip` instead of `pip.exe` directly, or recreate the venv in its final location.

### Google Colab Setup

```python
!pip install ultralytics opencv-python lapx
```

> **Note:** Colab has no display and no direct webcam access, so `cv2.imshow()` and `cv2.VideoCapture(0)` will not work. Use an uploaded video file as the input source instead.

## Usage

```bash
python detection_test.py
```

- Press **`q`** at any time to stop the video feed and close the window.
- Each detected object is displayed with its class label, confidence score, and a persistent tracking ID.

## Troubleshooting Log

| Issue | Cause | Fix |
|---|---|---|
| `ValueError: source code string cannot contain null bytes` on `import lap` | Corrupt/incompatible `lap` installation | Replace with `lapx` |
| `ModuleNotFoundError: No module named 'ultralytics'` despite active venv | `python`/`pip` on PATH pointed to a global install, not the venv | Run `venv\Scripts\python.exe` directly |
| `Fatal error in launcher` when running `pip.exe` | venv folder was moved after creation; launcher scripts have hardcoded paths | Use `python -m pip` instead of `pip.exe` |
| Low detection accuracy with `yolov8n.pt` | Nano model prioritizes speed over accuracy | Switched to `yolov8s.pt` |

## Hardware Used

- CPU: Intel i7 (8th Gen)
- RAM: 16 GB
- GPU: None (CPU-only inference)

## Possible Future Improvements

- Support for saving annotated output to a video file
- Class-specific filtering (track only selected object types)
- Upgrade to `yolov8m.pt` if GPU acceleration becomes available
- Add DeepSORT as an alternate tracker for appearance-based re-identification
