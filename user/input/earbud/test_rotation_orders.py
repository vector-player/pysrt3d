#!/usr/bin/env python3
"""
Test different rotation orders for the pose
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
Ry = np.array([
    [np.cos(angle_y_rad),  0, np.sin(angle_y_rad)],
    [0,                     1, 0],
    [-np.sin(angle_y_rad), 0, np.cos(angle_y_rad)]
])

Rx = np.array([
    [1, 0,                      0],
    [0, np.cos(angle_x_rad), -np.sin(angle_x_rad)],
    [0, np.sin(angle_x_rad),  np.cos(angle_x_rad)]
])

print("Testing different rotation orders:")
print("="*60)

# Order 1: Rx * Ry (rotate Y first, then X)
R1 = Rx @ Ry
print("\nOrder 1: Rx * Ry (rotate around Y first, then X)")
print(R1)

# Order 2: Ry * Rx (rotate X first, then Y)
R2 = Ry @ Rx
print("\nOrder 2: Ry * Rx (rotate around X first, then Y)")
print(R2)

# Order 3: Using scipy rotation (intrinsic rotations)
try:
    from scipy.spatial.transform import Rotation as R
    # Intrinsic rotations: rotate around Y, then around X (in body frame)
    r_intrinsic = R.from_euler('yx', [angle_y, angle_x], degrees=True)
    R3 = r_intrinsic.as_matrix()
    print("\nOrder 3: Intrinsic rotations (Y then X in body frame)")
    print(R3)
except ImportError:
    print("\nOrder 3: scipy not available, skipping")

# Load current pose
pose_path = Path(__file__).resolve().parent / 'pose.txt'
pose_original = np.loadtxt(pose_path, dtype=np.float32)
translation = pose_original[:3, 3]

print("\n" + "="*60)
print("Current translation:", translation)
print("\nTrying Order 2 (Ry * Rx)...")

# Try Order 2
pose_test = np.eye(4, dtype=np.float32)
pose_test[:3, :3] = R2
pose_test[:3, 3] = translation

# Save for testing
np.savetxt(pose_path, pose_test, fmt='%.6f')
print(f"[OK] Updated pose with Order 2 saved to: {pose_path}")
print("\nPose matrix:")
print(pose_test)
