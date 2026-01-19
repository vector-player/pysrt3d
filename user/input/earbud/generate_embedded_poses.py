#!/usr/bin/env python3
"""
Generate embedded pose data for Blender script
"""

import numpy as np
from pathlib import Path

# Load poses
script_dir = Path(__file__).parent
poses_file = script_dir / "poses.npy"
poses = np.load(str(poses_file))

print(f"Loaded {len(poses)} poses")
print("Generating embedded data...")

# Convert to list format
poses_list = poses.tolist()

# Generate Python code for embedded data
output_lines = []
output_lines.append("# Embedded pose data - 310 frames")
output_lines.append("EMBEDDED_POSES = [")

for i, pose in enumerate(poses_list):
    output_lines.append(f"    # Frame {i}")
    output_lines.append("    [")
    for row in pose:
        row_str = "[" + ", ".join(f"{val:.6f}" for val in row) + "]"
        output_lines.append(f"        {row_str},")
    output_lines.append("    ],")

output_lines.append("]")

# Write to file
output_file = script_dir / "embedded_poses_data.py"
with open(output_file, 'w') as f:
    f.write("\n".join(output_lines))

print(f"[OK] Generated embedded pose data: {output_file}")
print(f"     Size: {len(poses)} frames")
