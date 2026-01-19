# Blender Animation Scripts

This directory contains Blender scripts to animate the earbud using the tracked poses from pysrt3d.

## Files

- `blender_animate.py` - Basic script to load model and apply poses as keyframes
- `blender_animate_with_camera.py` - Complete setup with camera and lighting
- `poses.npy` - Tracked poses (OpenCV coordinates)
- `poses_gl.npy` - Tracked poses (OpenGL coordinates)
- `earbud_left.obj` - 3D model file

## Usage

### Method 1: Basic Animation

1. Open Blender (3.0+)
2. Go to **Scripting** workspace (top menu)
3. Click **Open** and select `blender_animate.py`
4. Update paths in the script if needed (lines 18-20)
5. Click **Run Script** (or press Alt+P)
6. Play animation with Spacebar

### Method 2: Complete Setup (Recommended)

1. Open Blender
2. Go to **Scripting** workspace
3. Open `blender_animate_with_camera.py`
4. Run the script
5. The script will:
   - Load the earbud model
   - Apply all tracked poses as keyframes
   - Setup camera with good viewing angle
   - Add lighting
   - Enable camera tracking (optional)

## Configuration

Edit these variables in the script:

```python
FPS = 30  # Match your video frame rate
START_FRAME = 1  # Starting frame number in Blender
SCALE_FACTOR = 1.0  # Scale adjustment (1.0 = 1 Blender unit = 1 meter)
USE_OPENGL_COORDS = False  # True to use poses_gl.npy instead
```

## Coordinate System

The script automatically converts from pysrt3d's coordinate system to Blender's:

- **pysrt3d (OpenCV)**: X-right, Y-down, Z-forward
- **Blender**: X-right, Y-forward, Z-up

## Troubleshooting

### Model not loading
- Check that `earbud_left.obj` exists in the same directory
- Ensure the path in the script is correct

### Poses not loading
- Check that `poses.npy` exists
- Verify the file path in the script

### Animation looks wrong
- Try setting `USE_OPENGL_COORDS = True` to use `poses_gl.npy`
- Adjust `SCALE_FACTOR` if the object appears too large/small
- Check that the coordinate conversion is correct for your setup

### Camera view
- Press **NumPad 0** to view from camera
- Adjust camera position in the script if needed
- Disable camera tracking by setting `CAMERA_LOOK_AT_OBJECT = False`

## Output

After running the script:
- The earbud will be animated through all 310 frames
- Keyframes are set for location and rotation
- You can render the animation or export it

## Rendering

To render the animation:
1. Set up your render settings (Resolution, Output path, etc.)
2. Go to **Render** > **Render Animation**
3. Or press **Ctrl+F12**

## Notes

- The poses are in meters (pysrt3d default)
- Blender uses 1 unit = 1 meter by default
- If your model is in different units (e.g., mm), adjust `SCALE_FACTOR`
- The animation uses linear interpolation for smooth motion
