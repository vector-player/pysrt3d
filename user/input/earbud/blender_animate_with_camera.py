"""
Blender Script to Animate Earbud with Camera Setup

This script creates a complete animation setup including:
- Earbud model with tracked poses
- Camera positioned to view the animation
- Optional: Camera tracking to follow the object

Usage in Blender:
1. Open Blender
2. Go to Scripting workspace
3. Open this script
4. Update the paths if needed
5. Run the script (Alt+P or click Run)
"""

import bpy
import numpy as np
from mathutils import Matrix, Vector
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR = Path(__file__).parent.resolve()
POSES_FILE = SCRIPT_DIR / "poses.npy"
MODEL_FILE = SCRIPT_DIR / "earbud_left.obj"
K_FILE = SCRIPT_DIR / "K.txt"  # Camera intrinsics (optional, for camera setup)

FPS = 30
START_FRAME = 1
SCALE_FACTOR = 1.0
USE_OPENGL_COORDS = False

# Camera settings
CAMERA_DISTANCE = 1.5  # Distance from origin (in Blender units)
CAMERA_HEIGHT = 0.5    # Height above ground
CAMERA_LOOK_AT_OBJECT = True  # Make camera track the object

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def opencv_to_blender_matrix(opencv_matrix):
    """Convert OpenCV to Blender coordinate system."""
    R = opencv_matrix[:3, :3]
    t = opencv_matrix[:3, 3]
    
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


def setup_camera(camera_distance=1.5, camera_height=0.5):
    """Setup camera with good viewing angle."""
    # Create or get camera
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add()
    camera = bpy.data.objects["Camera"]
    
    # Position camera
    camera.location = (camera_distance, -camera_distance, camera_height)
    camera.rotation_euler = (1.1, 0, 0.785)  # Look at origin
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    return camera


def add_track_constraint(camera, target_obj):
    """Add track constraint to camera to follow the object."""
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = target_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("="*60)
    print("Blender Earbud Animation with Camera Setup")
    print("="*60)
    
    # Clear scene (optional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Load model
    print(f"\nLoading model: {MODEL_FILE}")
    if not MODEL_FILE.exists():
        print(f"ERROR: Model file not found: {MODEL_FILE}")
        return
    
    bpy.ops.wm.obj_import(filepath=str(MODEL_FILE))
    obj = bpy.context.active_object
    if obj is None:
        print("ERROR: Failed to import model")
        return
    
    obj.name = "earbud_left"
    print(f"[OK] Model loaded: {obj.name}")
    
    # Load poses
    print(f"\nLoading poses: {POSES_FILE}")
    if not POSES_FILE.exists():
        print(f"ERROR: Poses file not found: {POSES_FILE}")
        return
    
    poses = np.load(str(POSES_FILE))
    num_frames = len(poses)
    print(f"[OK] Loaded {num_frames} poses")
    
    # Setup animation
    bpy.context.scene.frame_start = START_FRAME
    bpy.context.scene.frame_end = START_FRAME + num_frames - 1
    bpy.context.scene.render.fps = FPS
    print(f"\nAnimation: Frame {START_FRAME} to {START_FRAME + num_frames - 1} ({num_frames / FPS:.2f}s)")
    
    # Setup camera
    print("\nSetting up camera...")
    camera = setup_camera(CAMERA_DISTANCE, CAMERA_HEIGHT)
    print(f"[OK] Camera positioned at {camera.location}")
    
    # Add tracking constraint if requested
    if CAMERA_LOOK_AT_OBJECT:
        add_track_constraint(camera, obj)
        print("[OK] Camera tracking enabled")
    
    # Add light (optional)
    if "Light" not in bpy.data.objects:
        bpy.ops.object.light_add(type='SUN', location=(2, 2, 5))
        light = bpy.context.active_object
        light.data.energy = 3.0
        print("[OK] Light added")
    
    # Set keyframes
    print("\nSetting keyframes...")
    for i, pose_matrix in enumerate(poses):
        frame = START_FRAME + i
        blender_matrix = opencv_to_blender_matrix(pose_matrix)
        obj.matrix_world = blender_matrix
        obj.keyframe_insert(data_path="location", frame=frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{num_frames}...")
    
    # Set interpolation
    if obj.animation_data and obj.animation_data.action:
        for fcurve in obj.animation_data.action.fcurves:
            for keyframe in fcurve.keyframe_points:
                keyframe.interpolation = 'LINEAR'
    
    print(f"\n[OK] Keyframes set for {num_frames} frames")
    
    # Summary
    print("\n" + "="*60)
    print("Setup Complete!")
    print("="*60)
    print(f"Object: {obj.name}")
    print(f"Frames: {START_FRAME} to {START_FRAME + num_frames - 1}")
    print(f"Duration: {num_frames / FPS:.2f} seconds at {FPS} FPS")
    print(f"Camera: {'Tracking' if CAMERA_LOOK_AT_OBJECT else 'Fixed'}")
    print("\nControls:")
    print("  - Spacebar: Play/Pause animation")
    print("  - Right-click timeline: Scrub through frames")
    print("  - NumPad 0: Camera view")
    print("  - NumPad 7: Top view")
    print("  - NumPad 1: Front view")


if __name__ == "__main__":
    main()
