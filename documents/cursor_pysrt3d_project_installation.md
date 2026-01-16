# Pysrt3d project installation
_Exported on 1/15/2026 at 22:54:36 GMT+8 from Cursor (2.3.34)_

---

**User**

read https://github.com/Jianxff/pysrt3d start to install this project. remember to create conda env called "pysrt3d"

---

**Cursor**

Checking the current directory, then cloning the repository and setting up the conda environment.


Repository already exists. Checking its contents, then creating the conda environment and installing dependencies.


Creating the conda environment "pysrt3d" and installing dependencies:


Installing conda dependencies in the environment:


Installing pip dependencies and building the package:


Installing the pysrt3d package:


Installing cmake via conda to ensure the binary is available:


Checking the source directory structure, then retrying the installation:


Checking CMakeLists.txt for OpenGL requirements, then installing the necessary OpenGL development libraries:


Installing system OpenGL development libraries:


Retrying the package installation:


Verifying the installation by importing the module:


Installation complete. Summary:

## Installation Summary

1. **Created conda environment** named `pysrt3d` with Python 3.9

2. **Installed conda dependencies:**
   - `glew` - OpenGL Extension Wrangler Library
   - `glfw` - OpenGL Framework
   - `eigen` - C++ template library for linear algebra
   - `libopencv` - OpenCV library
   - `cmake` - Build system
   - `numpy` and `opencv` (Python packages) were automatically installed

3. **Installed pip dependencies:**
   - `opencv-python` - Python bindings for OpenCV
   - `cmake` (Python package)
   - `pybind11` - Python-C++ binding library

4. **Installed system dependencies:**
   - `libgl1-mesa-dev` and `libglu1-mesa-dev` - OpenGL development libraries

5. **Built and installed the package** using `pip install .`

6. **Verified installation** - The `pysrt3d` module can be imported successfully

The project is installed and ready to use. Activate the environment with:
```bash
conda activate pysrt3d
```

You can now run the demo as mentioned in the README:
```bash
cd /root/pysrt3d/example
python demo.py
```

```shellscript
conda activate pysrt3d
```

```shellscript
cd /root/pysrt3d/example
python demo.py
```

---

**User**

@bash (10-111) explain this error

---

**Cursor**

Analyzing the error. Checking the demo script and the example directory structure:


The errors stem from two issues:

1) Missing model metadata file
```
Could not open model file "/root/pysrt3d/example/data/Cat.meta"
```
The `Cat.meta` file is missing from the data directory.

2) GLFW initialization failure (headless environment)
```
error: XDG_RUNTIME_DIR is invalid or not set in the environment.
Failed to initialize GLFW: Failed to detect any supported platform
```
GLFW requires a display server (X11 or Wayland), but this appears to be a headless environment (Docker/remote server). This causes:
- Renderer geometry setup to fail
- Tracker setup to fail
- RuntimeError: "Set up tracker tracker first"

Checking if we can work around the headless issue or if the meta file can be generated:


```plaintext
Could not open model file "/root/pysrt3d/example/data/Cat.meta"
```

```plaintext
error: XDG_RUNTIME_DIR is invalid or not set in the environment.
Failed to initialize GLFW: Failed to detect any supported platform
```

Checking the source code to understand the meta file format:


## Error explanation

### Root cause: headless environment (GLFW failure)

The main issue is that GLFW cannot initialize because there's no display server. This is a headless environment (Docker/remote server without X11/Wayland).

Error chain:
1. GLFW initialization fails → no OpenGL context
2. Renderer geometry setup fails → depends on OpenGL
3. Tracker setup fails → depends on renderer
4. RuntimeError: "Set up tracker tracker first" → tracker never initialized

### Secondary issue: missing Cat.meta file

The code expects `Cat.meta` but it's missing. The code can auto-generate it (line 58 in pysrt3d.cpp), but it still needs to be created.

### Solutions

**Option 1: Use a virtual display (Xvfb) for headless environments**
```bash
# Install Xvfb
sudo apt-get install -y xvfb

# Run with virtual display
xvfb-run -a python /root/pysrt3d/example/demo.py
```

**Option 2: Set XDG_RUNTIME_DIR (may help with Wayland)**
```bash
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR
```

**Option 3: Use offscreen rendering**
The library may need to be configured for headless/offscreen rendering, which may require code changes.

Should I set up Xvfb and test the demo, or investigate the meta file generation?

```shellscript
# Install Xvfb
sudo apt-get install -y xvfb

# Run with virtual display
xvfb-run -a python /root/pysrt3d/example/demo.py
```

```shellscript
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR
```

---

**User**

try option 1

---

**Cursor**

Installing Xvfb and running the demo with a virtual display:


Setting up XDG_RUNTIME_DIR and running the demo with Xvfb:


Two issues: missing `Cat.meta` and an LLVM error. Checking the meta file format and creating it if needed:


Checking how the meta file is used in the source code:


The meta file is a binary cache of precomputed template views. It should be auto-generated, but that requires OpenGL. The LLVM error suggests a library conflict. Trying a different approach with better Xvfb settings and environment variables:


The LLVM error persists, likely a library conflict. Checking LLVM libraries in the conda environment:


Trying to work around the LLVM conflict by setting library paths and environment variables:


Checking which library is loading LLVM and whether we can work around it:


The error occurs during GLFW/OpenGL initialization, not during import. Installing OSMesa for offscreen rendering:


Trying software rendering to avoid the LLVM conflict:


The LLVM conflict persists. Trying EGL instead of GLX, which may avoid the LLVM path:


Creating a wrapper script to isolate the LLVM libraries:


```shellscript
#!/bin/bash
# Wrapper script to run pysrt3d demo in headless environment
# Attempts to work around LLVM library conflicts

export DISPLAY=:99
export XDG_RUNTIME_DIR=/tmp/runtime-root
mkdir -p $XDG_RUNTIME_DIR
chmod 700 $XDG_RUNTIME_DIR

# Try to avoid LLVM conflicts by not preloading conda's LLVM
# Use system Mesa/OpenGL libraries if available
export LIBGL_ALWAYS_SOFTWARE=1

# Try to suppress LLVM debug option registration
export LLVM_COMMAND_LINE_OPTIONS=0 2>/dev/null || true

# Run with Xvfb
xvfb-run --server-args="-screen 0 1920x1080x24 -ac +extension GLX +render -noreset" \
    python "$(dirname "$0")/example/demo.py" "$@"

```

The LLVM conflict persists. This is a known issue when multiple LLVM libraries load. Summary and a potential workaround:

## Summary of the Issue

The LLVM error (`CommandLine Error: Option 'use-dbg-addr' registered more than once!`) occurs because:
1. Conda installed `libllvm15` as a dependency
2. When GLFW/OpenGL initializes, Mesa's software renderer also tries to load LLVM
3. Both register the same command-line options, causing a conflict

## Potential Solutions

**Option A: Try removing conda's LLVM** (risky - might break other things):
```bash
conda activate pysrt3d
conda remove libllvm15 --force
```

**Option B: Use a system with a real display** (not headless)

**Option C: Rebuild pysrt3d** with system libraries instead of conda's LLVM

**Option D: Check if there's a way to disable LLVM in Mesa**

Should I try Option A (removing conda's LLVM), or would you prefer a different approach? The library conflict is preventing GLFW from initializing, which blocks the demo from running in this headless setup.

```shellscript
conda activate pysrt3d
conda remove libllvm15 --force
```

---

**User**

how many size of pysrt3d/ now?

---

**Cursor**

Checking the size of the pysrt3d directory:


The `/root/pysrt3d` directory is **52 MB** total.

Breakdown:
- **example/**: 20 MB (largest — likely demo data/images)
- **build/**: 12 MB (compiled build artifacts)
- **source/**: 1.5 MB (source code)
- **pysrt3d.egg-info/**: 27 KB (package metadata)
- Other files (LICENSE, readme.md, setup.py, run_demo_headless.sh): ~4.5 KB each

Most of the size is from the example data and build artifacts. The source code is about 1.5 MB.

---

**User**

Are all dataset, models and weights installed already for pysrt3d?

---

**Cursor**

Checking what's included in the pysrt3d installation, especially datasets, models, and weights:


Checking what's included and what might be missing:


## What's included

1. Demo dataset: 31 PNG images (0000.png–0030.png) in `example/data/images/`
2. 3D model: `Cat.obj` (164 KB)
3. Camera calibration: `K.txt` (camera intrinsic matrix)
4. Initial pose: `pose.txt` (4x4 transformation matrix)

## What's missing

1. `Cat.meta`: Binary cache file that should be auto-generated on first run. It contains precomputed template views for tracking. It's missing because the model setup failed due to the GLFW/OpenGL initialization issue.

## Important note

pysrt3d is a geometric/sparse region-based tracker, not a deep learning model. It does not use neural network weights. It uses:
- 3D geometry (the .obj file)
- Sparse region-based tracking
- Template views generated from the 3D model

The `Cat.meta` file is generated by the `Model.SetUp()` method when it first runs successfully. It requires OpenGL/GLFW to render the 3D model and generate template views, which is why it's missing — the setup failed due to the headless environment issue we encountered.

Summary: Demo data and the 3D model are included. The `Cat.meta` cache file will be generated automatically once the OpenGL/GLFW initialization issue is resolved.

---

**User**

Why is the Cat.obj model so small (164KB)? It looks inormal

---

**Cursor**

Inspecting the Cat.obj file to verify it's a complete 3D model:


Checking the model structure in more detail:


The Cat.obj file is normal for a low-poly tracking model.

## Model Statistics:
- **2,502 vertices**
- **5,000 faces** (triangles)
- **164 KB file size**
- Generated by Meshlab
- No texture coordinates or normals (computed on the fly)

## Why 164KB is normal:

1. **Low-poly model**: For object tracking, a simplified mesh is preferred:
   - Faster processing
   - Sparse region-based tracking doesn't need fine detail
   - Geometric features are sufficient

2. **Size calculation**:
   - ~2,502 vertices × ~25 bytes = ~62 KB
   - ~5,000 faces × ~20 bytes = ~100 KB
   - Plus comments/formatting = ~164 KB total

3. **Comparison**:
   - High-poly models: 100K–1M+ vertices, often 10–100+ MB
   - This model: 2.5K vertices, 164 KB — appropriate for tracking

## This is expected for tracking:
The SRT3D algorithm uses sparse region-based tracking, which relies on geometric features and contours rather than fine mesh detail. A low-poly model is standard and sufficient.

The file is complete and valid. The size is appropriate for a tracking demo model.

---

**User**

Investigate and explain what is the output for running this pysrt3d

---

**Cursor**

Investigating what pysrt3d outputs. Examining the demo code and source to understand the output:


Checking what the tracker and renderer produce:


Checking what the confidence score represents:


Creating a summary document explaining the outputs:


```markdown
# pysrt3d Output Explanation

## Overview
pysrt3d performs **6DoF (6 Degrees of Freedom) object tracking** - it tracks the 3D position and orientation of objects in video sequences. The output consists of several components:

---

## Main Outputs

### 1. **Pose Information** (6DoF Tracking Result)

#### `model.pose` - 4×4 Transformation Matrix (OpenCV coordinate)
- **Type**: `numpy.ndarray`, shape `(4, 4)`, dtype `float32`
- **Description**: The 6DoF pose of the tracked object in the camera coordinate system
- **Format**: 
  ```
  [R11 R12 R13 tx]
  [R21 R22 R23 ty]
  [R31 R32 R33 tz]
  [  0   0   0  1]
  ```
  Where:
  - `R` = 3×3 rotation matrix (orientation)
  - `[tx, ty, tz]` = translation vector (position)
- **Coordinate System**: OpenCV convention (Z forward, Y down, X right)

#### `model.pose_gl` - 4×4 Transformation Matrix (OpenGL coordinate)
- **Type**: `numpy.ndarray`, shape `(4, 4)`, dtype `float32`
- **Description**: Same pose but in OpenGL coordinate system
- **Coordinate System**: OpenGL convention (Z backward, Y up, X right)

#### `model.pose_uv` - 2D Projection Point
- **Type**: `tuple` of `(x, y)` integers
- **Description**: The 2D pixel coordinates where the object center projects onto the image
- **Usage**: Used for overlaying text/annotations on the image
- **Calculation**: Projects the 3D translation `[tx, ty, tz]` using camera intrinsics `K`

---

### 2. **Confidence Score**

#### `model.conf` - Tracking Confidence
- **Type**: `float`, range `[0.0, 1.0]`
- **Description**: Confidence that the current pose estimate is accurate
- **Calculation Method**: 
  - Uses **Kullback-Leibler (KL) divergence** between observed correspondence lines and optimal distribution
  - For each correspondence line, computes KL divergence: `KL(observed || N(0, σ²_min))`
  - If KL < `kl_threshold` (default 1.0), the line is considered "valid"
  - Confidence = `valid_lines / total_lines`
- **Interpretation**:
  - `1.0` = Perfect tracking (all correspondence lines match expected distribution)
  - `0.5` = Half of correspondence lines are valid
  - `0.0` = Poor/no tracking (no valid correspondences)
- **Usage**: 
  - Used to determine if tracking is successful
  - Can trigger re-initialization if confidence drops too low

---

### 3. **Rendered Visualization Image**

#### `renderer.render()` - Normal View Image
- **Type**: `numpy.ndarray`, shape `(height, width, 3)`, dtype `uint8`
- **Description**: Visualization image showing:
  - **Original camera image** (background)
  - **Rendered 3D model** overlaid with alpha blending (opacity ~0.5)
  - The rendered model shows the predicted pose of the object
- **Visualization**:
  - Shows how well the 3D model aligns with the actual object in the image
  - Green text overlay showing model name and confidence score
- **Format**: RGB image (can be displayed with OpenCV or saved)

---

### 4. **Additional Metrics**

#### `model.valid_line_prop` - Valid Line Proportion
- **Type**: `float`, range `[0.0, 1.0]`
- **Description**: Proportion of valid correspondence lines
- **Calculation**: `valid_data_lines / total_n_lines`
- **Usage**: Additional metric for tracking quality assessment

#### `model.name` - Model Name
- **Type**: `str`
- **Description**: Name identifier for the tracked model (e.g., "Cat")

---

## Workflow and Output Flow

### Per-Frame Processing:

```
1. Input: RGB image (numpy array)
   ↓
2. tracker.update(image=image_rgb)
   - Performs sparse region-based tracking
   - Updates pose estimate iteratively
   - Calculates correspondence lines
   ↓
3. Output Updates:
   - model.pose → Updated 6DoF pose
   - model.conf → Updated confidence score
   - model.pose_uv → Updated 2D projection
   ↓
4. renderer.render()
   - Renders 3D model at current pose
   - Blends with camera image
   ↓
5. Output: Visualization image with tracking overlay
```

---

## Example Output Values

Based on the demo code:

```python
# After tracker.update(image_rgb):
pose_uv = model.pose_uv  # e.g., (329, 260) - pixel coordinates
conf = model.conf         # e.g., 0.85 - 85% confidence
pose = model.pose         # 4x4 matrix with rotation and translation

# Visualization:
normal_image = renderer.render()  # RGB image array
# Image shows: original frame + rendered 3D model overlay + text "Cat: 0.85"
```

---

## Key Characteristics

1. **Real-time Tracking**: Processes each frame independently
2. **No Deep Learning**: Uses geometric/sparse region-based methods
3. **Requires Initial Pose**: Must provide starting pose (from `pose.txt` in demo)
4. **Multi-Model Support**: Can track multiple objects simultaneously
5. **Confidence-Based**: Uses KL divergence for quality assessment
6. **Visual Feedback**: Provides rendered visualization for debugging

---

## Use Cases

- **Robotic manipulation**: Track objects for pick-and-place
- **AR/VR applications**: Track objects for augmentation
- **Quality control**: Monitor object position/orientation
- **Autonomous systems**: Object tracking for navigation

---

## Notes

- The algorithm is **tracking-only** (not detection) - requires initial pose
- Confidence score is based on statistical distribution matching (KL divergence)
- The rendered image is for visualization - the main output is the pose matrix
- All outputs are updated every frame after `tracker.update()` is called

```

## Summary: pysrt3d Outputs

pysrt3d outputs the following per frame:

### 1. **6DoF pose** (main output)
- `model.pose`: 4×4 transformation matrix (rotation + translation)
  - Rotation: 3×3 matrix (orientation)
  - Translation: 3D position `[tx, ty, tz]`
  - Coordinate system: OpenCV convention

### 2. **Confidence score**
- `model.conf`: float in `[0.0, 1.0]`
  - Based on KL divergence between observed correspondences and expected distribution
  - `1.0` = perfect tracking, `0.0` = poor/no tracking
  - Proportion of valid correspondence lines

### 3. **2D projection point**
- `model.pose_uv`: `(x, y)` pixel coordinates
  - Where the object center projects onto the image
  - Used for overlaying annotations

### 4. **Visualization image**
- `renderer.render()`: RGB image array
  - Original camera frame + rendered 3D model overlay
  - Shows predicted pose alignment
  - Includes text overlay (model name + confidence)

### 5. **Additional metrics**
- `model.valid_line_prop`: Proportion of valid correspondence lines
- `model.name`: Model identifier

## How it works

For each frame:
1. Input: RGB image
2. `tracker.update(image)` → updates pose estimate
3. Outputs updated: pose, confidence, 2D projection
4. `renderer.render()` → visualization image

The main output is the 6DoF pose matrix, which gives the object’s 3D position and orientation in the camera frame.

Created a detailed explanation document at `/root/pysrt3d/OUTPUT_EXPLANATION.md` with more details.

