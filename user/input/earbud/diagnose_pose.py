#!/usr/bin/env python3
"""
Diagnostic script to check if the model is visible at the given pose
"""

import sys
from pathlib import Path
import numpy as np
import cv2

# Add build directory to path
import sysconfig
python_version = f"{sys.version_info.major}{sys.version_info.minor}"
base_dir = Path(__file__).resolve().parent.parent.parent
_build_dir = base_dir / "build" / f"lib.win-amd64-cpython-{python_version}" / "Release"
if _build_dir.exists() and str(_build_dir) not in sys.path:
    sys.path.insert(0, str(_build_dir))

try:
    import pysrt3d
except ImportError:
    print("Error: pysrt3d not found")
    sys.exit(1)

# Load data
DATA_DIR = Path(__file__).resolve().parent
pose = np.loadtxt(DATA_DIR / 'pose.txt', dtype=np.float32)
K = np.loadtxt(DATA_DIR / 'K.txt', dtype=np.float32)

# Load first image
first_image_path = DATA_DIR / 'images' / 'earbuds_003_00110.png'
if not first_image_path.exists():
    print(f"Error: First image not found: {first_image_path}")
    sys.exit(1)

image = cv2.imread(str(first_image_path))
h, w = image.shape[:2]
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

print("="*60)
print("POSE DIAGNOSTICS")
print("="*60)
print(f"\nPose matrix:")
print(pose)
print(f"\nCamera intrinsics K:")
print(K)
print(f"\nImage size: {w} x {h}")

# Initialize model and tracker
print("\nInitializing model and tracker...")
model = pysrt3d.Model(
    name="earbud_left",
    model_path=str(DATA_DIR / 'earbud_left.obj'),
    meta_path=str(DATA_DIR / 'earbud_left.obj.meta'),
    unit_in_meter=0.001,
    threshold_init=0.0,
    threshold_track=0.0,
    kl_threshold=1.0
)

tracker = pysrt3d.Tracker(
    imwidth=w,
    imheight=h,
    K=K
)

tracker.add_model(model)
tracker.setup()

# Set pose
print("Setting initial pose...")
model.reset_pose(pose)

# Try to render
print("\nAttempting to render model at this pose...")
renderer = pysrt3d.Renderer(tracker)

# Update camera with first image
try:
    tracker.update(image=image_rgb)
    print("[OK] Tracker update succeeded")
except Exception as e:
    print(f"[ERROR] Tracker update failed: {e}")
    print("\nThis is the error we're trying to diagnose.")
    print("The histogram initialization is failing because:")
    print("  - The model edges are not visible at this pose")
    print("  - Or the correspondence lines don't intersect the image")
    print("  - Or the model orientation is incorrect")
    sys.exit(1)

# Try to render
rendered = renderer.render()
if rendered is not None:
    print("[OK] Render succeeded")
    print(f"Rendered image shape: {rendered.shape}")
    
    # Save rendered image
    output_path = DATA_DIR / 'model_render_at_pose.png'
    if len(rendered.shape) == 3:
        cv2.imwrite(str(output_path), cv2.cvtColor(rendered, cv2.COLOR_RGB2BGR))
    else:
        cv2.imwrite(str(output_path), rendered)
    print(f"[OK] Rendered image saved to: {output_path}")
else:
    print("[WARNING] Render returned None")

print("\n" + "="*60)
