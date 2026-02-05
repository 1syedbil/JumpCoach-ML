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
