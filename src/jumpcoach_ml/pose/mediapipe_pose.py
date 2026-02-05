"""
USER STORY / TASK MAPPING (User Story 1):
- Extract and validate pose landmarks from the prepared video frames

OVERVIEW:
This module performs pose inference on prepared video frames by extracting body landmark
coordinates and confidence values for each frame.

SCOPE:
This module serves as the interface between raw image frames and structured pose data,
converting frames into pose landmark representations that can be used for downstream
feature extraction and analysis.

LIBRARIES USED:
- mediapipe: provides the pre-trained pose estimation model used to detect and track
  human body landmarks in each frame.
- numpy: used to store pose landmark coordinates and confidence values in a consistent
  numerical format for further processing.
"""
