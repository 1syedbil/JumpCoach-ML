"""
OVERVIEW:
This file serves as the command-line entry point for User Story 1
. It is responsible 
for invoking the baseline creation method defined in baseline.py, which connects and
coordinates all underlying modules involved in building the baseline shooting form model.

SCOPE:
This file contains no machine learning or computer vision logic; it exists
 only to run the baseline pipeline and handle basic input/output concerns.
Outputs the baseline model artifact.
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent directory to path so Python can find src module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.jumpcoach_ml.pipeline.baseline import build_baseline


def main():
    # Parse command-line arguments with 2 required parameters:
    # 1. video_path: path to the input video file
    # 2. output: path to the output JSON file (optional, default: baseline_model.json)
    
    parser = argparse.ArgumentParser(description="Build a baseline shooting form model from a video")
    parser.add_argument("video_path", help="Path to the video file")
    parser.add_argument("--output", default="baseline_model.json", help="Output JSON file path")
    
    args = parser.parse_args()
    
    # Check if the video file exists
    video_file = Path(args.video_path)
    if not video_file.exists():
        print(f"Error: Video file not found: {args.video_path}")
        return
    
    print(f"Processing video: {args.video_path}")
    
    # Create default configuration { you can expand / customize this as needed }
    config = {
        "fps": 30,
        "resize": True,
        "confidence_threshold": 0.5
    }
    
    # Runing the baseline pipeline here with try-catch 
    try:
        baseline_model = build_baseline(str(video_file), config)
        
        # Save the result to a JSON file
        output_file = Path(args.output)
        with open(output_file, "w") as f:
            json.dump(baseline_model, f, indent=2)
        
        print(f"Success, Baseline model saved to: {args.output}")
        
    except Exception as e:
        print(f"Error processing video: {e}")


if __name__ == "__main__":
    # 9. Invoke the main entry point when the script is run from the command line.
    main()