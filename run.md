# run.py - pysrt3d Object Tracking Script

## Overview

`run.py` is a generic command-line script for running 6DoF (6 Degrees of Freedom) object tracking using the `pysrt3d` library. It processes a sequence of images, tracks the 3D pose of an object in each frame, and saves all tracking results including pose matrices, confidence scores, and visualization images.

## Features

- **Automated tracking pipeline**: Processes entire image sequences automatically
- **Comprehensive output**: Saves 6DoF poses in multiple formats (text, NumPy arrays)
- **Flexible input**: Supports various image formats and flexible file naming
- **Visualization**: Generates rendered visualization images showing tracking results
- **Metadata tracking**: Records confidence scores, 2D projections, and tracking quality metrics
- **Batch processing**: Can run without interactive visualization for automated workflows

## Requirements

### Prerequisites

1. **Installed pysrt3d package**:
   ```bash
   pip install .
   ```

2. **Python dependencies**:
   - `numpy`
   - `opencv-python` (cv2)

3. **Input data** (see Input Directory Structure below)

## Input Directory Structure

The script expects a specific directory structure containing all necessary input files:

```
input_dir/
  ├── model.obj          # 3D model file (Wavefront OBJ format)
  ├── model.meta         # Metadata file (optional, auto-generated if missing)
  ├── K.txt              # Camera intrinsics matrix (3x3, space/tab-separated)
  ├── pose.txt           # Initial 6DoF pose matrix (4x4, space/tab-separated)
  └── images/            # Directory containing input images
      ├── 0000.png
      ├── 0001.png
      ├── 0002.png
      └── ...
```

### File Format Details

#### `model.obj`
- 3D model file in Wavefront OBJ format
- Can be named anything (e.g., `Cat.obj`, `object.obj`)
- The script will auto-detect any `.obj` file in the input directory

#### `model.meta`
- Metadata file for the 3D model
- If not found, the script will look for a `.meta` file matching the model name
- If still not found, it will be auto-generated (warning will be shown)

#### `K.txt` (Camera Intrinsics)
- 3×3 camera intrinsic matrix
- Format: space or tab-separated values
- Example:
  ```
  fx  0   cx
  0   fy  cy
  0   0   1
  ```

#### `pose.txt` (Initial Pose)
- 4×4 transformation matrix representing the initial 6DoF pose
- Format: space or tab-separated values
- OpenCV coordinate system
- Example:
  ```
  R00  R01  R02  tx
  R10  R11  R12  ty
  R20  R21  R22  tz
  0    0    0    1
  ```

#### `images/` Directory
- Contains input images for tracking
- Supported formats: `.png`, `.jpg` (configurable)
- Images should be named sequentially (e.g., `0000.png`, `0001.png`)
- Images are processed in alphabetical order

## Command-Line Arguments

### Required Arguments

| Argument | Description |
|----------|-------------|
| `--input_dir` | Path to input directory containing model, camera intrinsics, initial pose, and images |

### Optional Arguments

#### Output Configuration

| Argument | Default | Description |
|----------|---------|-------------|
| `--output_dir` | `./user/output` | Path to output directory where all results will be saved |

#### Model Parameters

| Argument | Default | Description |
|----------|---------|-------------|
| `--model_name` | `None` | Model name (default: derived from model filename) |
| `--unit_in_meter` | `1.0` | Scale factor for model units (use `0.001` for millimeter-scale models) |
| `--sphere_radius` | `0.8` | Sphere radius for region generation |
| `--threshold_init` | `0.0` | Confidence threshold for initialization (`0.0` = no limit) |
| `--threshold_track` | `0.0` | Confidence threshold for tracking (`0.0` = no limit) |
| `--kl_threshold` | `1.0` | KL divergence threshold for confidence assessment |

#### Tracker Parameters

| Argument | Default | Description |
|----------|---------|-------------|
| `--corr_iter` | `7` | Number of correspondence update iterations |
| `--pose_iter` | `2` | Number of pose update iterations |

#### Runtime Options

| Argument | Description |
|----------|-------------|
| `--no_visualize` | Disable interactive visualization (useful for batch processing) |
| `--save_visualizations` | Save visualization images (default: `True`) |
| `--image_ext` | Image file extensions to process (default: `png jpg`) |

## Output Directory Structure

After running the script, the output directory will contain:

```
output_dir/
  ├── poses.txt              # All 6DoF poses in human-readable text format
  ├── poses.npy              # All poses as NumPy array [N, 4, 4] (OpenCV coordinates)
  ├── poses_gl.npy           # All poses as NumPy array [N, 4, 4] (OpenGL coordinates)
  ├── metadata.npy           # Tracking metadata (NumPy format)
  ├── metadata.txt           # Tracking metadata (text format)
  └── visualizations/        # Rendered visualization images
      ├── frame_0000.png
      ├── frame_0001.png
      └── ...
```

### Output File Details

#### `poses.txt`
- Human-readable text format
- Each frame's pose is preceded by a comment line with frame number, confidence, and 2D projection
- Format matches the input `pose.txt` format
- Example:
  ```
  # Frame 0000: confidence=0.9234, pose_uv=(320, 240)
  0.786030  -0.587438  0.192550  0.281848
  0.604647   0.795404 -0.041652 -0.166599
  -0.128687  0.149164  0.980401  0.731918
  0.000000   0.000000  0.000000  1.000000
  ```

#### `poses.npy`
- NumPy array format for easy programmatic access
- Shape: `[num_frames, 4, 4]`
- OpenCV coordinate system
- Load with: `poses = np.load('poses.npy')`

#### `poses_gl.npy`
- Same format as `poses.npy` but in OpenGL coordinate system
- Useful for rendering or visualization in OpenGL-based applications

#### `metadata.npy` and `metadata.txt`
- Contains per-frame tracking information:
  - `confidences`: Tracking confidence scores (0.0 to 1.0)
  - `pose_uv`: 2D projection of object center `(u, v)` in image coordinates
  - `valid_line_prop`: Proportion of valid correspondence lines
  - `frame_numbers`: Frame indices

#### `visualizations/`
- Rendered images showing the tracked object overlaid on the scene
- Each image shows the normal map visualization with tracking info overlay
- Useful for visual inspection of tracking quality

## Usage Examples

### Basic Usage

Process images with default settings:

```bash
python run.py --input_dir example/data
```

### Custom Output Directory

Save results to a specific location:

```bash
python run.py --input_dir example/data --output_dir ./results/tracking_run_001
```

### Millimeter-Scale Models

For models created in millimeters (common for 3D printed objects):

```bash
python run.py --input_dir example/data --unit_in_meter 0.001
```

### Batch Processing

Run without interactive visualization (useful for automated workflows):

```bash
python run.py --input_dir example/data --no_visualize
```

### Custom Tracker Settings

Adjust tracking parameters for better performance:

```bash
python run.py --input_dir example/data --corr_iter 10 --pose_iter 3
```

### Threshold-Based Tracking

Set confidence thresholds to filter low-quality tracking:

```bash
python run.py --input_dir example/data --threshold_init 0.8 --threshold_track 0.5
```

### Process Only Specific Image Types

Only process JPEG images:

```bash
python run.py --input_dir example/data --image_ext jpg
```

### Complete Example

Full example with all custom parameters:

```bash
python run.py \
  --input_dir ./my_data/cat_sequence \
  --output_dir ./results/cat_tracking \
  --model_name "Cat" \
  --unit_in_meter 0.001 \
  --threshold_init 0.8 \
  --threshold_track 0.5 \
  --kl_threshold 1.0 \
  --corr_iter 7 \
  --pose_iter 2 \
  --no_visualize
```

## Loading Results in Python

### Load Poses

```python
import numpy as np

# Load all poses (OpenCV coordinates)
poses = np.load('output_dir/poses.npy')  # Shape: [N, 4, 4]

# Get pose for specific frame
frame_10_pose = poses[10]

# Load OpenGL poses
poses_gl = np.load('output_dir/poses_gl.npy')
```

### Load Metadata

```python
import numpy as np

# Load metadata
metadata = np.load('output_dir/metadata.npy', allow_pickle=True).item()

# Access tracking information
confidences = metadata['confidences']
pose_uv = metadata['pose_uv']
valid_line_prop = metadata['valid_line_prop']
frame_numbers = metadata['frame_numbers']

# Get confidence for frame 5
frame_5_conf = confidences[5]
```

### Read Text Format

```python
# Read poses from text file (for human inspection)
with open('output_dir/poses.txt', 'r') as f:
    content = f.read()
    # Parse as needed
```

## Troubleshooting

### Common Issues

#### 1. "pysrt3d module not found"
**Solution**: Install the package first:
```bash
pip install .
```

#### 2. "Model file not found"
**Solution**: Ensure your input directory contains a `.obj` file. The script will auto-detect any `.obj` file, or you can name it `model.obj`.

#### 3. "Camera intrinsics file not found"
**Solution**: Create a `K.txt` file with your 3×3 camera intrinsic matrix.

#### 4. "Initial pose file not found"
**Solution**: Create a `pose.txt` file with the initial 4×4 pose matrix. This is required for tracking initialization.

#### 5. "No images found"
**Solution**: Ensure your `images/` directory contains `.png` or `.jpg` files. Check the `--image_ext` argument if using other formats.

#### 6. Low tracking confidence
**Solutions**:
- Ensure initial pose is accurate
- Check camera intrinsics are correct
- Adjust `--threshold_init` and `--threshold_track` parameters
- Verify model scale (`--unit_in_meter`) is correct
- Check image quality and lighting conditions

#### 7. Tracking fails or drifts
**Solutions**:
- Increase `--corr_iter` and `--pose_iter` for more iterations
- Adjust `--kl_threshold` for stricter confidence filtering
- Verify initial pose accuracy
- Check that model matches the object in images

### Validation

The script performs automatic validation of inputs before processing:
- Checks for required files
- Validates file formats (matrix dimensions)
- Verifies image directory exists and contains images
- Reports all errors before starting

## Notes

1. **Initial Pose Requirement**: This is a tracking-only system. You must provide an accurate initial pose; the system does not perform global pose estimation.

2. **Coordinate Systems**: 
   - Default poses are in OpenCV coordinates
   - OpenGL poses are also saved for compatibility

3. **Image Format**: Images are expected in RGB format. The script handles BGR→RGB conversion automatically.

4. **Performance**: For large sequences, use `--no_visualize` to speed up processing.

5. **Memory**: Large sequences may require significant memory. Monitor system resources for very long sequences.

## See Also

- `example/demo.py`: Original demo script with interactive visualization
- `readme.md`: Project overview and installation instructions
- `source/pysrt3d/pysrt3d.cpp`: Python bindings implementation

## Getting Help

To see all available options and their descriptions:

```bash
python run.py --help
```
