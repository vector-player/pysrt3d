#!/usr/bin/env python3
"""
Update pose.txt with distance of 5cm (0.05 meters)
"""

import numpy as np
from pathlib import Path

# Load current pose
pose_path = Path(__file__).resolve().parent / 'pose.txt'
pose = np.loadtxt(pose_path, dtype=np.float32)

print("Current pose:")
print(pose)
print()

# Update Z translation to 5cm (0.05 meters)
pose_updated = pose.copy()
pose_updated[2, 3] = 0.05  # 5cm = 0.05 meters

print("Updated pose with Z = 0.05m (5cm):")
print(pose_updated)
print()

# Save
np.savetxt(pose_path, pose_updated, fmt='%.6f')
print(f"[OK] Updated pose saved to: {pose_path}")

# Calculate projection
K = np.loadtxt(Path(__file__).resolve().parent / 'K.txt', dtype=np.float32)
fx, fy = K[0, 0], K[1, 1]
cx, cy = K[0, 2], K[1, 2]

tx, ty, tz = pose_updated[0, 3], pose_updated[1, 3], pose_updated[2, 3]
u = (fx * tx / tz) + cx
v = (fy * ty / tz) + cy

print(f"\nProjected position in image: ({u:.1f}, {v:.1f})")
print(f"Distance: {tz*100:.1f} cm")
