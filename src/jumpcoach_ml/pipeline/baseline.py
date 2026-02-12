"""
USER STORY / TASK MAPPING (User Story 1):
- Assemble baseline model artifact and compute baseline quality score (quality scoring may be added later)

OVERVIEW:
This module defines the baseline creation pipeline for User Story 1. It coordinates
the processing stages that transform an uploaded optimal free-throw video into a
baseline shooting form model.

SCOPE:
This module serves as an orchestration layer that brings together the video frame
extraction logic (video/frames.py), pose inference logic (pose/mediapipe_pose.py),
and feature extraction logic (features/angles.py) into a single, ordered workflow. 
It assembles the final baseline model artifact and computes the baseline quality score
based on the extracted features. It does not implement the underlying machine learning 
or computer vision logic itself.
"""

# 1. Import standard utilities:
#    - typing helpers
#    - dataclasses (optional)
#    - path handling

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List
import time


def build_baseline(video_path, config):

    start_ts = time.time()
    video_file = Path(video_path)

    if not video_file.exists():
        raise FileNotFoundError(f"Video file not found: {video_file}")

    # Config values are currently not used by frames.py because it hardcodes
    # FPS/resize via ffmpeg internally. Keeping these reads is harmless for now. :contentReference[oaicite:3]{index=3}
    confidence_threshold = float(config.get("confidence_threshold", 0.5))

    # ------------------------------------------------------------------
    # Stage 1: Video → Frames (frames.py)
    # ------------------------------------------------------------------
    try:
        from jumpcoach_ml.video.frames import get_frames
    except Exception as e:
        raise ImportError(
            "Could not import get_frames from jumpcoach_ml.video.frames. "
            "Make sure frames.py defines get_frames(video_path)."
        ) from e

    frame_dict = get_frames(str(video_file), config)  # returns {timestamp: frame}

    # Convert dict -> ordered list of frame records
    
    # The frame_dict is sorted in get_frames()
    # ordered_timestamps = sorted(frame_dict.keys())
    frames: List[Dict[str, Any]] = [
        {
            "timestamp_ms": int(tms),
            "image_bgr": frame_dict[tms],
        }
        for tms in frame_dict
    ]

    # ------------------------------------------------------------------
    # Stage 2: Frames → Pose Landmarks (mediapipe_pose.py)
    # ------------------------------------------------------------------
    # infer_pose_sequence should iterate frames in order. We now provide that order.
    try:
        from jumpcoach_ml.pose.mediapipe_pose import infer_pose_sequence
    except Exception as e:
        raise ImportError(
            "Could not import infer_pose_sequence from jumpcoach_ml.pose.mediapipe_pose. "
            "Make sure mediapipe_pose.py defines infer_pose_sequence(frames, confidence_threshold)."
        ) from e

    pose_frames = infer_pose_sequence(
        frames=frames,
        confidence_threshold=confidence_threshold
    )

    # ------------------------------------------------------------------
    # Stage 3: Pose Normalization & Stabilization (pose_cleaning.py)
    # ------------------------------------------------------------------
    try:
        from jumpcoach_ml.preprocessing.pose_cleaning import clean_pose_sequence
    except Exception as e:
        raise ImportError(
            "Could not import clean_pose_sequence from jumpcoach_ml.preprocessing.pose_cleaning. "
            "Make sure pose_cleaning.py defines clean_pose_sequence(pose_frames)."
        ) from e

    cleaned_pose_frames = clean_pose_sequence(pose_frames=pose_frames)

    # ------------------------------------------------------------------
    # Stage 4: Feature Extraction (angles.py)
    # ------------------------------------------------------------------
    try:
        from jumpcoach_ml.features.angles import compute_angle_features
    except Exception as e:
        raise ImportError(
            "Could not import compute_angle_features from jumpcoach_ml.features.angles. "
            "Make sure angles.py defines compute_angle_features(pose_frames)."
        ) from e

    feature_series = compute_angle_features(pose_frames=cleaned_pose_frames)

    # ------------------------------------------------------------------
    # Stage 5: Baseline Model Assembly (still TBD)
    # ------------------------------------------------------------------
    artifact: Dict[str, Any] = {
        "metadata": {
            "pipeline_version": "v1",
            "video_filename": video_file.name,
            "created_unix_ts": int(time.time()),
            "runtime_sec": round(time.time() - start_ts, 4),
        },
        "baseline": {
            "status": "TBD",
            "notes": "Baseline model artifact schema not finalized yet.",
            "feature_series": None,
            "timestamps_sec": None,
        },
    }

    # JSON sanitization (inline)
    try:
        import numpy as np

        def sanitize(obj):
            if isinstance(obj, dict):
                return {str(k): sanitize(v) for k, v in obj.items()}
            if isinstance(obj, list):
                return [sanitize(v) for v in obj]
            if isinstance(obj, tuple):
                return [sanitize(v) for v in obj]
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            if isinstance(obj, (np.float32, np.float64)):
                return float(obj)
            if isinstance(obj, (np.int32, np.int64)):
                return int(obj)
            return obj

        artifact = sanitize(artifact)
    except ImportError:
        pass

    return artifact