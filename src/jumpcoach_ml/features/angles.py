"""
USER STORY / TASK MAPPING (User Story 1):
- Define exactly which jump-shot attributes will be extracted from the video and stored in the JSON object (feature definitions live here)
- Derive and standardize baseline shooting form features

OVERVIEW:
This module derives biomechanical shooting-form features from pose landmark data, focusing
on joint angles and related geometric attributes relevant to free-throw mechanics.

SCOPE:
This module defines the specific shooting-form attributes extracted from pose data and
converts raw landmark coordinates into structured, per-frame feature values that form
the basis of the baseline shooting form model.

LIBRARIES USED:
- numpy: used to perform vector mathematics required for joint angle computation and to
  assemble feature values into numerical representations suitable for analysis.
"""
