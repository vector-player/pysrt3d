"""
Blender Standalone Animation Script - No External Files Required

This script creates a cube and animates it using embedded pose data.
All pose data is included directly in the script - no external files needed.

Usage in Blender:
1. Open Blender
2. Go to Scripting workspace
3. Paste this entire script
4. Run the script (Alt+P or click Run)
"""

import bpy
import numpy as np
from mathutils import Matrix, Vector
from pathlib import Path

# ============================================================================
# CONFIGURATION
# ============================================================================

FPS = 30  # Frames per second
START_FRAME = 1  # Starting frame number
SCALE_FACTOR = 1.0  # Scale factor (1.0 = 1 Blender unit = 1 meter)

# Object settings
CUBE_SIZE = 0.02  # Size of the cube in meters (2cm for earbud scale)
USE_CUBE = True  # Set to False to try loading model (if available)

# Camera settings
CAMERA_DISTANCE = 0.15  # Distance from origin (adjusted for 5cm object)
CAMERA_HEIGHT = 0.05
CAMERA_LOOK_AT_OBJECT = True

# ============================================================================
# EMBEDDED POSE DATA
# ============================================================================
# This data is automatically generated from poses.npy
# Format: List of 4x4 matrices (310 frames)
# To regenerate: Run generate_embedded_poses.py

# Try to load from separate file first (if available)
def load_embedded_poses():
    """Load embedded poses - tries file first, then uses fallback data."""
    script_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    embedded_file = script_dir / "embedded_poses_data.py"
    
    if embedded_file.exists():
        try:
            # Read and execute the embedded file
            with open(embedded_file, 'r') as f:
                code = f.read()
            namespace = {}
            exec(code, namespace)
            if 'EMBEDDED_POSES' in namespace:
                print(f"[OK] Loaded embedded poses from file")
                return namespace['EMBEDDED_POSES']
        except Exception as e:
            print(f"[WARNING] Could not load embedded file: {e}")
    
    # Fallback: minimal data (just first frame as example)
    return [
        [[-0.171190, 0.000117, 0.985238, 0.000004],
         [-0.899612, 0.407739, -0.156360, -0.000021],
         [-0.401737, -0.913099, -0.069695, 0.050406],
         [0.000000, 0.000000, 0.000000, 1.000000]],
    ]

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def opencv_to_blender_matrix(opencv_matrix):
    """
    Convert OpenCV coordinate system to Blender coordinate system.
    
    OpenCV: X-right, Y-down, Z-forward
    Blender: X-right, Y-forward, Z-up
    """
    if isinstance(opencv_matrix, list):
        opencv_matrix = np.array(opencv_matrix)
    
    R = opencv_matrix[:3, :3]
    t = opencv_matrix[:3, 3]
    
    # Conversion matrix
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


def load_poses_from_file(filepath):
    """Try to load poses from file if available."""
    try:
        poses = np.load(str(filepath))
        print(f"[OK] Loaded poses from file: {filepath}")
        return poses.tolist()
    except Exception as e:
        print(f"[WARNING] Could not load poses from file: {e}")
        return None


def setup_camera(camera_distance=0.15, camera_height=0.05):
    """Setup camera with good viewing angle."""
    # Create or get camera
    if "Camera" not in bpy.data.objects:
        bpy.ops.object.camera_add()
    camera = bpy.data.objects["Camera"]
    
    # Position camera (adjusted for close-up view of small object)
    camera.location = (camera_distance, -camera_distance, camera_height)
    camera.rotation_euler = (1.1, 0, 0.785)  # Look at origin
    
    # Set camera settings for close-up
    camera.data.lens = 50  # 50mm lens
    camera.data.sensor_width = 36  # Full frame sensor
    
    # Set as active camera
    bpy.context.scene.camera = camera
    
    return camera


def add_track_constraint(camera, target_obj):
    """Add track constraint to camera to follow the object."""
    constraint = camera.constraints.new(type='TRACK_TO')
    constraint.target = target_obj
    constraint.track_axis = 'TRACK_NEGATIVE_Z'
    constraint.up_axis = 'UP_Y'


def create_cube(size=0.02, name="earbud_cube"):
    """Create a cube to represent the earbud."""
    # Delete existing cube if it exists
    if name in bpy.data.objects:
        bpy.data.objects.remove(bpy.data.objects[name])
    
    # Create new cube
    bpy.ops.mesh.primitive_cube_add(size=size)
    obj = bpy.context.active_object
    obj.name = name
    
    # Add some material for visibility
    mat = bpy.data.materials.new(name=f"{name}_material")
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0.8, 0.2, 0.2, 1.0)  # Red color
    bsdf.inputs["Metallic"].default_value = 0.8
    bsdf.inputs["Roughness"].default_value = 0.2
    obj.data.materials.append(mat)
    
    return obj


def try_load_model(model_path):
    """Try to load the OBJ model if available."""
    try:
        if Path(model_path).exists():
            bpy.ops.wm.obj_import(filepath=str(model_path))
            obj = bpy.context.active_object
            if obj:
                obj.name = "earbud_left"
                print(f"[OK] Model loaded from: {model_path}")
                return obj
    except Exception as e:
        print(f"[WARNING] Could not load model: {e}")
    return None


# ============================================================================
# MAIN SCRIPT
# ============================================================================

def main():
    print("="*60)
    print("Blender Standalone Earbud Animation")
    print("="*60)
    
    # Clear existing mesh objects (optional)
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete(use_global=False)
    
    # Try to load poses from file first, fallback to embedded data
    script_dir = Path(__file__).parent if '__file__' in globals() else Path.cwd()
    poses_file = script_dir / "poses.npy"
    
    poses_data = load_poses_from_file(poses_file)
    
    if poses_data is None:
        print("\nTrying to load embedded pose data...")
        poses_data = load_embedded_poses()
        if len(poses_data) <= 1:
            print("[ERROR] Embedded pose data not found or incomplete!")
            print("        Please ensure embedded_poses_data.py exists in the same directory,")
            print("        or run generate_embedded_poses.py to create it.")
            return
    else:
        print("\nUsing poses from file...")
    
    num_frames = len(poses_data)
    print(f"[OK] Loaded {num_frames} poses")
    
    if num_frames == 0:
        print("ERROR: No pose data available!")
        return
    
    # Create object (cube or load model)
    obj = None
    if USE_CUBE:
        print(f"\nCreating cube (size: {CUBE_SIZE}m)...")
        obj = create_cube(size=CUBE_SIZE, name="earbud_cube")
    else:
        # Try to load model
        model_path = script_dir / "earbud_left.obj"
        print(f"\nTrying to load model from: {model_path}")
        obj = try_load_model(model_path)
        
        if obj is None:
            print("Model not found, creating cube instead...")
            obj = create_cube(size=CUBE_SIZE, name="earbud_cube")
    
    if obj is None:
        print("ERROR: Failed to create object!")
        return
    
    print(f"[OK] Object created: {obj.name}")
    
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
    
    # Add light
    if "Light" not in bpy.data.objects:
        bpy.ops.object.light_add(type='SUN', location=(0.1, -0.1, 0.2))
        light = bpy.context.active_object
        light.data.energy = 5.0
        print("[OK] Light added")
    
    # Set keyframes
    print("\nSetting keyframes...")
    for i, pose_matrix in enumerate(poses_data):
        frame = START_FRAME + i
        
        # Convert coordinate system
        blender_matrix = opencv_to_blender_matrix(pose_matrix)
        obj.matrix_world = blender_matrix
        
        # Insert keyframes
        obj.keyframe_insert(data_path="location", frame=frame)
        obj.keyframe_insert(data_path="rotation_euler", frame=frame)
        
        if (i + 1) % 50 == 0:
            print(f"  {i + 1}/{num_frames}...")
    
    # Set interpolation to linear for smooth motion
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
    print("  - NumPad 0: Camera view")
    print("  - NumPad 7: Top view")
    print("  - NumPad 1: Front view")


if __name__ == "__main__":
    main()
