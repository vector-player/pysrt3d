#!/usr/bin/env python3
"""
Estimate camera intrinsics (K-matrix) from an image using Depth-Anything-3 (DA3).

This script uses Depth-Anything-3 (DA3) to automatically estimate camera
intrinsics from a single image, without requiring a calibration pattern.

Supports two packages:
  - awesome-depth-anything-3 (recommended, PyPI package)
  - depth-anything-v3 (original, from GitHub)
"""

import argparse
import sys
from pathlib import Path
import numpy as np
import cv2

# Try to import awesome-depth-anything-3 (preferred, PyPI package)
try:
    from depth_anything_3.api import DepthAnything3
    USE_AWESOME_DA3 = True
except ImportError:
    USE_AWESOME_DA3 = False
    # Fallback to original depth-anything-v3 (if available)
    try:
        from depth_anything_v3 import DepthAnythingV3
    except ImportError:
        print("Error: Neither awesome-depth-anything-3 nor depth-anything-v3 package found.")
        print("Please install one of the following:")
        print("  pip install awesome-depth-anything-3  (recommended)")
        print("  # OR install from GitHub:")
        print("  pip install git+https://github.com/ByteDance-Seed/Depth-Anything-3.git")
        sys.exit(1)


def estimate_k_matrix(image_path: Path, output_path: Path) -> bool:
    """
    Estimate K-matrix from an image using Depth-Anything-3.
    
    Args:
        image_path: Path to input image file
        output_path: Path to output K-matrix file (should end with .txt)
    
    Returns:
        True if successful, False otherwise
    """
    # Validate input image exists
    if not image_path.exists():
        print(f"Error: Image file not found: {image_path}")
        return False
    
    # Validate output directory exists
    output_dir = output_path.parent
    if not output_dir.exists():
        print(f"Creating output directory: {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)
    
    # Load image
    print(f"Loading image: {image_path}")
    image = cv2.imread(str(image_path))
    if image is None:
        print(f"Error: Could not read image file: {image_path}")
        print("Please ensure the file is a valid image format (PNG, JPG, etc.)")
        return False
    
    # Convert BGR to RGB (DA3 expects RGB)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    h, w = image.shape[:2]
    print(f"Image size: {w} x {h} pixels")
    
    # Initialize DA3 (using appropriate API)
    print("Initializing Depth-Anything-3...")
    try:
        if USE_AWESOME_DA3:
            # Use awesome-depth-anything-3 API
            print("Using awesome-depth-anything-3 package...")
            # Try to load a model (DA3-BASE is a good default, can be changed)
            model_name = "depth-anything/DA3-BASE"  # Can be DA3-SMALL, DA3-BASE, DA3-LARGE, etc.
            try:
                da3_model = DepthAnything3.from_pretrained(model_name)
            except Exception as e:
                print(f"Warning: Failed to load {model_name}, trying DA3-SMALL...")
                model_name = "depth-anything/DA3-SMALL"
                da3_model = DepthAnything3.from_pretrained(model_name)
        else:
            # Use original depth-anything-v3 API
            print("Using depth-anything-v3 package...")
            da3_model = DepthAnythingV3()
    except Exception as e:
        print(f"Error: Failed to initialize Depth-Anything-3: {e}")
        print("This may be due to missing model files or GPU issues.")
        return False
    
    # Process image to get camera intrinsics
    print("Processing image with DA3...")
    try:
        if USE_AWESOME_DA3:
            # awesome-depth-anything-3 API: inference expects list of images
            output = da3_model.inference(images=[image_rgb])
            # Extract intrinsics from output (shape: [N, 3, 3] for N images)
            intrinsics_tensor = output.intrinsics
            if intrinsics_tensor is None:
                print("Error: Camera intrinsics not found in DA3 output.")
                print("Available attributes:", dir(output))
                return False
            # Convert tensor to numpy and get first image's intrinsics
            if hasattr(intrinsics_tensor, 'cpu'):
                intrinsics_tensor = intrinsics_tensor.cpu()
            if hasattr(intrinsics_tensor, 'numpy'):
                K_estimated = intrinsics_tensor.numpy()[0]  # Get first image's K-matrix
            else:
                K_estimated = np.array(intrinsics_tensor)[0]
            
            # Extract parameters from K-matrix
            fx = float(K_estimated[0, 0])
            fy = float(K_estimated[1, 1])
            cx = float(K_estimated[0, 2])
            cy = float(K_estimated[1, 2])
        else:
            # Original depth-anything-v3 API
            result = da3_model.process_image(image_rgb)
            
            # Extract camera intrinsics
            if 'camera_intrinsics' not in result:
                print("Error: Camera intrinsics not found in DA3 result.")
                print("Available keys:", list(result.keys()))
                return False
            
            camera_intrinsics = result['camera_intrinsics']
            
            # Check if required keys exist
            required_keys = ['fx', 'fy', 'cx', 'cy']
            missing_keys = [key for key in required_keys if key not in camera_intrinsics]
            if missing_keys:
                print(f"Error: Missing camera intrinsics keys: {missing_keys}")
                print("Available keys:", list(camera_intrinsics.keys()))
                return False
            
            fx = camera_intrinsics['fx']
            fy = camera_intrinsics['fy']
            cx = camera_intrinsics['cx']
            cy = camera_intrinsics['cy']
    except Exception as e:
        print(f"Error: Failed to process image: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print(f"Estimated camera intrinsics:")
    print(f"  fx (focal length X): {fx:.6f} pixels")
    print(f"  fy (focal length Y): {fy:.6f} pixels")
    print(f"  cx (principal point X): {cx:.6f} pixels")
    print(f"  cy (principal point Y): {cy:.6f} pixels")
    
    # Construct K-matrix
    K = np.array([
        [fx,  0, cx],
        [0,  fy, cy],
        [0,   0,  1]
    ], dtype=np.float32)
    
    # Save K-matrix to file
    print(f"\nSaving K-matrix to: {output_path}")
    np.savetxt(str(output_path), K, fmt='%.6f')
    
    # Verify the saved file
    if output_path.exists():
        print("✓ K-matrix saved successfully!")
        print(f"\nK-matrix (3x3):")
        print(K)
        print(f"\nFile format: Space-separated values, 3 rows x 3 columns")
        return True
    else:
        print(f"Error: Failed to save K-matrix to {output_path}")
        return False


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(
        description="Estimate camera intrinsics (K-matrix) from an image using Depth-Anything-3",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Estimate K-matrix from an image
  python estimate_k_matrix.py --image frame_0000.png --output K.txt
  
  # Specify full paths
  python estimate_k_matrix.py --image /path/to/image.png --output /path/to/K.txt
  
  # Use with pysrt3d
  python estimate_k_matrix.py --image first_frame.png --output K.txt
  # Then use K.txt with pysrt3d.Tracker(K=np.loadtxt('K.txt'))
        """
    )
    
    parser.add_argument(
        '--image',
        type=str,
        required=True,
        help='Path to input image file (PNG, JPG, etc.)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        required=True,
        help='Path to output K-matrix file (should end with .txt)'
    )
    
    args = parser.parse_args()
    
    # Convert to Path objects
    image_path = Path(args.image).resolve()
    output_path = Path(args.output).resolve()
    
    # Validate output file extension
    if output_path.suffix.lower() != '.txt':
        print(f"Warning: Output file should have .txt extension, got: {output_path.suffix}")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != 'y':
            print("Aborted.")
            return 1
    
    # Estimate K-matrix
    success = estimate_k_matrix(image_path, output_path)
    
    if success:
        print("\n" + "="*60)
        print("SUCCESS: K-matrix estimation completed!")
        print("="*60)
        print(f"\nYou can now use this K-matrix with pysrt3d:")
        print(f"  K = np.loadtxt('{output_path}')")
        print(f"  tracker = pysrt3d.Tracker(imwidth=w, imheight=h, K=K)")
        return 0
    else:
        print("\n" + "="*60)
        print("ERROR: K-matrix estimation failed!")
        print("="*60)
        return 1


if __name__ == '__main__':
    sys.exit(main())
