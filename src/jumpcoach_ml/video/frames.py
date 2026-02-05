"""
USER STORY / TASK MAPPING (User Story 1):
- Prepare the uploaded optimal free throw shooting form video for pose inference

OVERVIEW:
This module is responsible for preparing an uploaded optimal free-throw video for pose
inference by extracting a consistent sequence of frames from the video.

SCOPE:
This module handles video decoding, frame sampling, and basic frame preprocessing before
the frames are passed to the pose inference stage of the baseline pipeline.

LIBRARIES USED:
- opencv-python (cv2): used to open video files, iterate through frames, and perform basic
  preprocessing such as resizing and frame sampling.
- numpy: used as the underlying data structure for image frames passed between pipeline stages.
"""
