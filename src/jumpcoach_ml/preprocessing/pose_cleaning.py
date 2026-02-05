"""
USER STORY / TASK MAPPING (User Story 1):
- Normalize and stabilize pose data for baseline modeling

OVERVIEW:
This module is responsible for normalizing and stabilizing pose landmark data extracted
from video frames in order to reduce noise and remove irrelevant variation prior to
feature extraction.

SCOPE:
This module operates on sequences of pose landmarks to apply transformations such as
coordinate normalization, scale normalization, and temporal smoothing, producing a
cleaned and consistent pose representation suitable for downstream biomechanical
feature computation.

LIBRARIES USED:
- numpy: used to perform geometric transformations, scaling, and basic smoothing
  operations on pose landmark data.
- scipy (optional): used for more robust signal smoothing, interpolation, and temporal
  resampling of pose sequences when higher-quality stabilization is required.
"""