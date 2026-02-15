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
import json
import numpy as np

def process_data(baseline_json):
  """
  calculate the angles_deg section in baseline.json
  
  :param json: the json that has landmarks
  """
  stages = ['set_point', 'release_point', 'follow_through']
  
  joint_map = {
    'left_knee_flexion':  ('left_hip', 'left_knee', 'left_ankle'),
    'right_knee_flexion': ('right_hip', 'right_knee', 'right_ankle'),

    'left_elbow_flexion': ('left_shoulder', 'left_elbow', 'left_wrist'),
    'right_elbow_flexion':('right_shoulder', 'right_elbow', 'right_wrist'),
  }
  
  foot_map = {
    'left_foot_orientation':  ('left_knee', 'left_ankle', 'left_foot_index'),
    'right_foot_orientation': ('right_knee', 'right_ankle', 'right_foot_index')
  }
  
  data = baseline_json.get('baseline',{}).get('keyframes',{})
  for stage in stages:
    frame_data = data[stage]
    landmarks = frame_data.get('landmarks',{})
    
    # body's angle
    for angle_name, (key_a,key_b,key_c) in joint_map.items():
      landmark_a = landmarks.get(key_a)
      landmark_b = landmarks.get(key_b)
      landmark_c = landmarks.get(key_c)
      
      angle = calculate_angle(landmark_a,landmark_b,landmark_c)
      frame_data['angles_deg'][angle_name] = angle
      
    # foot's angle
    for foot_name, (key_a,key_b,key_c) in foot_map.items():
      knee = landmarks.get(key_a)
      ankle = landmarks.get(key_b)
      foot_index = landmarks.get(key_c)
      
      is_left_foot = True
      if "left" not in foot_name:
        is_left_foot = False
        
      angle = calculate_foot(knee,ankle,foot_index,is_left_foot)
      frame_data['angles_deg'][foot_name] = angle
      
  return baseline_json



def calculate_angle(landmark_a,landmark_b,landmark_c):
  """
  calculate the angle of joints
  
  """
  # valid landmarks
  if not all([landmark_a,landmark_b,landmark_c]):
    return None
  
  try:
    a = np.array([landmark_a['x'], landmark_a['y'], landmark_a['z']],dtype=float)
    b = np.array([landmark_b['x'], landmark_b['y'], landmark_b['z']],dtype=float)
    c = np.array([landmark_c['x'], landmark_c['y'], landmark_c['z']],dtype=float)
  except(TypeError, ValueError):
    return None
  
  # vector
  vec_ab = a-b
  vec_bc = c-b
  
  # norm of vectors
  norm_ab = np.linalg.norm(vec_ab)
  norm_bc = np.linalg.norm(vec_bc)
  
  # dot product
  cos_angle = np.dot(vec_ab, vec_bc) / (norm_ab * norm_bc)
  cos_angle = np.clip(cos_angle, -1.0, 1.0)
  
  angle = np.degrees(np.arccos(cos_angle))
  return float(np.round(angle, 2))


def calculate_foot(knee, ankle, foot_index, is_left_foot):
  """
  calculate the foot orientation
  With the knee at 0 degrees, the direction of the toes relative to the knee is left or right.
  +: toes pointing outward
  -: toes pointing inward

  :param knee: landmark of knee
  :param ankle: landmark of ankle
  :param foot_index: landmark of foot_index
  :param is_left_foot: which foot
  """
  # valid landmarks
  if not all([knee,ankle,foot_index]):
    return None
  
  try:
    a = np.array([knee['x'], knee['z']],dtype=float)
    b = np.array([ankle['x'], ankle['z']],dtype=float)
    c = np.array([foot_index['x'], foot_index['z']],dtype=float)
  except(TypeError, ValueError):
    return None
  
  # vector
  vec_ab = b-a
  vec_bc = c-b
  
  # cross_product & dot_product
  cross_product = np.cross(vec_ab, vec_bc)
  dot_product   = np.dot(vec_ab, vec_bc)
  
  angle_rad = np.arctan2(cross_product, dot_product)
  angle_deg = np.degrees(angle_rad)
  
  if not is_left_foot:
        angle_deg = -angle_deg
        
  return float(np.round(angle_deg, 2))


# for testing⬇️
if __name__ == "__main__":
  test_data = {
      "baseline": {
        "keyframes": {
          "set_point": {
            "landmarks": {
              "left_hip":    {"x": 0.0, "y": 0.0, "z": 0.0},
              "left_knee":   {"x": 0.0, "y": 1.0, "z": 0.0},
              "left_ankle":  {"x": 1.0, "y": 1.0, "z": 0.0},
              "left_foot_index":{"x": -0.5, "y": 0, "z": 2},
              
              "right_hip":    {"x": 0.0, "y": 0.0, "z": 0.0},
              "right_knee":   {"x": 0.0, "y": 1.0, "z": 0.0},
              "right_ankle":  {"x": 1.0, "y": 1.0, "z": 0.0},
              "right_foot_index":{"x": 1.5, "y": 0, "z": 2},

              "left_shoulder": {"x": 0.0, "y": 0.0, "z": 0.0},
              "left_elbow":    {"x": 1.0, "y": 0.0, "z": 0.0},
              "left_wrist":    {"x": 2.0, "y": 0.0, "z": 0.0},
              
              "right_shoulder": {"x": 0.0, "y": 0.0, "z": 0.0},
              "right_elbow":    {"x": 1.0, "y": 0.0, "z": 0.0},
              "right_wrist":    {"x": 2.0, "y": 0.0, "z": 0.0}
            },
            "angles_deg": {
            "left_knee_flexion": 0,
            "right_knee_flexion": 0,

            "left_elbow_flexion": 0,
            "right_elbow_flexion": 0,

            "left_foot_orientation": 0,
            "right_foot_orientation": 0
        }
          }
        }
      }
    }
  process_data(test_data)
  a = input()