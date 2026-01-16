#!/usr/bin/env python3
"""
Generic script for running pysrt3d object tracking.

This script processes a sequence of images and tracks 6DoF object poses,
saving all outputs including pose matrices, visualizations, and metadata.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, Tuple
import numpy as np
import cv2

# Add build directory to path for pysrt3d import (for development mode)
# Try common build directory patterns
import sysconfig
python_version = f"{sys.version_info.major}{sys.version_info.minor}"
base_dir = Path(__file__).resolve().parent

# Try Windows pattern first (most common for this project)
_build_dir = base_dir / "build" / f"lib.win-amd64-cpython-{python_version}" / "Release"
if not _build_dir.exists():
    # Try generic pattern
    platform_tag = sysconfig.get_platform().replace("-", "_")
    _build_dir = base_dir / "build" / f"lib.{platform_tag}-cpython-{python_version}" / "Release"

if _build_dir.exists() and str(_build_dir) not in sys.path:
    sys.path.insert(0, str(_build_dir))

try:
    import pysrt3d
except ImportError:
    print("Error: pysrt3d module not found. Please install the package first.")
    print("Run: pip install .")
    sys.exit(1)


def validate_inputs(input_dir: Path) -> Tuple[Path, Path, Path, Path, Path]:
    """Validate input directory structure and return paths to required files."""
    errors = []
    
    # Check required files
    model_path = input_dir / "model.obj"
    if not model_path.exists():
        # Try alternative names
        obj_files = list(input_dir.glob("*.obj"))
        if obj_files:
            model_path = obj_files[0]
        else:
            errors.append(f"Model file not found: {model_path}")
    
    meta_path = input_dir / f"{model_path.stem}.meta"
    if not meta_path.exists():
        # Try alternative names
        meta_files = list(input_dir.glob("*.meta"))
        if meta_files:
            meta_path = meta_files[0]
        else:
            # Meta file is optional, will be auto-generated
            meta_path = input_dir / f"{model_path.stem}.meta"
            print(f"Warning: Meta file not found, will use: {meta_path}")
    
    k_path = input_dir / "K.txt"
    if not k_path.exists():
        errors.append(f"Camera intrinsics file not found: {k_path}")
    
    pose_path = input_dir / "pose.txt"
    if not pose_path.exists():
        errors.append(f"Initial pose file not found: {pose_path}")
    
    images_dir = input_dir / "images"
    if not images_dir.exists():
        errors.append(f"Images directory not found: {images_dir}")
    else:
        images = sorted(list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg")))
        if not images:
            errors.append(f"No images found in: {images_dir}")
    
    if errors:
        print("Input validation errors:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    
    return model_path, meta_path, k_path, pose_path, images_dir


def load_camera_intrinsics(k_path: Path) -> np.ndarray:
    """Load camera intrinsic matrix from file."""
    try:
        K = np.loadtxt(k_path, dtype=np.float32)
        if K.shape != (3, 3):
            raise ValueError(f"Expected 3x3 matrix, got shape {K.shape}")
        return K
    except Exception as e:
        print(f"Error loading camera intrinsics from {k_path}: {e}")
        sys.exit(1)


def load_initial_pose(pose_path: Path) -> np.ndarray:
    """Load initial pose matrix from file."""
    try:
        pose = np.loadtxt(pose_path, dtype=np.float32)
        if pose.shape != (4, 4):
            raise ValueError(f"Expected 4x4 matrix, got shape {pose.shape}")
        return pose
    except Exception as e:
        print(f"Error loading initial pose from {pose_path}: {e}")
        sys.exit(1)


def get_image_size(images_dir: Path) -> Tuple[int, int]:
    """Get image dimensions from first image."""
    images = sorted(list(images_dir.glob("*.png")) + list(images_dir.glob("*.jpg")))
    if not images:
        raise ValueError(f"No images found in {images_dir}")
    
    img = cv2.imread(str(images[0]))
    if img is None:
        raise ValueError(f"Could not read image: {images[0]}")
    
    h, w = img.shape[:2]
    return w, h


def save_outputs(
    output_dir: Path,
    poses_output: list,
    visualizations: list,
    model_name: str
) -> None:
    """Save all tracking outputs to files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save poses in text format
    poses_txt_file = output_dir / "poses.txt"
    with open(poses_txt_file, 'w') as f:
        for item in poses_output:
            f.write(f"# Frame {item['frame']:04d}: confidence={item['confidence']:.4f}, "
                   f"pose_uv=({item['pose_uv'][0]}, {item['pose_uv'][1]})\n")
            np.savetxt(f, item['pose'], fmt='%.6f', delimiter='\t')
            f.write('\n')
    
    # Save poses as numpy array (shape: [num_frames, 4, 4])
    poses_array = np.array([item['pose'] for item in poses_output])
    poses_npy_file = output_dir / "poses.npy"
    np.save(poses_npy_file, poses_array)
    
    # Save OpenGL poses
    poses_gl_array = np.array([item['pose_gl'] for item in poses_output])
    poses_gl_npy_file = output_dir / "poses_gl.npy"
    np.save(poses_gl_npy_file, poses_gl_array)
    
    # Save metadata
    metadata = {
        'confidences': [item['confidence'] for item in poses_output],
        'pose_uv': [item['pose_uv'] for item in poses_output],
        'valid_line_prop': [item['valid_line_prop'] for item in poses_output],
        'frame_numbers': [item['frame'] for item in poses_output]
    }
    metadata_file = output_dir / "metadata.npy"
    np.save(metadata_file, metadata)
    
    # Save metadata as text for easy reading
    metadata_txt_file = output_dir / "metadata.txt"
    with open(metadata_txt_file, 'w') as f:
        f.write(f"# Tracking metadata for {model_name}\n")
        f.write(f"# Total frames: {len(poses_output)}\n")
        f.write(f"# Format: frame, confidence, pose_uv_u, pose_uv_v, valid_line_prop\n")
        for item in poses_output:
            f.write(f"{item['frame']:04d}\t{item['confidence']:.6f}\t"
                   f"{item['pose_uv'][0]}\t{item['pose_uv'][1]}\t"
                   f"{item['valid_line_prop']:.6f}\n")
    
    # Save visualization images
    vis_dir = output_dir / "visualizations"
    vis_dir.mkdir(exist_ok=True)
    for idx, vis_img in enumerate(visualizations):
        if vis_img is not None:
            vis_file = vis_dir / f"frame_{idx:04d}.png"
            cv2.imwrite(str(vis_file), cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR))
    
    print(f"\n✓ All outputs saved to: {output_dir}")
    print(f"  - Poses (text): {poses_txt_file}")
    print(f"  - Poses (numpy): {poses_npy_file} (shape: {poses_array.shape})")
    print(f"  - Poses OpenGL (numpy): {poses_gl_npy_file}")
    print(f"  - Metadata: {metadata_file} and {metadata_txt_file}")
    print(f"  - Visualizations: {vis_dir} ({len(visualizations)} images)")


def main():
    parser = argparse.ArgumentParser(
        description="Run pysrt3d 6DoF object tracking on a sequence of images",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Input directory structure:
  input_dir/
    ├── model.obj          # 3D model file (or any .obj file)
    ├── model.meta         # Metadata file (optional, auto-generated if missing)
    ├── K.txt              # Camera intrinsics (3x3 matrix)
    ├── pose.txt           # Initial pose (4x4 matrix)
    └── images/            # Directory containing images (.png or .jpg)
        ├── 0000.png
        ├── 0001.png
        └── ...

Output directory (default: ./user/output):
  output_dir/
    ├── poses.txt           # All poses in text format
    ├── poses.npy           # All poses as numpy array [N, 4, 4]
    ├── poses_gl.npy        # All poses in OpenGL coordinates [N, 4, 4]
    ├── metadata.npy         # Tracking metadata (confidences, pose_uv, etc.)
    ├── metadata.txt         # Metadata in text format
    └── visualizations/     # Rendered visualization images
        ├── frame_0000.png
        └── ...
        """
    )
    
    # Required arguments
    parser.add_argument(
        "--input_dir",
        type=str,
        required=True,
        help="Path to input directory containing model, camera intrinsics, initial pose, and images"
    )
    
    # Optional arguments
    parser.add_argument(
        "--output_dir",
        type=str,
        default="./user/output",
        help="Path to output directory (default: ./user/output)"
    )
    
    parser.add_argument(
        "--model_name",
        type=str,
        default=None,
        help="Model name (default: derived from model filename)"
    )
    
    # Model parameters
    parser.add_argument(
        "--unit_in_meter",
        type=float,
        default=1.0,
        help="Scale factor for model units (default: 1.0, use 0.001 for mm models)"
    )
    
    parser.add_argument(
        "--sphere_radius",
        type=float,
        default=0.8,
        help="Sphere radius for region generation (default: 0.8)"
    )
    
    parser.add_argument(
        "--threshold_init",
        type=float,
        default=0.0,
        help="Confidence threshold for initialization (default: 0.0 = no limit)"
    )
    
    parser.add_argument(
        "--threshold_track",
        type=float,
        default=0.0,
        help="Confidence threshold for tracking (default: 0.0 = no limit)"
    )
    
    parser.add_argument(
        "--kl_threshold",
        type=float,
        default=1.0,
        help="KL divergence threshold for confidence (default: 1.0)"
    )
    
    # Tracker parameters
    parser.add_argument(
        "--corr_iter",
        type=int,
        default=7,
        help="Correspondence update iterations (default: 7)"
    )
    
    parser.add_argument(
        "--pose_iter",
        type=int,
        default=2,
        help="Pose update iterations (default: 2)"
    )
    
    # Runtime options
    parser.add_argument(
        "--no_visualize",
        action="store_true",
        help="Disable interactive visualization (useful for batch processing)"
    )
    
    parser.add_argument(
        "--save_visualizations",
        action="store_true",
        default=True,
        help="Save visualization images (default: True)"
    )
    
    parser.add_argument(
        "--image_ext",
        type=str,
        nargs="+",
        default=["png", "jpg"],
        help="Image file extensions to process (default: png jpg)"
    )
    
    args = parser.parse_args()
    
    # Convert to Path objects
    input_dir = Path(args.input_dir).resolve()
    output_dir = Path(args.output_dir).resolve()
    
    if not input_dir.exists():
        print(f"Error: Input directory does not exist: {input_dir}")
        sys.exit(1)
    
    print(f"Input directory: {input_dir}")
    print(f"Output directory: {output_dir}")
    
    # Validate inputs
    print("\nValidating inputs...")
    model_path, meta_path, k_path, pose_path, images_dir = validate_inputs(input_dir)
    print(f"✓ Model: {model_path}")
    print(f"✓ Meta: {meta_path}")
    print(f"✓ Camera intrinsics: {k_path}")
    print(f"✓ Initial pose: {pose_path}")
    print(f"✓ Images: {images_dir}")
    
    # Load data
    print("\nLoading data...")
    K = load_camera_intrinsics(k_path)
    init_pose = load_initial_pose(pose_path)
    w, h = get_image_size(images_dir)
    
    # Get images
    images = []
    for ext in args.image_ext:
        images.extend(sorted(images_dir.glob(f"*.{ext}")))
    images = sorted(images)
    
    if not images:
        print(f"Error: No images found in {images_dir}")
        sys.exit(1)
    
    print(f"✓ Found {len(images)} images")
    print(f"✓ Image size: {w}x{h}")
    
    # Get model name
    model_name = args.model_name if args.model_name else model_path.stem
    
    # Initialize model
    print(f"\nInitializing model: {model_name}")
    model = pysrt3d.Model(
        name=model_name,
        model_path=str(model_path),
        meta_path=str(meta_path) if meta_path.exists() else "",
        unit_in_meter=args.unit_in_meter,
        shpere_radius=args.sphere_radius,
        threshold_init=args.threshold_init,
        threshold_track=args.threshold_track,
        kl_threshold=args.kl_threshold
    )
    
    # Initialize tracker
    print("Initializing tracker...")
    tracker = pysrt3d.Tracker(
        imwidth=w,
        imheight=h,
        K=K,
        corr_iter=args.corr_iter,
        pose_iter=args.pose_iter
    )
    
    tracker.add_model(model)
    tracker.setup()
    
    # Initialize renderer
    renderer = pysrt3d.Renderer(tracker)
    
    # Set initial pose
    print("Setting initial pose...")
    model.reset_pose(init_pose)
    
    # Tracking loop
    print(f"\nProcessing {len(images)} frames...")
    poses_output = []
    visualizations = []
    
    for idx, image_path in enumerate(images):
        # Read image
        image = cv2.imread(str(image_path))
        if image is None:
            print(f"Warning: Could not read image {image_path}, skipping...")
            visualizations.append(None)
            continue
        
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
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
            'pose': pose_6dof,
            'pose_gl': pose_gl,
            'confidence': conf,
            'pose_uv': pose_uv,
            'valid_line_prop': valid_line_prop
        })
        
        # Print progress
        if (idx + 1) % 10 == 0 or idx == 0:
            print(f"  Frame {idx:04d}/{len(images)-1:04d}: confidence={conf:.4f}, "
                  f"pose_uv=({pose_uv[0]}, {pose_uv[1]})")
        
        # Render visualization
        normal_image = renderer.render()
        if normal_image is not None:
            # Convert to RGB if needed
            if len(normal_image.shape) == 3:
                vis_img = normal_image.copy()
            else:
                vis_img = cv2.cvtColor(normal_image, cv2.COLOR_GRAY2RGB)
            
            # Add tracking info overlay
            cv2.putText(
                vis_img,
                f"{model_name}: {conf:.2f}",
                pose_uv,
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )
            
            visualizations.append(vis_img)
            
            # Show visualization if not disabled
            if not args.no_visualize:
                cv2.imshow('Tracking View', cv2.cvtColor(vis_img, cv2.COLOR_RGB2BGR))
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    print("\nTracking interrupted by user (pressed 'q')")
                    break
        else:
            visualizations.append(None)
    
    if not args.no_visualize:
        cv2.destroyAllWindows()
    
    # Save outputs
    print("\nSaving outputs...")
    if args.save_visualizations:
        save_outputs(output_dir, poses_output, visualizations, model_name)
    else:
        # Save only poses and metadata, no visualizations
        save_outputs(output_dir, poses_output, [], model_name)
    
    print("\n✓ Tracking complete!")


if __name__ == "__main__":
    main()
