# standard library
from typing import *
from pathlib import Path
import numpy as np
import sys
# third party
import cv2
# Add build directory to path for pysrt3d import
_build_dir = Path(__file__).resolve().parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release"
if _build_dir.exists() and str(_build_dir) not in sys.path:
    sys.path.insert(0, str(_build_dir))
import pysrt3d


# fetch images
DATA_DIR = Path(__file__).resolve().parent / 'data'
images_dir = DATA_DIR / 'images'
images = sorted(list(images_dir.glob('*.png')))
h, w = cv2.imread(str(images[0])).shape[:2]

# init model
model = pysrt3d.Model(
    name="Cat",
    model_path=str(DATA_DIR / 'Cat.obj'),
    meta_path=str(DATA_DIR / 'Cat.meta'),
    unit_in_meter=0.001,    # the model was made in 'mm'
    threshold_init = 0.0,   # no limit while initialization
    threshold_track = 0.0,  # no limit while tracking
    kl_threshold = 1.0      
)

# init tracker
tracker = pysrt3d.Tracker(
    imwidth=w,
    imheight=h,
    K=np.loadtxt(DATA_DIR / 'K.txt', dtype=np.float32)
)

# add model to tracker
tracker.add_model(model)
# setup tracker
tracker.setup()
# make renderer
renderer = pysrt3d.Renderer(tracker)

# set init pose
init_pose = np.loadtxt(DATA_DIR / 'pose.txt')
model.reset_pose(init_pose)

# Store poses for all frames
poses_output = []

for idx, image in enumerate(images):
    # read image
    image = cv2.imread(str(image))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # tracking iteration
    tracker.update(image=image_rgb)
    # get tracking info
    pose_uv = model.pose_uv
    conf = model.conf
    pose_6dof = model.pose  # 4x4 6DoF pose matrix
    
    # Store pose for this frame
    poses_output.append({
        'frame': idx,
        'pose': pose_6dof,
        'confidence': conf,
        'pose_uv': pose_uv
    })
    
    # Print pose to console
    print(f"Frame {idx:04d}: confidence={conf:.4f}, pose_uv={pose_uv}")
    print(f"  Pose matrix:\n{pose_6dof}\n")

    # render normal view
    normal_image = renderer.render()
    # write tracking info
    cv2.putText(normal_image, f"{model.name}: {conf:.2f}", pose_uv, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('view', normal_image)
    cv2.waitKey(0)

# Save all poses to file (text format)
poses_output_file = DATA_DIR / 'poses_output.txt'
with open(poses_output_file, 'w') as f:
    for item in poses_output:
        f.write(f"# Frame {item['frame']:04d}: confidence={item['confidence']:.4f}, pose_uv={item['pose_uv']}\n")
        np.savetxt(f, item['pose'], fmt='%.6f', delimiter='\t')
        f.write('\n')

# Also save as numpy array for easy loading (shape: [num_frames, 4, 4])
poses_array = np.array([item['pose'] for item in poses_output])
poses_npy_file = DATA_DIR / 'poses_output.npy'
np.save(poses_npy_file, poses_array)

# Save metadata (confidence and pose_uv for each frame)
metadata = {
    'confidences': [item['confidence'] for item in poses_output],
    'pose_uv': [item['pose_uv'] for item in poses_output]
}
metadata_file = DATA_DIR / 'poses_metadata.npy'
np.save(metadata_file, metadata)

print(f"\nAll poses saved to:")
print(f"  - Text format: {poses_output_file}")
print(f"  - NumPy array: {poses_npy_file} (shape: {poses_array.shape})")
print(f"  - Metadata: {metadata_file}")