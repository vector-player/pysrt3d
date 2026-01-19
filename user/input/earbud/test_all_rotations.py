#!/usr/bin/env python3
"""
Test all possible rotation interpretations
"""

import numpy as np
from pathlib import Path
from scipy.spatial.transform import Rotation as R

# Original angles
angle_y = 100.0
angle_x = -66.0

print("Testing different rotation interpretations:")
print("="*60)

base_dir = Path(__file__).resolve().parent
pose_path = base_dir / 'pose.txt'
translation = np.array([0.0, 0.0, 1.383606])

# Test different combinations
test_cases = [
    ("Original: Y=100°, X=-66° (intrinsic YX)", 'yx', [angle_y, angle_x]),
    ("Negated Y: Y=-100°, X=-66°", 'yx', [-angle_y, angle_x]),
    ("Negated X: Y=100°, X=66°", 'yx', [angle_y, -angle_x]),
    ("Both negated: Y=-100°, X=66°", 'yx', [-angle_y, -angle_x]),
    ("XY order: X=-66°, Y=100°", 'xy', [angle_x, angle_y]),
    ("ZYX order (yaw-pitch-roll)", 'zyx', [0, angle_x, angle_y]),  # Assuming Z=0
]

for i, (name, order, angles) in enumerate(test_cases, 1):
    try:
        r = R.from_euler(order, angles, degrees=True)
        R_mat = r.as_matrix()
        
        pose = np.eye(4, dtype=np.float32)
        pose[:3, :3] = R_mat
        pose[:3, 3] = translation
        
        # Save this version
        test_file = base_dir / f'pose_test_{i}.txt'
        np.savetxt(test_file, pose, fmt='%.6f')
        
        print(f"\n{i}. {name}")
        print(f"   Rotation matrix:")
        print(f"   {R_mat}")
        print(f"   Saved to: {test_file.name}")
        
    except Exception as e:
        print(f"\n{i}. {name} - ERROR: {e}")

print("\n" + "="*60)
print("You can test each pose by copying it to pose.txt:")
print("  Copy-Item pose_test_1.txt pose.txt -Force")
print("  Then run: python run.py --input_dir user\\input\\earbud ...")
