#!/usr/bin/env python3
"""
Visual confirmation script for poses.npy
Follows the pattern from example/demo.py
Loads poses from poses.npy and renders them over images for visual confirmation
"""

import sys
from pathlib import Path
import numpy as np
import cv2

# Add build directory to path for pysrt3d import
# Try common build directory patterns
import sysconfig
python_version = f"{sys.version_info.major}{sys.version_info.minor}"
base_dir = Path(__file__).resolve().parent.parent.parent.parent

# Try Windows pattern first (most common for this project)
_build_dir = base_dir / "build" / f"lib.win-amd64-cpython-{python_version}" / "Release"
if not _build_dir.exists():
    # Try generic pattern
    platform_tag = sysconfig.get_platform().replace("-", "_")
    _build_dir = base_dir / "build" / f"lib.{platform_tag}-cpython-{python_version}" / "Release"
# Fallback to Python 3.11 if current version not found
if not _build_dir.exists():
    _build_dir = base_dir / "build" / "lib.win-amd64-cpython-311" / "Release"

if _build_dir.exists():
    build_path = str(_build_dir)
    if build_path not in sys.path:
        sys.path.insert(0, build_path)
try:
    import pysrt3d
except ImportError as e:
    print(f"Error: pysrt3d module not found: {e}")
    print(f"Build directory: {_build_dir}")
    print(f"sys.path: {sys.path[:3]}")
    sys.exit(1)

# Setup paths
DATA_DIR = Path(__file__).resolve().parent
images_dir = DATA_DIR / 'images'
poses_file = DATA_DIR / 'poses.npy'
metadata_file = DATA_DIR / 'metadata.npy'

# Load poses
print(f"Loading poses from: {poses_file}")
poses = np.load(poses_file)
print(f"Loaded poses shape: {poses.shape}")
print(f"Number of frames: {len(poses)}")

# Load metadata if available
metadata = None
if metadata_file.exists():
    print(f"Loading metadata from: {metadata_file}")
    metadata = np.load(metadata_file, allow_pickle=True).item()
    print(f"Metadata keys: {metadata.keys() if isinstance(metadata, dict) else 'N/A'}")

# Get images
images = sorted(list(images_dir.glob('*.png')))
print(f"Found {len(images)} images")

if len(images) == 0:
    print(f"Error: No images found in {images_dir}")
    sys.exit(1)

# Get image dimensions
h, w = cv2.imread(str(images[0])).shape[:2]
print(f"Image size: {w}x{h}")

# Load camera intrinsics
K = np.loadtxt(DATA_DIR / 'K.txt', dtype=np.float32)
print(f"\nCamera intrinsics K:\n{K}")

# Check if we have enough poses for the images
num_frames = min(len(poses), len(images))
print(f"\nProcessing {num_frames} frames...")

# Init model
model_name = "earbud_left"
model_path = DATA_DIR / 'earbud_left.obj'
meta_path = DATA_DIR / f'{model_name}.obj.meta'

if not meta_path.exists():
    meta_path = DATA_DIR / f'{model_name}.meta'
    if not meta_path.exists():
        meta_path = None

print(f"\nInitializing model:")
print(f"  Model: {model_path}")
print(f"  Meta: {meta_path if meta_path and meta_path.exists() else 'None'}")

model = pysrt3d.Model(
    name=model_name,
    model_path=str(model_path),
    meta_path=str(meta_path) if meta_path and meta_path.exists() else "",
    unit_in_meter=0.001,    # model in mm
    threshold_init=0.0,
    threshold_track=0.0,
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

# Create output directory for visualizations
output_dir = DATA_DIR / 'visualizations_poses'
output_dir.mkdir(exist_ok=True)
print(f"\nSaving visualizations to: {output_dir}")

# Process each frame
print(f"\nRendering poses over images...")
for idx in range(num_frames):
    # Load image
    image_path = images[idx]
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Warning: Could not read {image_path}, skipping...")
        continue
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Set pose from poses.npy BEFORE updating tracker
    # This ensures the model is at the correct pose for rendering
    pose = poses[idx]
    model.reset_pose(pose)
    
    # Update tracker with image (needed for renderer to work properly)
    # This pushes the image to the camera queue and does tracking
    # Note: We call this to ensure the camera has the image, but we've already
    # set the pose from poses.npy, so the tracking won't change it significantly
    tracker.update(image=image_rgb)
    
    # Re-set the pose after tracking to ensure we're visualizing the exact pose from poses.npy
    # (tracking might have slightly adjusted it)
    model.reset_pose(pose)
    
    # Push the image again for the renderer (tracker.update() consumed it from the queue)
    # The renderer needs the image to be available when it calls UpdateImage()
    # Note: This will do tracking again, but we'll reset the pose after
    tracker.update(image=image_rgb)
    
    # Re-set the pose again after the second tracking update
    model.reset_pose(pose)
    
    # Render the model at this pose
    # Note: renderer.render() already returns the model overlaid on the camera image
    # (it blends the camera image with the rendered model automatically)
    # renderer.render() calls camera_ptr_->UpdateImage() which will use the image
    # that was pushed above
    rendered_image = renderer.render()
    
    if rendered_image is None:
        print(f"Warning: renderer.render() returned None for frame {idx}, skipping...")
        continue
    
    # Convert rendered image to BGR for OpenCV
    # The rendered_image already contains the overlay, so we can use it directly
    composite = cv2.cvtColor(rendered_image, cv2.COLOR_RGB2BGR)
    
    # Get pose info for display
    pose_uv = model.pose_uv
    conf = model.conf
    
    # Get metadata if available
    if metadata and isinstance(metadata, dict):
        if 'pose_uv' in metadata and idx < len(metadata['pose_uv']):
            meta_pose_uv = metadata['pose_uv'][idx]
        else:
            meta_pose_uv = None
        if 'confidences' in metadata and idx < len(metadata['confidences']):
            meta_conf = metadata['confidences'][idx]
        else:
            meta_conf = None
    else:
        meta_pose_uv = None
        meta_conf = None
    
    # Overlay text information
    info_lines = [
        f"Frame {idx:04d}/{num_frames-1:04d}",
        f"Pose UV: ({pose_uv[0]:.1f}, {pose_uv[1]:.1f})",
        f"Confidence: {conf:.4f}" if conf > 0 else "Confidence: N/A"
    ]
    
    if meta_conf is not None:
        info_lines.append(f"Meta Conf: {meta_conf:.4f}")
    
    # Draw text with background for readability on composite image
    y_offset = 30
    for i, text in enumerate(info_lines):
        # Draw background rectangle
        (text_width, text_height), baseline = cv2.getTextSize(
            text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2
        )
        cv2.rectangle(composite, 
                     (10, y_offset + i*25 - text_height - 5),
                     (10 + text_width + 10, y_offset + i*25 + 5),
                     (0, 0, 0), -1)
        # Draw text
        cv2.putText(composite, text, (15, y_offset + i*25),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    # Draw pose_uv point
    if pose_uv[0] > 0 and pose_uv[1] > 0:
        uv_point = (int(pose_uv[0]), int(pose_uv[1]))
        cv2.circle(composite, uv_point, 5, (0, 255, 0), -1)
        cv2.circle(composite, uv_point, 8, (0, 255, 0), 2)
    
    # Save visualization
    output_path = output_dir / f'frame_{idx:04d}.png'
    cv2.imwrite(str(output_path), composite)
    
    # Print progress
    if (idx + 1) % 50 == 0 or idx == 0 or idx == num_frames - 1:
        conf_str = f"{conf:.4f}" if conf > 0 else "N/A"
        print(f"  Frame {idx:04d}/{num_frames-1:04d}: pose_uv=({pose_uv[0]:.1f}, {pose_uv[1]:.1f}), "
              f"conf={conf_str}")
    
    # Optionally display frames (set SHOW_FRAMES to True to enable)
    SHOW_FRAMES = False  # Set to True to display frames interactively
    if SHOW_FRAMES and idx < 5:
        cv2.imshow('Pose Visualization', composite)
        print(f"  Press any key to continue (frame {idx})...")
        cv2.waitKey(0)

cv2.destroyAllWindows()

print(f"\n[OK] Visualization complete!")
print(f"  - Processed {num_frames} frames")
print(f"  - Saved visualizations to: {output_dir}")
print(f"  - Sample frames: frame_0000.png, frame_0001.png, ...")
