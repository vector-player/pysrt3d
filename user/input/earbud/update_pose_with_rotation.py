#!/usr/bin/env python3
"""
Update pose.txt with rotation around Y-axis (100°) and X-axis (-66°)
"""

import numpy as np
from pathlib import Path

# Euler angles (in degrees)
angle_y = 100.0  # Y-axis rotation
angle_x = -66.0  # X-axis rotation

# Convert to radians
angle_y_rad = np.deg2rad(angle_y)
angle_x_rad = np.deg2rad(angle_x)

# Create rotation matrices
# Rotation around Y-axis
Ry = np.array([
    [np.cos(angle_y_rad),  0, np.sin(angle_y_rad)],
    [0,                     1, 0],
    [-np.sin(angle_y_rad), 0, np.cos(angle_y_rad)]
])

# Rotation around X-axis
Rx = np.array([
    [1, 0,                      0],
    [0, np.cos(angle_x_rad), -np.sin(angle_x_rad)],
    [0, np.sin(angle_x_rad),  np.cos(angle_x_rad)]
])

# Combined rotation: First rotate around Y, then around X
# R = Rx * Ry (apply Ry first, then Rx)
R = Rx @ Ry

print("Rotation matrix (3x3):")
print(R)
print()

# Load current pose
pose_path = Path(__file__).resolve().parent / 'pose.txt'
pose = np.loadtxt(pose_path, dtype=np.float32)

print("Original pose:")
print(pose)
print()

# Update rotation part of pose matrix (keep translation)
pose_updated = pose.copy()
pose_updated[:3, :3] = R

print("Updated pose with rotation:")
print(pose_updated)
print()

# Save updated pose
np.savetxt(pose_path, pose_updated, fmt='%.6f')
print(f"[OK] Updated pose saved to: {pose_path}")

# Verify by reading back
pose_verify = np.loadtxt(pose_path, dtype=np.float32)
print("\nVerification (reading back):")
print(pose_verify)
