#!/usr/bin/env python3
"""
Visualize where the object would appear in the image based on the pose.txt
"""

import numpy as np
import cv2
from pathlib import Path

# Load pose and camera intrinsics
DATA_DIR = Path(__file__).resolve().parent
pose = np.loadtxt(DATA_DIR / 'pose.txt', dtype=np.float32)
K = np.loadtxt(DATA_DIR / 'K.txt', dtype=np.float32)

print("="*60)
print("POSE VISUALIZATION")
print("="*60)

# Extract translation
tx, ty, tz = pose[0, 3], pose[1, 3], pose[2, 3]
print(f"\nTranslation (camera coordinates):")
print(f"  X (right):     {tx:8.4f} meters")
print(f"  Y (down):      {ty:8.4f} meters")
print(f"  Z (forward):   {tz:8.4f} meters ({tz*100:.2f} cm)")

# Extract rotation (check if it's identity)
rotation = pose[:3, :3]
is_identity = np.allclose(rotation, np.eye(3))
print(f"\nRotation:")
if is_identity:
    print("  Identity matrix (no rotation)")
    print("  Object axes align with camera axes")
else:
    print("  Rotation matrix:")
    print(rotation)

# Project to image plane
fx, fy = K[0, 0], K[1, 1]
cx, cy = K[0, 2], K[1, 2]

# Project the object center (assuming it's at the pose translation)
if tz > 0:  # Only project if in front of camera
    u = (fx * tx / tz) + cx
    v = (fy * ty / tz) + cy
    print(f"\nProjected position in image:")
    print(f"  Pixel (u, v): ({u:.1f}, {v:.1f})")
else:
    print("\n[WARNING] Object is behind camera (Z < 0)!")

# Load first image to show where object would be
first_image_path = DATA_DIR / 'images' / 'earbuds_003_00110.png'
if first_image_path.exists():
    img = cv2.imread(str(first_image_path))
    h, w = img.shape[:2]
    print(f"\nImage dimensions: {w} × {h} pixels")
    print(f"Principal point (cx, cy): ({cx:.1f}, {cy:.1f})")
    
    # Check if projected point is within image bounds
    if tz > 0:
        in_bounds = (0 <= u < w) and (0 <= v < h)
        print(f"\nProjected point status:")
        if in_bounds:
            print(f"  [OK] Within image bounds")
            print(f"  Location: {u:.1f} pixels from left, {v:.1f} pixels from top")
        else:
            print(f"  [ERROR] OUTSIDE image bounds!")
            if u < 0:
                print(f"    Too far LEFT (u = {u:.1f} < 0)")
            elif u >= w:
                print(f"    Too far RIGHT (u = {u:.1f} >= {w})")
            if v < 0:
                print(f"    Too far UP (v = {v:.1f} < 0)")
            elif v >= h:
                print(f"    Too far DOWN (v = {v:.1f} >= {h})")
    
    # Create visualization
    vis_img = img.copy()
    
    # Draw coordinate system at image center
    center_u, center_v = int(cx), int(cy)
    cv2.circle(vis_img, (center_u, center_v), 5, (0, 255, 0), -1)  # Green dot at principal point
    cv2.putText(vis_img, "Principal Point", (center_u + 10, center_v - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    
    # Draw projected point if valid
    if tz > 0 and 0 <= u < w and 0 <= v < h:
        proj_u, proj_v = int(u), int(v)
        cv2.circle(vis_img, (proj_u, proj_v), 10, (0, 0, 255), 2)  # Red circle
        cv2.putText(vis_img, f"Pose Projection ({u:.0f}, {v:.0f})", 
                    (proj_u + 15, proj_v - 15),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        # Draw line from principal point to projected point
        cv2.line(vis_img, (center_u, center_v), (proj_u, proj_v), (255, 0, 0), 1)
    
    # Add text overlay
    info_text = [
        f"Pose Translation: ({tx:.3f}, {ty:.3f}, {tz:.3f}) m",
        f"Distance: {tz*100:.1f} cm",
        f"Projected to: ({u:.1f}, {v:.1f})" if tz > 0 else "Behind camera",
    ]
    
    y_offset = 30
    for i, text in enumerate(info_text):
        cv2.putText(vis_img, text, (10, y_offset + i*25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(vis_img, text, (10, y_offset + i*25),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 1)
    
    # Save visualization
    output_path = DATA_DIR / 'pose_visualization.png'
    cv2.imwrite(str(output_path), vis_img)
    print(f"\n[OK] Visualization saved to: {output_path}")
    print(f"   - Green dot: Principal point (camera center)")
    print(f"   - Red circle: Where object center would project")
    print(f"   - Blue line: Connection between principal point and projection")
    
else:
    print(f"\n[WARNING] First image not found: {first_image_path}")

# Additional analysis
print("\n" + "="*60)
print("ANALYSIS")
print("="*60)

print(f"\n1. Object Position:")
print(f"   - Horizontal offset: {tx*100:.1f} cm {'right' if tx > 0 else 'left' if tx < 0 else 'centered'}")
print(f"   - Vertical offset: {ty*100:.1f} cm {'down' if ty > 0 else 'up' if ty < 0 else 'centered'}")
print(f"   - Distance from camera: {tz*100:.1f} cm")

if tz > 0:
    # Estimate object size in image (assuming object is ~2-3 cm)
    object_size_m = 0.025  # 2.5 cm typical earbud size
    pixel_size = (fx * object_size_m) / tz
    print(f"\n2. Estimated Object Size in Image:")
    print(f"   - Assuming object is ~2.5 cm:")
    print(f"   - Would appear as ~{pixel_size:.1f} pixels wide")
    print(f"   - At {tz*100:.1f} cm distance, this is {'very small' if pixel_size < 20 else 'small' if pixel_size < 50 else 'reasonable'}")

print(f"\n3. Potential Issues:")
issues = []
if abs(tx) > 0.5:
    issues.append(f"   - Large horizontal offset ({tx*100:.1f} cm) might place object outside view")
if abs(ty) > 0.5:
    issues.append(f"   - Large vertical offset ({ty*100:.1f} cm) might place object outside view")
if tz > 1.0:
    issues.append(f"   - Object is far ({tz*100:.1f} cm), might be too small to track")
if tz < 0.2:
    issues.append(f"   - Object is very close ({tz*100:.1f} cm), might be too large or out of focus")
if is_identity:
    issues.append(f"   - No rotation: object might be oriented incorrectly")

if issues:
    for issue in issues:
        print(issue)
else:
    print("   [OK] No obvious issues detected")

print("\n" + "="*60)
