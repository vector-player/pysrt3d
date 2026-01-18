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

#### 1. **3D Model (Object Space) → 3D Camera Coordinates (Camera Space)**

The pose matrix transforms 3D points from the **object's coordinate system** (object space) to the **camera's coordinate system** (camera space):

```python
# For a 3D point P_object in object coordinates:
P_camera = Pose @ P_object  # Matrix multiplication

# Or explicitly:
P_camera = R @ P_object + t  # Rotation + Translation
```

Where:
- `P_object = [x_obj, y_obj, z_obj, 1]` (homogeneous coordinates in **object space**)
  - These coordinates are relative to the object's origin
  - Units are defined by `unit_in_meter` (e.g., millimeters if `unit_in_meter=0.001`)
- `R` = 3×3 rotation matrix from pose (object orientation in camera frame)
- `t` = [tx, ty, tz] translation from pose (object position in camera frame, in meters)
- `P_camera = [X, Y, Z]` = 3D position in **camera space** (always in meters)
  - These coordinates are relative to the camera center
  - X = right, Y = down, Z = forward (OpenCV convention)

**Key Transformation:**
- **Input**: Point in object space (e.g., `(100, 50, 25)` in model units)
- **Output**: Same point in camera space (e.g., `(0.282, -0.167, 0.732)` in meters)
- **What changes**: The coordinate system and units (object → camera, model units → meters)
- **What stays the same**: The physical point in 3D space

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

### 1. **Object/Model Space** (3D Model Coordinates)

**Definition:** The coordinate system where the 3D model (.obj file) is defined. This is the object's **local coordinate system**.

**Characteristics:**
- **Origin**: Object's local reference point (often the object's center or a specific vertex)
- **Units**: Defined by `unit_in_meter` parameter (e.g., 0.001 for millimeters, 1.0 for meters)
- **Orientation**: Fixed relative to the object (e.g., front/back, up/down as defined in the model)
- **Purpose**: Describes the object's geometry independently of its position in the scene
- **Static**: Never changes - the model geometry is fixed

**Example:**
- A vertex at `(100, 50, 25)` in model coordinates means:
  - 100 units along the object's X-axis
  - 50 units along the object's Y-axis
  - 25 units along the object's Z-axis
- If `unit_in_meter = 0.001`, this represents `(0.1, 0.05, 0.025)` meters in the object's local frame

**Key Point:** Model coordinates are **relative to the object itself**, not the camera or world.

### 2. **Camera Space** (3D Camera Coordinates)

**Definition:** The coordinate system centered at the camera, used to describe where points are **relative to the camera**.

**Characteristics:**
- **Origin**: Camera center (optical center)
- **Units**: Always **meters** (regardless of model units)
- **Orientation** (OpenCV Convention):
  - **X-axis**: Right (positive X = to the right of camera)
  - **Y-axis**: Down (positive Y = below camera)
  - **Z-axis**: Forward (positive Z = into the scene, away from camera)
- **Purpose**: Describes the object's position and orientation relative to the camera
- **Dynamic**: Changes as the object moves relative to the camera

**Example:**
- A point at `(0.282, -0.167, 0.732)` in camera coordinates means:
  - 0.282 meters to the **right** of the camera
  - 0.167 meters **above** the camera (negative Y = up in OpenCV)
  - 0.732 meters **in front** of the camera (depth)

**Key Point:** Camera coordinates are **relative to the camera**, describing where the object is in the scene.

### 3. **Image Space** (2D Image Coordinates)

- **Origin**: Top-left corner of image
- **X-axis (u)**: Right (columns)
- **Y-axis (v)**: Down (rows)
- **Units**: Pixels
- **Purpose**: 2D pixel locations in the image
- The camera intrinsics K project from camera space to this space

---

## Understanding Object Space vs Camera Space

### Key Differences

| Aspect | Object Space (Model Coordinates) | Camera Space (Camera Coordinates) |
|--------|----------------------------------|----------------------------------|
| **Reference Frame** | Object's local coordinate system | Camera's coordinate system |
| **Origin** | Object's center/reference point | Camera center |
| **Units** | Defined by `unit_in_meter` | Always meters |
| **Orientation** | Fixed relative to object | Fixed relative to camera |
| **Changes With** | Never changes (model is static) | Changes as object moves relative to camera |
| **Purpose** | Define object geometry | Define object position in scene |
| **Example Point** | `(100, 50, 25)` in model units | `(0.282, -0.167, 0.732)` in meters |

### Why Both Are Needed

1. **Object Space** is needed because:
   - The 3D model (.obj file) is defined in its own coordinate system
   - Model geometry is static and doesn't change
   - Allows us to describe the object independently of where it is in the scene

2. **Camera Space** is needed because:
   - The camera sees the world from its own perspective
   - To project to 2D, we need to know where points are relative to the camera
   - The pose matrix tells us where the object is relative to the camera

3. **The Pose Matrix** bridges them:
   - Transforms points from object space to camera space
   - Encodes both position (translation) and orientation (rotation)
   - Enables projection to 2D image coordinates

### Transformation Example

```python
import numpy as np

# 1. A point in the 3D model (object space)
# This is a vertex from your .obj file
point_model = np.array([100, 50, 25, 1])  # In model units (e.g., mm)
# This point is 100 units along object's X, 50 along Y, 25 along Z

# 2. Load the pose matrix (object-to-camera transformation)
pose = np.loadtxt('pose.txt')  # 4×4 matrix

# 3. Transform to camera coordinates
point_camera = pose @ point_model  # Now in camera space (meters)

# Extract 3D position in camera frame
X, Y, Z = point_camera[:3]  # In meters, relative to camera

print(f"Model coordinates: {point_model[:3]} (object space)")
print(f"  → This point is relative to the object's origin")
print(f"Camera coordinates: ({X:.3f}, {Y:.3f}, {Z:.3f}) meters (camera space)")
print(f"  → This point is relative to the camera center")
print(f"  → X={X:.3f}m right, Y={Y:.3f}m down, Z={Z:.3f}m forward")

# 4. Now we can project to 2D using camera intrinsics K
K = np.loadtxt('K.txt')
u = (K[0,0] * X + K[0,2] * Z) / Z
v = (K[1,1] * Y + K[1,2] * Z) / Z
print(f"Image coordinates: ({u:.1f}, {v:.1f}) pixels")
```

### Visual Comparison

```
OBJECT SPACE (Model Coordinates):
    ┌─────────────────────┐
    │     3D Model        │
    │   (Object Space)    │
    │                     │
    │  Origin (0,0,0)     │ ← Object's local origin
    │      │              │
    │      │ Point A:     │
    │      │ (100,50,25)  │ ← Relative to object origin
    │      │              │
    └─────────────────────┘
           │
           │ [Pose Matrix: R, t]
           │ Transforms object → camera
           ↓
CAMERA SPACE (Camera Coordinates):
    ┌─────────────────────┐
    │      Camera        │
    │   (Camera Space)   │
    │                    │
    │  Origin (0,0,0)    │ ← Camera center
    │      │             │
    │      │ Point A:    │
    │      │ (0.282, -0.167, 0.732) │ ← Relative to camera
    │      │             │
    └────────────────────┘
           │
           │ [Camera Intrinsics K]
           │ Projects 3D → 2D
           ↓
IMAGE SPACE (2D Pixels):
    ┌─────────────────────┐
    │      Image         │
    │   (Image Space)    │
    │                    │
    │  Origin (0,0)      │ ← Top-left corner
    │      │             │
    │      │ Point A:    │
    │      │ (514, 150)  │ ← Pixel coordinates
    │      │             │
    └────────────────────┘
```

### Important Notes

1. **Model coordinates are fixed**: The same point in the model always has the same coordinates in object space, regardless of where the object is in the scene.

2. **Camera coordinates change**: As the object moves, the same model point will have different camera coordinates because the camera's perspective changes.

3. **The pose matrix encodes the relationship**: It tells us where the object is and how it's oriented relative to the camera at any given moment.

4. **Units matter**: Model coordinates use `unit_in_meter` (e.g., 0.001 for mm), while camera coordinates are always in meters. The pose matrix handles this conversion.

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

# Example 1: Transform the object origin from object to camera space
point_object = np.array([0, 0, 0, 1])  # Object origin in object space
point_camera = pose @ point_object  # = [tx, ty, tz, 1] in camera space
# The object origin in camera space is exactly the translation vector!

# Example 2: Transform an arbitrary model point
# Suppose we have a vertex at (100, 50, 25) in model coordinates
# (assuming unit_in_meter = 0.001, so this is 0.1m, 0.05m, 0.025m)
point_model = np.array([100, 50, 25, 1])  # In object space
point_camera = pose @ point_model  # Now in camera space (meters)
X, Y, Z = point_camera[:3]
print(f"Model point (100, 50, 25) in object space")
print(f"  → Camera space: ({X:.3f}, {Y:.3f}, {Z:.3f}) meters")

# Project to 2D image coordinates
X, Y, Z = point_camera[:3]
u = (K[0,0] * X + K[0,2] * Z) / Z  # fx * (X/Z) + cx
v = (K[1,1] * Y + K[1,2] * Z) / Z  # fy * (Y/Z) + cy

print(f"3D position in camera frame: ({X:.3f}, {Y:.3f}, {Z:.3f}) meters")
print(f"2D projection in image: ({u:.1f}, {v:.1f}) pixels")
```

This is exactly what happens internally when you call `model.pose_uv`!
