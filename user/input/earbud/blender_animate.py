"""
Blender Script to Animate Earbud Using Tracked Poses

This script loads the earbud model and applies the tracked poses as keyframes
to create an animation in Blender.

Usage in Blender:
1. Open Blender
2. Go to Scripting workspace
3. Open this script
4. Update the paths in the script if needed
5. Run the script (Alt+P or click Run)
"""

import bpy
import bmesh
import numpy as np
from mathutils import Matrix, Vector, Euler
from pathlib import Path
import os

# ============================================================================
# CONFIGURATION - Update these paths if needed
# ============================================================================

# Path to the pose data (relative to this script or absolute)
SCRIPT_DIR = Path(__file__).parent.resolve()
POSES_FILE = SCRIPT_DIR / "poses.npy"  # or "poses_gl.npy" for OpenGL coordinates
MODEL_FILE = SCRIPT_DIR / "earbud_left.obj"

# Animation settings
FPS = 30  # Frames per second (adjust to match your video)
START_FRAME = 1  # Blender frame to start animation

# Scale factor (pysrt3d uses meters, Blender default is 1 unit = 1m, but you may need to adjust)
SCALE_FACTOR = 1.0  # 1.0 = 1 Blender unit = 1 meter

# Coordinate system conversion
# pysrt3d uses OpenCV coordinates: X-right, Y-down, Z-forward
# Blender uses: X-right, Y-forward, Z-up (in default view)
USE_OPENGL_COORDS = False  # Set to True to use poses_gl.npy instead

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def opencv_to_blender_matrix(opencv_matrix):
    """
    Convert OpenCV coordinate system to Blender coordinate system.
    
    OpenCV: X-right, Y-down, Z-forward
    Blender: X-right, Y-forward, Z-up
    
    Conversion:
    - Blender X = OpenCV X
    - Blender Y = -OpenCV Z
    - Blender Z = OpenCV Y
    """
    # Extract rotation and translation
    R = opencv_matrix[:3, :3]
    t = opencv_matrix[:3, 3]
    
    # Create conversion matrix
    # Blender X = OpenCV X
    # Blender Y = -OpenCV Z  
    # Blender Z = OpenCV Y
    convert = np.array([
        [1,  0,  0],
        [0,  0, -1],
        [0,  1,  0]
    ])
    
    # Convert rotation
    R_blender = convert @ R @ convert.T
    
    # Convert translation
    t_blender = convert @ t
    
    # Create 4x4 matrix for Blender
    matrix = np.eye(4)
    matrix[:3, :3] = R_blender
    matrix[:3, 3] = t_blender * SCALE_FACTOR
    
    return Matrix(matrix.tolist())


def opengl_to_blender_matrix(opengl_matrix):
    """
    Convert OpenGL coordinate system to Blender coordinate system.
    
    OpenGL: X-right, Y-up, Z-backward
    Blender: X-right, Y-forward, Z-up
    
    Conversion:
    - Blender X = OpenGL X
    - Blender Y = -OpenGL Z
    - Blender Z = OpenGL Y
    """
    R = opengl_matrix[:3, :3]
    t = opengl_matrix[:3, 3]
    
    convert = np.array([
        [1,  0,  0],
        [0,  0, -1],
        [0,  1,  0]
    ])
    
    R_blender = convert @ R @ convert.T
    t_blender = convert @ t
    
    matrix = np.eye(4)
    matrix[:3, :3] = R_blender
    matrix[:3, 3] = t_blender * SCALE_FACTOR
    
    return Matrix(matrix.tolist())


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("="*60)
    print("Blender Earbud Animation Script")
    print("="*60)
    
    # Clear existing mesh objects (optional - comment out if you want to keep existing objects)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Load the 3D model
    print(f"\nLoading model: {MODEL_FILE}")
    if not MODEL_FILE.exists():
        print(f"ERROR: Model file not found: {MODEL_FILE}")
        return
    
    # Import OBJ file
    bpy.ops.wm.obj_import(filepath=str(MODEL_FILE))
    
    # Get the imported object
    obj = bpy.context.active_object
    if obj is None:
        print("ERROR: Failed to import model")
        return
    
    obj.name = "earbud_left"
    print(f"[OK] Model loaded: {obj.name}")
    
    # Load pose data
    print(f"\nLoading poses: {POSES_FILE}")
    if not POSES_FILE.exists():
        print(f"ERROR: Poses file not found: {POSES_FILE}")
        return
    
    poses = np.load(str(POSES_FILE))
    num_frames = len(poses)
    print(f"[OK] Loaded {num_frames} poses")
    
    # Set animation frame range
    bpy.context.scene.frame_start = START_FRAME
    bpy.context.scene.frame_end = START_FRAME + num_frames - 1
    bpy.context.scene.render.fps = FPS
    print(f"\nAnimation range: Frame {START_FRAME} to {START_FRAME + num_frames - 1}")
    print(f"FPS: {FPS}")
    
    # Convert poses and set keyframes
    print("\nSetting keyframes...")
    for i, pose_matrix in enumerate(poses):
        frame = START_FRAME + i
        
        # Convert coordinate system
        if USE_OPENGL_COORDS:
            blender_matrix = opengl_to_blender_matrix(pose_matrix)
        else:
            blender_matrix = opencv_to_blender_matrix(pose_matrix)
        
        # Set object transformation
        obj.matrix_world = blender_matrix
        
        # Insert keyframes for location and rotation
        obj.keyframe_insert(data_path="location", frame=frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        if (i + 1) % 50 == 0:
            print(f"  Processed {i + 1}/{num_frames} frames...")
    
    print(f"[OK] Keyframes set for {num_frames} frames")
    
    # Set interpolation mode (optional)
    # Linear interpolation for smoother motion
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'LINEAR'
    
    print("\n" + "="*60)
    print("Animation setup complete!")
    print("="*60)
    print(f"\nObject: {obj.name}")
    print(f"Frames: {START_FRAME} to {START_FRAME + num_frames - 1}")
    print(f"Total duration: {(num_frames / FPS):.2f} seconds")
    print("\nYou can now:")
    print("  - Play the animation (Spacebar)")
    print("  - Render the animation")
    print("  - Adjust camera/view as needed")


if __name__ == "__main__":
    main()
