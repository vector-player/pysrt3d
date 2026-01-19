#!/usr/bin/env python3
"""
Simple tracking script for earbud_left.obj
Based on example/demo.py
"""

import sys
from pathlib import Path
import numpy as np
import cv2

# Add build directory to path for pysrt3d import (for development mode)
# Try common build directory patterns
import sysconfig
python_version = f"{sys.version_info.major}{sys.version_info.minor}"
base_dir = Path(__file__).resolve().parent.parent.parent

# Try Windows pattern first (most common for this project)
_build_dir = base_dir / "build" / f"lib.win-amd64-cpython-{python_version}" / "Release"
if not _build_dir.exists():
    # Try generic pattern
    platform_tag = sysconfig.get_platform().replace("-", "_")
    _build_dir = base_dir / "build" / f"lib.{platform_tag}-cpython-{python_version}" / "Release"

if _build_dir.exists() and str(_build_dir) not in sys.path:
    sys.path.insert(0, str(_build_dir))

# Also try importing from installed package
try:
    import pysrt3d
    # Verify Model is available
    if not hasattr(pysrt3d, 'Model'):
        raise AttributeError("pysrt3d.Model not found")
except (ImportError, AttributeError) as e:
    print(f"Error: pysrt3d module not found or incomplete: {e}")
    print(f"Build directory: {_build_dir}")
    print(f"Build dir exists: {_build_dir.exists()}")
    if _build_dir.exists():
        print(f"Files in build dir: {list(_build_dir.glob('*.pyd'))}")
    sys.exit(1)

# Setup paths
DATA_DIR = Path(__file__).resolve().parent
images_dir = DATA_DIR / 'images'
images = sorted(list(images_dir.glob('*.png')))
print(f"Found {len(images)} images")

# Get image dimensions
h, w = cv2.imread(str(images[0])).shape[:2]
print(f"Image size: {w}x{h}")

# Load camera intrinsics and initial pose
K = np.loadtxt(DATA_DIR / 'K.txt', dtype=np.float32)
init_pose = np.loadtxt(DATA_DIR / 'pose.txt', dtype=np.float32)

print(f"\nCamera intrinsics K:\n{K}")
print(f"\nInitial pose:\n{init_pose}")

# Init model
model = pysrt3d.Model(
    name="earbud_left",
    model_path=str(DATA_DIR / 'earbud_left.obj'),
    meta_path=str(DATA_DIR / 'earbud_left.obj.meta'),
    unit_in_meter=0.001,    # model in mm
    threshold_init=0.0,     # no limit while initialization
    threshold_track=0.0,    # no limit while tracking
    kl_threshold=1.0
)

# Init tracker
tracker = pysrt3d.Tracker(
    imwidth=w,
    imheight=h,
    K=K
)

# Add model to tracker
tracker.add_model(model)
tracker.setup()

# Make renderer
renderer = pysrt3d.Renderer(tracker)

# Set initial pose
print("\nSetting initial pose...")
model.reset_pose(init_pose)

# Store poses for all frames
poses_output = []

print(f"\nProcessing {len(images)} frames...")
for idx, image_path in enumerate(images):
    # Read image
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Warning: Could not read {image_path}, skipping...")
        continue
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    try:
        # Tracking iteration
        tracker.update(image=image_rgb)
        
        # Get tracking info
        pose_uv = model.pose_uv
        conf = model.conf
        pose_6dof = model.pose
        pose_gl = model.pose_gl
        valid_line_prop = model.valid_line_prop
        
        # Store pose for this frame
        poses_output.append({
            'frame': idx,
            'pose': pose_6dof.copy(),
            'pose_gl': pose_gl.copy(),
            'confidence': conf,
            'pose_uv': pose_uv.copy(),
            'valid_line_prop': valid_line_prop
        })
        
        # Print progress
        if (idx + 1) % 10 == 0 or idx == 0:
            print(f"  Frame {idx:04d}/{len(images)-1:04d}: confidence={conf:.4f}, "
                  f"pose_uv=({pose_uv[0]:.1f}, {pose_uv[1]:.1f}), "
                  f"valid_lines={valid_line_prop:.2f}")
    
    except Exception as e:
        print(f"Error processing frame {idx}: {e}")
        import traceback
        traceback.print_exc()
        break

# Save results
print(f"\nSaving results...")

# Save poses in text format
poses_txt = DATA_DIR / 'poses_output.txt'
with open(poses_txt, 'w') as f:
    for item in poses_output:
        f.write(f"# Frame {item['frame']:04d}: confidence={item['confidence']:.6f}, "
                f"pose_uv=({item['pose_uv'][0]:.2f}, {item['pose_uv'][1]:.2f}), "
                f"valid_lines={item['valid_line_prop']:.4f}\n")
        np.savetxt(f, item['pose'], fmt='%.8f')
        f.write('\n')

# Save poses as numpy array [N, 4, 4]
poses_array = np.array([item['pose'] for item in poses_output])
poses_npy = DATA_DIR / 'poses_output.npy'
np.save(poses_npy, poses_array)

# Save OpenGL poses [N, 4, 4]
poses_gl_array = np.array([item['pose_gl'] for item in poses_output])
poses_gl_npy = DATA_DIR / 'poses_gl_output.npy'
np.save(poses_gl_npy, poses_gl_array)

# Save metadata
metadata = {
    'confidences': [item['confidence'] for item in poses_output],
    'pose_uv': np.array([item['pose_uv'] for item in poses_output]),
    'valid_line_prop': [item['valid_line_prop'] for item in poses_output]
}
metadata_npy = DATA_DIR / 'poses_metadata.npy'
np.save(metadata_npy, metadata)

print(f"\n✓ Results saved:")
print(f"  - Poses (text): {poses_txt}")
print(f"  - Poses (numpy): {poses_npy} (shape: {poses_array.shape})")
print(f"  - Poses GL (numpy): {poses_gl_npy} (shape: {poses_gl_array.shape})")
print(f"  - Metadata: {metadata_npy}")
print(f"\nProcessed {len(poses_output)} frames successfully!")
