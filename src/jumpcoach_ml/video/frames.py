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


    # 3. Pass the input video file path to the frame extraction module.
    #    The module should:
    #  ✅    - open the video
    #  ✅   - sample frames at a fixed FPS
    #  ✅    - optionally resize frames
    #  ✅  - attach timestamps/frame indices
    #
    #    Output: ordered list of video frames.
"""
import cv2, time, os

def get_frames(video_path):
  #resize and fix fps
  #video_path = "testVideos\IMG_1350.mov"
  os.system("ffmpeg -i "+video_path+" -r 30 -vf scale=640:-2 output_30fps.mp4 -loglevel quiet -y")
  video_path = "output_30fps.mp4"

  # max allow 10 min videos
  MAX_FRAMES = 1800

  cap = cv2.VideoCapture(video_path)
  frame_dict = {}

  #read video and attach timestamps
  while cap.isOpened():
      time_stamp = time.time()

      success, frame = cap.read()
      if not success:
          break
    
      frame_dict[time_stamp] = frame.copy()

      if len(frame_dict) >= MAX_FRAMES:
          #video too long
          #do something here
          break
  cap.release()

  #sorting dict
  sorted_keys = sorted(frame_dict.keys())
  
  return frame_dict



