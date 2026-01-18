# estimate_k_matrix.py - K-Matrix Estimation Tool

## Overview

`estimate_k_matrix.py` is a command-line tool that automatically estimates camera intrinsics (K-matrix) from a single image using **Depth-Anything-3 (DA3)**. This tool eliminates the need for physical calibration patterns (like checkerboards) and provides a quick way to obtain camera intrinsics for use with pysrt3d.

## Features

- **Automatic estimation**: No calibration pattern required
- **Single image**: Works with just one image
- **Easy to use**: Simple command-line interface
- **Compatible with pysrt3d**: Outputs K-matrix in the exact format needed by pysrt3d
- **Works with unknown cameras**: Useful when camera specifications are unavailable

## Installation

### Prerequisites

1. **Python 3.7+** installed

2. **Install one of the following DA3 packages**:

   **Option A: awesome-depth-anything-3 (Recommended)**
   ```bash
   pip install awesome-depth-anything-3
   ```
   - PyPI package, easier to install
   - Production optimizations (caching, batching)
   - Better device support (Apple Silicon, etc.)

   **Option B: Install from GitHub (Original)**
   ```bash
   pip install git+https://github.com/ByteDance-Seed/Depth-Anything-3.git
   ```
   - Original repository
   - Latest features
   - Requires git

   **Note:** The first time you run the script, DA3 will download model weights (this may take a few minutes and require several GB of disk space).

3. **Additional dependencies** (usually installed with depth-anything-v3):
   - `numpy`
   - `opencv-python` (cv2)

### Verify Installation

**For awesome-depth-anything-3:**
```bash
python -c "from depth_anything_3.api import DepthAnything3; print('awesome-DA3 installed successfully')"
```

**For original depth-anything-v3:**
```bash
python -c "from depth_anything_v3 import DepthAnythingV3; print('DA3 installed successfully')"
```

The script automatically detects which package is available and uses it accordingly.

## Usage

### Basic Usage

```bash
python lib/estimate_k_matrix.py --image path/to/image.png --output K.txt
```

### Arguments

| Argument | Required | Description | Example |
|----------|----------|-------------|---------|
| `--image` | Yes | Path to input image file | `--image frame_0000.png` |
| `--output` | Yes | Path to output K-matrix file (should be .txt) | `--output K.txt` |

### Examples

#### Example 1: Estimate K-matrix from first frame

```bash
# Estimate K-matrix from the first frame of your sequence
python lib/estimate_k_matrix.py \
    --image example/data/images/0000.png \
    --output example/data/K_estimated.txt
```

#### Example 2: Use with full paths

```bash
python lib/estimate_k_matrix.py \
    --image /path/to/your/image.png \
    --output /path/to/output/K.txt
```

#### Example 3: Estimate K-matrix for pysrt3d tracking

```bash
# Step 1: Estimate K-matrix
python lib/estimate_k_matrix.py \
    --image user/input/earbud/images/0000.png \
    --output user/input/earbud/K.txt

# Step 2: Use with pysrt3d (in your tracking script)
import numpy as np
import pysrt3d

K = np.loadtxt('user/input/earbud/K.txt', dtype=np.float32)
tracker = pysrt3d.Tracker(imwidth=640, imheight=480, K=K)
```

## Output Format

The script outputs a 3×3 K-matrix in the following format:

```
fx   0   cx
0   fy   cy
0    0    1
```

**File format:**
- Space-separated values
- 3 rows × 3 columns
- Floating-point numbers (6 decimal places)
- Compatible with `np.loadtxt()` and pysrt3d

**Example output file (`K.txt`):**
```
481.340250  0.000000  329.400300
0.000000  481.824300  260.378800
0.000000  0.000000  1.000000
```

## How It Works

1. **Load Image**: Reads the input image file
2. **Initialize DA3**: Loads the Depth-Anything-3 model (first run downloads weights)
3. **Process Image**: DA3 analyzes the image to estimate camera intrinsics
4. **Extract Parameters**: Gets focal lengths (fx, fy) and principal point (cx, cy)
5. **Construct K-Matrix**: Builds the 3×3 camera intrinsics matrix
6. **Save to File**: Writes the K-matrix to the specified output file

## Integration with pysrt3d

### Step-by-Step Workflow

1. **Estimate K-matrix**:
   ```bash
   python lib/estimate_k_matrix.py --image first_frame.png --output K.txt
   ```

2. **Use in pysrt3d**:
   ```python
   import numpy as np
   import pysrt3d
   import cv2
   
   # Load estimated K-matrix
   K = np.loadtxt('K.txt', dtype=np.float32)
   
   # Get image dimensions
   image = cv2.imread('first_frame.png')
   h, w = image.shape[:2]
   
   # Create tracker with estimated K-matrix
   tracker = pysrt3d.Tracker(
       imwidth=w,
       imheight=h,
       K=K  # Use the estimated K-matrix
   )
   
   # Continue with your tracking setup...
   model = pysrt3d.Model(...)
   tracker.add_model(model)
   tracker.setup()
   ```

## Limitations and Considerations

### Accuracy

- **Model-dependent**: Accuracy varies with DA3 model variant
- **Camera-dependent**: Works best with standard cameras; may be less accurate for:
  - Wide-angle lenses
  - Fisheye lenses
  - Unusual lens configurations
- **Validation recommended**: Compare with known calibration if available

### Performance

- **First run**: Model weights are downloaded (several GB, one-time)
- **Processing time**: Typically 1-5 seconds per image (depends on GPU/CPU)
- **Memory**: Requires sufficient RAM/VRAM for model loading

### When to Use This Method

✅ **Good for:**
- Unknown cameras (no calibration data available)
- Quick setup without calibration pattern
- Single image sequences
- Prototyping and testing

❌ **Consider alternatives if:**
- You need maximum accuracy (use Method 1: Camera Calibration)
- You have camera specifications (use Method 2: Camera Specifications)
- You're working with unusual lenses
- You need metric-scale accuracy (consider DA3Metric variants)

## Troubleshooting

### Error: "Neither awesome-depth-anything-3 nor depth-anything-v3 package found"

**Solution:**
Install one of the supported packages:
```bash
# Recommended: awesome-depth-anything-3 (PyPI package)
pip install awesome-depth-anything-3

# OR: Original from GitHub
pip install git+https://github.com/ByteDance-Seed/Depth-Anything-3.git
```

### Error: "Failed to initialize Depth-Anything-3"

**Possible causes:**
- Missing model files (first run downloads them automatically)
- GPU/CUDA issues
- Insufficient memory

**Solutions:**
- Wait for model download to complete (first run only)
- Check GPU drivers if using GPU
- Try running on CPU (may be slower)

### Error: "Camera intrinsics not found in DA3 result"

**Possible causes:**
- DA3 model variant doesn't support intrinsics estimation
- Image processing failed

**Solutions:**
- Ensure you're using a DA3 model that supports camera intrinsics
- Try a different image
- Check image format (PNG, JPG supported)

### Error: "Could not read image file"

**Solutions:**
- Verify image path is correct
- Check image file format (PNG, JPG, etc.)
- Ensure file is not corrupted

## Comparison with Other Methods

| Method | Requires | Accuracy | Setup Time |
|--------|----------|----------|------------|
| **Method 1: Camera Calibration** | Checkerboard pattern, multiple images | High | High (calibration session) |
| **Method 2: Camera Specifications** | Camera specs (focal length, sensor size) | Medium | Low |
| **Method 3: Manufacturer Data** | Camera calibration data | High | Low |
| **Method 4: DA3 (This Tool)** | Single image | Medium-High | Low (after initial setup) |
| **Method 5: Estimated Values** | None | Low | Very Low |

## Advanced Usage

### Using Different DA3 Model Variants

**For awesome-depth-anything-3:**
The script uses `DA3-BASE` by default. To use a different model, modify the script:
- `DA3-SMALL`: Fastest, smallest
- `DA3-BASE`: Balanced (default)
- `DA3-LARGE`: Better accuracy
- `DA3-GIANT`: Best accuracy, slowest
- `DA3METRIC-LARGE`: Metric depth variant

**For original depth-anything-v3:**
Check the package documentation for model variant options.

### Batch Processing

To estimate K-matrices for multiple images:

```bash
# Bash script example
for img in images/*.png; do
    output_name=$(basename "$img" .png)_K.txt
    python lib/estimate_k_matrix.py --image "$img" --output "K_matrices/$output_name"
done
```

### Python API Usage

You can also use the estimation function directly in Python:

```python
from pathlib import Path
from lib.estimate_k_matrix import estimate_k_matrix

# Estimate K-matrix
success = estimate_k_matrix(
    image_path=Path('frame_0000.png'),
    output_path=Path('K.txt')
)

if success:
    print("K-matrix estimated successfully!")
```

## Related Documentation

- **`documents/input_k_and_startPose.md`**: Complete guide on K-matrix and initial pose
- **`documents/output_pose_matrix.md`**: Understanding pose matrices and projections
- **Depth-Anything-3 Repository**: https://github.com/ByteDance-Seed/Depth-Anything-3

## References

- **Depth-Anything-3 Paper**: "Depth Anything 3: Recovering the visual space from any views"
- **DA3 GitHub**: https://github.com/ByteDance-Seed/Depth-Anything-3
- **PyPI Package**: https://pypi.org/project/depth-anything-v3/

---

**Last Updated:** Based on pysrt3d integration with Depth-Anything-3
