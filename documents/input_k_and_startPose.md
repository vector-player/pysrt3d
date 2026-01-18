# Understanding K-Matrix and Initial Pose Inputs

This document explains the two critical input data files required for pysrt3d tracking: the **K-matrix** (camera intrinsics) and the **initial pose** (starting 6DoF pose).

---

## 1. K-Matrix (Camera Intrinsics)

### What is the K-Matrix?

The **K-matrix** (also called the **camera intrinsics matrix** or **calibration matrix**) is a 3×3 matrix that describes the internal parameters of your camera. It defines how 3D points in camera space are projected onto the 2D image plane.

### File Format

**File name:** `K.txt` (or any filename you specify)

**Format:** 3×3 matrix, space or tab-separated values

```
fx   0   cx
0   fy   cy
0    0    1
```

### Matrix Elements Explained

```
[fx   0   cx]   ← fx: focal length in x-direction (pixels)
[0   fy   cy]   ← fy: focal length in y-direction (pixels)
[0    0    1]   ← cx, cy: principal point (image center) in pixels
```

**Parameters:**
- **`fx`**: Focal length in the x-direction (horizontal), in pixels
- **`fy`**: Focal length in the y-direction (vertical), in pixels
- **`cx`**: X-coordinate of the principal point (optical center), in pixels
- **`cy`**: Y-coordinate of the principal point (optical center), in pixels

**Note:** The bottom-left and top-right elements are always `0`, and the bottom-right element is always `1`.

### Example from Your Data

**File:** `example/data/K.txt`

```
481.34025  0.0        329.4003
0.0        481.8243   260.3788
0.000000   0.000000   1.000000
```

**Interpretation:**
- `fx = 481.34025` pixels (horizontal focal length)
- `fy = 481.8243` pixels (vertical focal length)
- `cx = 329.4003` pixels (principal point X, near image center)
- `cy = 260.3788` pixels (principal point Y, near image center)

This suggests the camera has approximately square pixels (fx ≈ fy) and the principal point is near the center of a ~640×480 image.

### How to Obtain the K-Matrix

#### Method 1: Camera Calibration (Recommended)

Use OpenCV's camera calibration tools:

```python
import cv2
import numpy as np

# Prepare calibration images (checkerboard pattern)
# ... capture multiple images of checkerboard ...

# Calibrate camera
ret, K, dist_coeffs, rvecs, tvecs = cv2.calibrateCamera(
    object_points, image_points, image_size, None, None
)

# Save K matrix
np.savetxt('K.txt', K, fmt='%.6f')
```

#### Method 2: Camera Specifications

If you know your camera's specifications:
- **Focal length** (in mm) → convert to pixels: `fx = (focal_length_mm / sensor_width_mm) * image_width_pixels`
- **Principal point**: Usually near image center: `cx ≈ image_width / 2`, `cy ≈ image_height / 2`

#### Method 3: From Camera Manufacturer

Many cameras provide calibration data or software tools to extract the K-matrix.

#### Method 4: Depth-Anything-3 (DA3) - Automatic Estimation

**Depth-Anything-3 (DA3)** can automatically estimate camera intrinsics from images. This is particularly useful when you don't have camera calibration data.

**Installation:**
```bash
pip install depth-anything-v3
```

**Usage:**
```python
from depth_anything_v3 import DepthAnythingV3
import numpy as np

# Initialize DA3
da3 = DepthAnythingV3()

# Process first frame to get camera intrinsics
result = da3.process_image(first_image)

# Extract camera intrinsics
fx = result['camera_intrinsics']['fx']
fy = result['camera_intrinsics']['fy']
cx = result['camera_intrinsics']['cx']
cy = result['camera_intrinsics']['cy']

# Construct K-matrix
K = np.array([
    [fx,  0, cx],
    [0,  fy, cy],
    [0,   0,  1]
], dtype=np.float32)

# Save to K.txt
np.savetxt('K.txt', K, fmt='%.6f')
```

**Advantages:**
- No physical calibration target needed
- Works with any camera
- Automatic estimation from images

**Limitations:**
- Accuracy depends on DA3 model variant
- May be less accurate for unusual lenses or wide-angle cameras
- Metric depth variants (e.g., `DA3Metric-Large`) may provide better intrinsics

**Note:** DA3 K-matrix estimation is well-supported and generally reliable. See Section 3 for more details on DA3 integration.

#### Method 5: Default/Estimated Values

For testing, you can use estimated values:
```python
# For a 640×480 image:
K = np.array([
    [640.0,   0.0,  320.0],  # fx = image width, cx = width/2
    [  0.0, 640.0,  240.0],  # fy = fx (square pixels), cy = height/2
    [  0.0,   0.0,    1.0]
])
```

**Warning:** Using estimated values may reduce tracking accuracy.

### Usage in pysrt3d

```python
import numpy as np
import pysrt3d

# Load K matrix
K = np.loadtxt('K.txt', dtype=np.float32)

# Create tracker with K matrix
tracker = pysrt3d.Tracker(
    imwidth=640,
    imheight=480,
    K=K  # 3×3 camera intrinsics matrix
)
```

### What Happens Without K-Matrix?

If you don't provide a K-matrix, pysrt3d will use default values:
- `fx = fy = max(image_width, image_height)` (estimated focal length)
- `cx = image_width / 2` (center X)
- `cy = image_height / 2` (center Y)

**This is not recommended** for accurate tracking.

---

## 2. Initial Pose (Starting 6DoF Pose)

### What is the Initial Pose?

The **initial pose** is a 4×4 homogeneous transformation matrix that represents the **starting position and orientation** of the 3D object in the camera's coordinate system. It is **required** for tracking initialization.

**Important:** pysrt3d is a **tracking-only** system. It does not perform global pose estimation. You must provide an accurate initial pose for the first frame.

### File Format

**File name:** `pose.txt` (or any filename you specify)

**Format:** 4×4 matrix, space or tab-separated values

```
R00  R01  R02  tx
R10  R11  R12  ty
R20  R21  R22  tz
0    0    0    1
```

### Matrix Structure Explained

The 4×4 pose matrix combines **rotation** and **translation**:

```
[R00  R01  R02  tx]   ← 3×3 Rotation Matrix (orientation)
[R10  R11  R12  ty]   ← 3×1 Translation Vector (position)
[R20  R21  R22  tz]
[0    0    0    1 ]   ← Homogeneous coordinates padding
```

**Components:**
- **Top-left 3×3 block**: Rotation matrix `R` describing the object's 3D orientation (roll, pitch, yaw)
- **Right column (top 3)**: Translation vector `[tx, ty, tz]` describing the object's 3D position in **meters**
- **Bottom row**: Always `[0, 0, 0, 1]` for homogeneous coordinates

### Example from Your Data

**File:** `example/data/pose.txt`

```
0.78603    -0.587438   0.19255    0.281848
0.604647    0.795404  -0.0416517 -0.166599
-0.128687   0.149164   0.980401   0.731918
0           0          0          1
```

**Interpretation:**
- **Translation**: The object is located at `(0.282, -0.167, 0.732)` meters from the camera
  - `tx = 0.282 m` (0.282 meters to the right)
  - `ty = -0.167 m` (0.167 meters up)
  - `tz = 0.732 m` (0.732 meters forward, into the scene)
- **Rotation**: The 3×3 rotation matrix describes how the object is oriented in 3D space

### Coordinate System

The pose uses **OpenCV camera coordinates**:
- **Origin**: Camera center
- **X-axis**: Right (positive X = right)
- **Y-axis**: Down (positive Y = down)
- **Z-axis**: Forward (positive Z = into the scene, away from camera)
- **Units**: Meters

### How to Obtain the Initial Pose

#### Method 1: Manual Annotation (For Testing)

For the first frame, manually estimate:
1. **Position**: Roughly estimate where the object center is relative to the camera
2. **Orientation**: Estimate the object's rotation (can start with identity matrix for front-facing)

```python
import numpy as np

# Example: Object at (0.3, 0.0, 0.5) meters, front-facing
pose = np.eye(4)  # Identity matrix (no rotation)
pose[0, 3] = 0.3  # tx = 0.3 m
pose[1, 3] = 0.0  # ty = 0.0 m
pose[2, 3] = 0.5  # tz = 0.5 m

np.savetxt('pose.txt', pose, fmt='%.6f')
```

#### Method 2: Pose Estimation from First Frame

Use a pose estimation method (e.g., PnP, template matching) on the first frame:

```python
import cv2
import numpy as np

# Load first image and 3D model
image = cv2.imread('frame_0000.png')
model_points = ...  # 3D model points
image_points = ...  # Corresponding 2D points in image

# Solve PnP to get pose
ret, rvec, tvec = cv2.solvePnP(
    model_points, image_points, K, dist_coeffs
)

# Convert to 4×4 matrix
R, _ = cv2.Rodrigues(rvec)
pose = np.eye(4)
pose[:3, :3] = R
pose[:3, 3] = tvec.flatten()

np.savetxt('pose.txt', pose, fmt='%.6f')
```

#### Method 3: From Previous Tracking Session

If you have a previous tracking result, use the pose from the last frame as the initial pose for a new sequence.

#### Method 4: Depth-Anything-3 (DA3) - With Object Detection

**Depth-Anything-3 (DA3)** can estimate camera pose and depth, which can be combined with object detection to estimate initial pose. However, this requires additional steps and conversions.

**Important Considerations:**
- DA3 estimates **camera pose** (camera-to-world), but pysrt3d needs **object pose** (object-to-camera)
- DA3 may use different coordinate conventions than OpenCV
- DA3 depth may be up-to-scale; pysrt3d needs metric scale (meters)
- Requires object detection to locate the object in the first frame

**Workflow:**
```python
from depth_anything_v3 import DepthAnythingV3
import numpy as np
import cv2

# 1. Initialize DA3
da3 = DepthAnythingV3()

# 2. Process first frame
result = da3.process_image(first_frame)
depth_map = result['depth']  # Depth map

# 3. Detect object in first frame (using your detection method)
bbox = detect_object_bbox(first_frame)  # e.g., YOLO, manual annotation
bbox_center = [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2]

# 4. Extract depth at object center
depth_at_object = depth_map[int(bbox_center[1]), int(bbox_center[0]]

# 5. Convert 2D + depth to 3D position (using K-matrix)
K = np.loadtxt('K.txt')  # Load K-matrix (can also use DA3-estimated K)
u, v = bbox_center
Z = depth_at_object  # Depth in meters (may need scale calibration)
X = (u - K[0, 2]) * Z / K[0, 0]
Y = (v - K[1, 2]) * Z / K[1, 1]
object_3d_pos = np.array([X, Y, Z])

# 6. Estimate orientation (simplified - front-facing)
# For more accurate orientation, use PnP with 3D model points
R = np.eye(3)  # Identity rotation (front-facing)

# 7. Construct pose matrix (object-to-camera)
pose = np.eye(4)
pose[:3, :3] = R
pose[:3, 3] = object_3d_pos

# 8. Save to pose.txt
np.savetxt('pose.txt', pose, fmt='%.6f')
```

**Limitations:**
- Requires object detection step
- Depth scale may need calibration
- Orientation estimation is simplified (may need refinement)
- Coordinate system conversion may be needed

**Recommendation:** Use DA3 primarily for K-matrix estimation. For initial pose, consider combining DA3 depth with more robust pose estimation methods (e.g., PnP with 3D model points). See Section 3 for complete DA3 integration details.

#### Method 5: From Ground Truth Data

If you have ground truth poses (e.g., from motion capture, simulation, or manual annotation), use the first frame's pose.

### Usage in pysrt3d

```python
import numpy as np
import pysrt3d

# Load initial pose
init_pose = np.loadtxt('pose.txt', dtype=np.float32)

# Set initial pose for the model
model.reset_pose(init_pose)

# Now tracking can begin
for image in images:
    tracker.update(image=image_rgb)
    current_pose = model.pose  # Updated pose after tracking
```

### Why is Initial Pose Required?

1. **Tracking, not detection**: pysrt3d tracks the object frame-by-frame, assuming it's already visible and roughly known
2. **Optimization starting point**: The tracker optimizes the pose starting from the initial pose
3. **Correspondence matching**: The initial pose helps establish correspondences between the 3D model and 2D image features

### What Happens with Wrong Initial Pose?

- **Tracking may fail**: If the initial pose is too far from the actual pose, tracking may not converge
- **Low confidence**: The tracker's confidence (`model.conf`) will be low
- **Drift**: Tracking may drift or lose the object
- **No recovery**: The system cannot recover from a completely wrong initial pose

**Recommendation:** Ensure the initial pose is accurate to within a few centimeters and ~10 degrees of rotation.

---

## Relationship Between K-Matrix and Initial Pose

### How They Work Together

1. **K-matrix** projects 3D points (in camera coordinates) to 2D image pixels
2. **Initial pose** transforms 3D model points (in object coordinates) to camera coordinates
3. Together, they enable the tracker to:
   - Render the 3D model onto the 2D image
   - Compare the rendered view with the actual image
   - Optimize the pose to minimize the difference

### Transformation Pipeline

```
3D Model Points (Object Space)
    ↓ [Initial Pose: 4×4 matrix]
3D Camera Coordinates (X, Y, Z in meters)
    ↓ [K-Matrix: 3×3 projection]
2D Image Coordinates (u, v in pixels)
```

### Mathematical Relationship

For a 3D point `P_object = [x, y, z, 1]` in object coordinates:

```python
# Step 1: Transform to camera coordinates
P_camera = pose @ P_object  # 4×4 @ 4×1 = 4×1
X, Y, Z = P_camera[:3]      # Extract 3D position

# Step 2: Project to 2D image
u = (K[0,0] * X + K[0,2] * Z) / Z  # fx * (X/Z) + cx
v = (K[1,1] * Y + K[1,2] * Z) / Z  # fy * (Y/Z) + cy
```

This is exactly what `model.pose_uv` returns - the 2D projection of the object center!

---

## File Format Summary

### K.txt Format

```
fx   0   cx
0   fy   cy
0    0    1
```

**Requirements:**
- 3×3 matrix
- Space or tab-separated
- Bottom-left and top-right must be `0`
- Bottom-right must be `1`

### pose.txt Format

```
R00  R01  R02  tx
R10  R11  R12  ty
R20  R21  R22  tz
0    0    0    1
```

**Requirements:**
- 4×4 matrix
- Space or tab-separated
- Bottom row must be `[0, 0, 0, 1]`
- Top-left 3×3 must be a valid rotation matrix (orthogonal, determinant = 1)

---

## Loading in Python

### Loading K-Matrix

```python
import numpy as np

# Method 1: Using np.loadtxt (recommended)
K = np.loadtxt('K.txt', dtype=np.float32)

# Verify shape
assert K.shape == (3, 3), f"Expected 3×3, got {K.shape}"

# Verify structure
assert K[0, 1] == 0 and K[1, 0] == 0, "Off-diagonal elements must be 0"
assert K[2, 0] == 0 and K[2, 1] == 0 and K[2, 2] == 1, "Bottom row must be [0, 0, 1]"
```

### Loading Initial Pose

```python
import numpy as np

# Method 1: Using np.loadtxt (recommended)
pose = np.loadtxt('pose.txt', dtype=np.float32)

# Verify shape
assert pose.shape == (4, 4), f"Expected 4×4, got {pose.shape}"

# Verify structure
assert np.allclose(pose[3, :], [0, 0, 0, 1]), "Bottom row must be [0, 0, 0, 1]"

# Verify rotation matrix (optional but recommended)
R = pose[:3, :3]
assert np.allclose(R @ R.T, np.eye(3)), "Rotation matrix must be orthogonal"
assert np.isclose(np.linalg.det(R), 1.0), "Rotation matrix determinant must be 1"
```

---

## Common Issues and Solutions

### Issue 1: "K matrix shape mismatch"

**Problem:** K matrix is not 3×3

**Solution:** Check your K.txt file has exactly 3 rows and 3 columns

### Issue 2: "Pose matrix shape mismatch"

**Problem:** Pose matrix is not 4×4

**Solution:** Check your pose.txt file has exactly 4 rows and 4 columns

### Issue 3: Tracking fails immediately

**Possible causes:**
- Initial pose is too far from actual pose
- K-matrix is incorrect (wrong camera calibration)
- Model scale (`unit_in_meter`) doesn't match the pose units

**Solutions:**
- Verify initial pose accuracy
- Recalibrate camera to get correct K-matrix
- Check that pose translation is in meters and matches model scale

### Issue 4: Object appears in wrong location

**Possible causes:**
- Wrong coordinate system (OpenCV vs OpenGL)
- Incorrect K-matrix (principal point wrong)
- Initial pose translation is wrong

**Solutions:**
- Ensure pose uses OpenCV coordinates (Y-down, Z-forward)
- Verify K-matrix principal point (cx, cy) matches image center
- Check initial pose translation units (should be meters)

---

## Example: Complete Setup

```python
import numpy as np
import cv2
import pysrt3d
from pathlib import Path

# 1. Load K-matrix
K = np.loadtxt('K.txt', dtype=np.float32)
print(f"K-matrix:\n{K}\n")

# 2. Load initial pose
init_pose = np.loadtxt('pose.txt', dtype=np.float32)
print(f"Initial pose:\n{init_pose}\n")

# 3. Extract camera parameters
fx, fy = K[0, 0], K[1, 1]
cx, cy = K[0, 2], K[1, 2]
print(f"Camera: fx={fx:.1f}, fy={fy:.1f}, cx={cx:.1f}, cy={cy:.1f}\n")

# 4. Extract pose translation
tx, ty, tz = init_pose[0, 3], init_pose[1, 3], init_pose[2, 3]
print(f"Object position: ({tx:.3f}, {ty:.3f}, {tz:.3f}) meters\n")

# 5. Project object center to 2D
X, Y, Z = tx, ty, tz
u = (fx * X + cx * Z) / Z
v = (fy * Y + cy * Z) / Z
print(f"Object center in image: ({u:.1f}, {v:.1f}) pixels\n")

# 6. Setup tracker
image = cv2.imread('frame_0000.png')
h, w = image.shape[:2]

tracker = pysrt3d.Tracker(
    imwidth=w,
    imheight=h,
    K=K
)

model = pysrt3d.Model(
    name="Object",
    model_path="model.obj",
    meta_path="model.meta",
    unit_in_meter=0.001
)

tracker.add_model(model)
tracker.setup()

# 7. Set initial pose
model.reset_pose(init_pose)

# 8. Verify projection matches
print(f"Model pose_uv: {model.pose_uv}")
print(f"Calculated uv: ({u:.1f}, {v:.1f})")
```

---

## 3. Using Depth-Anything-3 (DA3) for Automatic Generation

### Overview

**Depth-Anything-3 (DA3)** is a state-of-the-art monocular depth estimation model that can automatically estimate camera intrinsics and, with additional processing, help estimate initial pose. This section provides a comprehensive guide to using DA3 with pysrt3d.

### DA3 Capabilities Summary

| Component | DA3 Support | Usability | Notes |
|-----------|-------------|-----------|-------|
| **K-Matrix** | ✅ Yes | High | Direct extraction, good accuracy |
| **Initial Pose** | ⚠️ Partial | Medium | Requires object detection + conversion |

### 3.1 Using DA3 for K-Matrix

#### Installation

```bash
pip install depth-anything-v3
```

#### Basic Usage

```python
from depth_anything_v3 import DepthAnythingV3
import numpy as np
import cv2

# Initialize DA3
da3 = DepthAnythingV3()

# Load first frame
first_frame = cv2.imread('frame_0000.png')
first_frame_rgb = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)

# Process image to get camera intrinsics
result = da3.process_image(first_frame_rgb)

# Extract camera intrinsics
fx = result['camera_intrinsics']['fx']
fy = result['camera_intrinsics']['fy']
cx = result['camera_intrinsics']['cx']
cy = result['camera_intrinsics']['cy']

# Construct K-matrix
K = np.array([
    [fx,  0, cx],
    [0,  fy, cy],
    [0,   0,  1]
], dtype=np.float32)

# Save to K.txt
np.savetxt('K.txt', K, fmt='%.6f')
print(f"DA3-estimated K-matrix:\n{K}")
```

#### Advantages

- **No calibration target needed**: Works directly from images
- **Automatic**: No manual measurement required
- **Works with unknown cameras**: Useful when camera specs are unavailable
- **Good accuracy**: Generally reliable for standard cameras

#### Limitations

- **Model-dependent accuracy**: Accuracy varies with DA3 model variant
- **Lens limitations**: May be less accurate for unusual lenses or wide-angle cameras
- **Validation recommended**: Compare with known calibration if available

#### Model Variants

DA3 offers different model variants:
- **Standard variants**: Good for general use
- **Metric variants** (e.g., `DA3Metric-Large`): May provide better intrinsics for metric-scale applications

### 3.2 Using DA3 for Initial Pose

#### Overview

DA3 can estimate camera pose and depth, but converting this to object pose requires additional steps:

1. **Object detection**: Locate the object in the first frame
2. **Depth extraction**: Get depth at object location
3. **3D position calculation**: Convert 2D + depth to 3D position
4. **Orientation estimation**: Estimate object orientation
5. **Coordinate conversion**: Convert to OpenCV coordinates if needed

#### Complete Workflow

```python
from depth_anything_v3 import DepthAnythingV3
import numpy as np
import cv2

# 1. Initialize DA3
da3 = DepthAnythingV3()

# 2. Load first frame
first_frame = cv2.imread('frame_0000.png')
first_frame_rgb = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)

# 3. Process image with DA3
result = da3.process_image(first_frame_rgb)
depth_map = result['depth']  # Depth map

# 4. Get K-matrix (from DA3 or from file)
K = np.array([
    [result['camera_intrinsics']['fx'], 0, result['camera_intrinsics']['cx']],
    [0, result['camera_intrinsics']['fy'], result['camera_intrinsics']['cy']],
    [0, 0, 1]
], dtype=np.float32)

# 5. Detect object in first frame
# Option A: Manual annotation
bbox = [x1, y1, x2, y2]  # Bounding box coordinates

# Option B: Use object detection model (e.g., YOLO)
# bbox = detect_object_yolo(first_frame)

# Option C: Use segmentation
# mask = detect_object_segmentation(first_frame)

# 6. Extract object center and depth
bbox_center_u = (bbox[0] + bbox[2]) / 2
bbox_center_v = (bbox[1] + bbox[3]) / 2

# Get depth at object center (may need interpolation)
depth_at_object = depth_map[int(bbox_center_v), int(bbox_center_u)]

# Note: DA3 depth may be in relative scale - may need calibration
# For metric depth, use DA3Metric variants or calibrate scale

# 7. Convert 2D + depth to 3D position (in camera coordinates)
u, v = bbox_center_u, bbox_center_v
Z = depth_at_object  # Depth in meters (verify scale!)
X = (u - K[0, 2]) * Z / K[0, 0]
Y = (v - K[1, 2]) * Z / K[1, 1]
object_3d_pos = np.array([X, Y, Z])

# 8. Estimate orientation
# Option A: Simple front-facing (identity rotation)
R = np.eye(3)

# Option B: Use PnP with 3D model points (more accurate)
# model_points_3d = ...  # 3D points from your .obj file
# image_points_2d = ...  # Corresponding 2D points from detection
# ret, rvec, tvec = cv2.solvePnP(model_points_3d, image_points_2d, K, None)
# R, _ = cv2.Rodrigues(rvec)

# 9. Construct pose matrix (object-to-camera, OpenCV convention)
pose = np.eye(4, dtype=np.float32)
pose[:3, :3] = R
pose[:3, 3] = object_3d_pos

# 10. Save to pose.txt
np.savetxt('pose.txt', pose, fmt='%.6f')
print(f"DA3-estimated initial pose:\n{pose}")
```

#### Important Considerations

**1. Coordinate System:**
- DA3 may use different coordinate conventions than OpenCV
- pysrt3d expects OpenCV: X-right, Y-down, Z-forward
- Verify and convert if needed

**2. Scale:**
- DA3 depth may be up-to-scale or normalized
- pysrt3d needs metric scale (meters)
- Use DA3Metric variants or calibrate scale using known object dimensions

**3. Frame of Reference:**
- DA3 estimates **camera pose** (camera-to-world)
- pysrt3d needs **object pose** (object-to-camera)
- Requires object detection and alignment

**4. Accuracy:**
- Initial pose accuracy affects tracking performance
- Consider manual refinement for critical applications
- Validate with known ground truth if available

### 3.3 Recommended Integration Approach

#### Hybrid Solution

1. **Use DA3 for K-matrix** (most reliable)
   - Direct extraction from DA3 output
   - Good accuracy for standard cameras
   - No additional processing needed

2. **Use DA3 depth + object detection for initial pose**
   - Get depth map from DA3
   - Detect object in first frame
   - Extract 3D position from depth
   - Estimate orientation (PnP recommended)

3. **Manual refinement** (if needed)
   - Adjust pose if tracking fails
   - Use interactive tools for fine-tuning

#### Complete Integration Example

```python
from depth_anything_v3 import DepthAnythingV3
import numpy as np
import cv2
import pysrt3d

# Step 1: Initialize DA3
da3 = DepthAnythingV3()

# Step 2: Load first frame
first_frame = cv2.imread('frame_0000.png')
first_frame_rgb = cv2.cvtColor(first_frame, cv2.COLOR_BGR2RGB)
h, w = first_frame.shape[:2]

# Step 3: Get K-matrix from DA3
result = da3.process_image(first_frame_rgb)
K = np.array([
    [result['camera_intrinsics']['fx'], 0, result['camera_intrinsics']['cx']],
    [0, result['camera_intrinsics']['fy'], result['camera_intrinsics']['cy']],
    [0, 0, 1]
], dtype=np.float32)

# Step 4: Get depth map
depth_map = result['depth']

# Step 5: Detect object (simplified - replace with your detection method)
bbox = detect_object(first_frame)  # Your detection function
bbox_center = [(bbox[0] + bbox[2])/2, (bbox[1] + bbox[3])/2]

# Step 6: Extract 3D position from depth
u, v = bbox_center
Z = depth_map[int(v), int(u)]  # May need scale calibration
X = (u - K[0, 2]) * Z / K[0, 0]
Y = (v - K[1, 2]) * Z / K[1, 1]

# Step 7: Estimate initial pose (simplified)
init_pose = np.eye(4, dtype=np.float32)
init_pose[:3, 3] = [X, Y, Z]  # Translation
# Rotation can be identity or estimated via PnP

# Step 8: Setup pysrt3d with DA3-generated inputs
tracker = pysrt3d.Tracker(imwidth=w, imheight=h, K=K)
model = pysrt3d.Model(
    name="Object",
    model_path="model.obj",
    meta_path="model.meta",
    unit_in_meter=0.001
)
tracker.add_model(model)
tracker.setup()
model.reset_pose(init_pose)

# Step 9: Start tracking
for image_path in image_sequence:
    image = cv2.imread(image_path)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    tracker.update(image=image_rgb)
    current_pose = model.pose
    print(f"Pose: {current_pose}")
```

### 3.4 Limitations and Troubleshooting

#### Common Issues

**Issue 1: DA3 K-matrix accuracy**
- **Symptom**: Tracking drifts or fails
- **Solution**: Validate K-matrix with known calibration, or use camera calibration instead

**Issue 2: Depth scale mismatch**
- **Symptom**: Object appears at wrong distance
- **Solution**: Calibrate depth scale using known object dimensions, or use DA3Metric variants

**Issue 3: Coordinate system mismatch**
- **Symptom**: Object orientation is wrong
- **Solution**: Verify coordinate conventions and convert if needed

**Issue 4: Object detection required**
- **Symptom**: Need to locate object in first frame
- **Solution**: Use object detection model (YOLO, etc.) or manual annotation

#### Best Practices

1. **Validate DA3 outputs**: Compare with known ground truth when possible
2. **Use metric variants**: For metric-scale applications, prefer DA3Metric variants
3. **Refine initial pose**: Manually adjust if tracking fails
4. **Combine methods**: Use DA3 for K-matrix, traditional methods for initial pose if needed

### 3.5 References

- **Depth-Anything-3**: https://github.com/vector-player/Depth-Anything-3
- **DA3 Documentation**: See DA3 repository for detailed API documentation
- **Related Documents**:
  - `documents/cursor_pysrt3d_integrate_da3.md`: Complete DA3 integration guide

---

## References

- **Camera Calibration**: OpenCV Camera Calibration Tutorial
- **Pose Estimation**: PnP (Perspective-n-Point) algorithm
- **Coordinate Systems**: OpenCV camera coordinate convention
- **Depth-Anything-3**: https://github.com/vector-player/Depth-Anything-3
- **Related Documents**:
  - `documents/output_pose_matrix.md`: Understanding output poses
  - `documents/input_3d_model.md`: Understanding 3D model input
  - `documents/cursor_pysrt3d_integrate_da3.md`: Complete DA3 integration guide

---

**Last Updated:** Based on pysrt3d codebase analysis and Depth-Anything-3 integration
