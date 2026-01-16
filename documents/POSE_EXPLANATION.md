# Understanding the 6DoF Pose Matrix and Image Relationship

## Is the Pose 2D or 3D?

**The pose is a 3D transformation matrix** (4×4 homogeneous transformation matrix) that represents the object's position and orientation in **3D space**.

### What the 4×4 Matrix Contains

```
[R00  R01  R02  tx]   ← 3×3 Rotation Matrix (3D orientation)
[R10  R11  R12  ty]   ← 3D Translation Vector (3D position)
[R20  R21  R22  tz]
[0    0    0    1 ]
```

- **Top-left 3×3 block**: Rotation matrix describing the object's **3D orientation** (roll, pitch, yaw)
- **Right column (top 3)**: Translation vector `[tx, ty, tz]` describing the object's **3D position** in meters
- **Bottom row**: Homogeneous coordinates padding `[0, 0, 0, 1]`

### Example from Your Data

```
0.78603    -0.587438   0.19255    0.281848  ← tx = 0.282m (X position)
0.604647    0.795404  -0.0416517 -0.166599  ← ty = -0.167m (Y position)
-0.128687   0.149164   0.980401   0.731918  ← tz = 0.732m (Z position, depth)
0           0          0          1
```

This means:
- The object is located at 3D position: **(0.282, -0.167, 0.732) meters** from the camera
- The object is rotated according to the 3×3 rotation matrix

---

## How Does the 3D Pose Match to 2D Images?

The 3D pose is **projected onto 2D images** using the camera projection model. Here's the transformation chain:

### Transformation Pipeline

```
3D Model Points (Object Space)
    ↓ [Pose Matrix: body2world]
3D World/Camera Coordinates
    ↓ [Camera Intrinsics K]
2D Image Coordinates (pixels)
```

### Step-by-Step Process

#### 1. **3D Model → 3D Camera Coordinates**

The pose matrix transforms 3D points from the object's coordinate system to the camera's coordinate system:

```python
# For a 3D point P_object in object coordinates:
P_camera = Pose @ P_object  # Matrix multiplication

# Or explicitly:
P_camera = R @ P_object + t  # Rotation + Translation
```

Where:
- `P_object = [x_obj, y_obj, z_obj, 1]` (homogeneous coordinates)
- `R` = 3×3 rotation matrix from pose
- `t` = [tx, ty, tz] translation from pose
- `P_camera = [X, Y, Z]` = 3D position in camera frame

#### 2. **3D Camera Coordinates → 2D Image Coordinates**

The camera intrinsics matrix `K` projects 3D camera coordinates to 2D image pixels:

```python
# Camera projection
[u]   [fx  0  cx]   [X]
[v] = [0  fy  cy] @ [Y]  / Z
[1]   [0   0   1]   [Z]

# Or:
u = (fx * X + cx * Z) / Z = fx * (X/Z) + cx
v = (fy * Y + cy * Z) / Z = fy * (Y/Z) + cy
```

Where:
- `[u, v]` = 2D pixel coordinates in the image
- `fx, fy` = focal lengths (from K.txt)
- `cx, cy` = principal point (from K.txt)
- `X, Y, Z` = 3D coordinates in camera frame

### Example from Your Data

**Camera Intrinsics (K.txt):**
```
481.34025  0.0        329.4003
0.0        481.8243   260.3788
0.0        0.0        1.0
```

**Pose Translation:** `[tx=0.282, ty=-0.167, tz=0.732]`

**Projection to 2D:**
```python
# The object center projects to:
u = 481.34025 * (0.282 / 0.732) + 329.4003 ≈ 514 pixels
v = 481.8243 * (-0.167 / 0.732) + 260.3788 ≈ 150 pixels
```

This is exactly what `model.pose_uv` returns - the 2D projection of the object's center!

---

## Coordinate Systems

### 1. **Object/Model Space**
- Origin: Object's local coordinate system
- Units: Defined by `unit_in_meter` (e.g., 0.001 for millimeters)
- The 3D model (.obj file) is defined in this space

### 2. **World/Camera Space** (OpenCV Convention)
- Origin: Camera center
- X-axis: Right
- Y-axis: Down
- Z-axis: Forward (into the scene)
- Units: Meters
- The pose matrix transforms from object space to this space

### 3. **Image Space**
- Origin: Top-left corner of image
- X-axis (u): Right (columns)
- Y-axis (v): Down (rows)
- Units: Pixels
- The camera intrinsics K project from camera space to this space

---

## How It Works in the Tracking Loop

### For Each Frame:

1. **Load Image** (2D, pixels)
   ```python
   image = cv2.imread('frame_0000.png')  # 2D array of pixels
   ```

2. **Current Pose** (3D, meters)
   ```python
   pose = model.pose  # 4×4 matrix: 3D position + orientation
   ```

3. **Project 3D Model to 2D**
   - The renderer uses the pose to project the 3D model onto the 2D image
   - Creates a "synthetic view" of what the object should look like at that pose

4. **Compare with Actual Image**
   - Compares the synthetic projection with the actual image
   - Finds correspondences (matching points/lines)

5. **Update Pose** (still 3D)
   - Optimizes the 3D pose to better match the image
   - Updates the 4×4 matrix

6. **Get 2D Projection** (for visualization)
   ```python
   pose_uv = model.pose_uv  # 2D projection: (u, v) in pixels
   ```

---

## Visual Representation

```
                    ┌─────────────────┐
                    │   3D Model      │
                    │  (Object Space) │
                    │  .obj file      │
                    └────────┬────────┘
                             │
                             │ [Pose Matrix]
                             │ body2world
                             ↓
                    ┌─────────────────┐
                    │  Camera Space   │
                    │  (3D: X, Y, Z)  │
                    │  Units: meters  │
                    └────────┬────────┘
                             │
                             │ [Camera Intrinsics K]
                             │ Projection
                             ↓
                    ┌─────────────────┐
                    │   Image Space   │
                    │  (2D: u, v)     │
                    │  Units: pixels  │
                    └─────────────────┘
```

---

## Key Points

1. **Pose is 3D**: The 4×4 matrix represents full 6DoF (6 Degrees of Freedom):
   - 3 DoF for rotation (roll, pitch, yaw)
   - 3 DoF for translation (x, y, z)

2. **Images are 2D**: Each input image is a 2D projection of the 3D scene

3. **Connection via Projection**: The camera intrinsics matrix `K` connects 3D poses to 2D images through perspective projection

4. **Tracking Process**: 
   - Starts with initial 3D pose
   - Projects 3D model to 2D for each frame
   - Compares with actual 2D image
   - Updates 3D pose to minimize error
   - Repeats for next frame

5. **Output**: 
   - `model.pose`: 3D pose (4×4 matrix)
   - `model.pose_uv`: 2D projection of object center (u, v pixels)
   - `model.pose_gl`: 3D pose in OpenGL coordinates (for rendering)

---

## Code Example: Understanding the Relationship

```python
import numpy as np
import cv2

# Load camera intrinsics
K = np.loadtxt('K.txt')  # 3×3 matrix

# Load initial pose
pose = np.loadtxt('pose.txt')  # 4×4 matrix

# Extract rotation and translation
R = pose[:3, :3]  # 3×3 rotation matrix
t = pose[:3, 3]   # 3×1 translation vector [tx, ty, tz]

# Example: Transform a 3D point from object to camera space
point_object = np.array([0, 0, 0, 1])  # Object origin
point_camera = pose @ point_object  # = [tx, ty, tz, 1]

# Project to 2D image coordinates
X, Y, Z = point_camera[:3]
u = (K[0,0] * X + K[0,2] * Z) / Z  # fx * (X/Z) + cx
v = (K[1,1] * Y + K[1,2] * Z) / Z  # fy * (Y/Z) + cy

print(f"3D position in camera frame: ({X:.3f}, {Y:.3f}, {Z:.3f}) meters")
print(f"2D projection in image: ({u:.1f}, {v:.1f}) pixels")
```

This is exactly what happens internally when you call `model.pose_uv`!
