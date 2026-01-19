#!/usr/bin/env python3
"""
Create a truly standalone Blender script with all pose data embedded
"""

from pathlib import Path

script_dir = Path(__file__).parent

# Read the standalone script (without embedded data)
standalone_script = script_dir / "blender_animate_standalone.py"
embedded_data = script_dir / "embedded_poses_data.py"

print("Creating standalone script...")

# Read standalone script
with open(standalone_script, 'r') as f:
    script_content = f.read()

# Read embedded data
with open(embedded_data, 'r') as f:
    embedded_content = f.read()

# Find where to insert the embedded data
# Replace the load_embedded_poses function with direct assignment
insert_marker = "def load_embedded_poses():"
end_marker = "    ]\n"

# Extract the EMBEDDED_POSES from the embedded file
embedded_poses_start = embedded_content.find("EMBEDDED_POSES = [")
embedded_poses_end = embedded_content.rfind("]") + 1
embedded_poses_data = embedded_content[embedded_poses_start:embedded_poses_end]

# Create new script
new_script = script_content.replace(
    """# Try to load from separate file first (if available)
def load_embedded_poses():
    \"\"\"Load embedded poses - tries file first, then uses fallback data.\"\"\"
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
    ]""",
    """# Embedded pose data (310 frames) - all data included inline
""" + embedded_poses_data + """

def load_embedded_poses():
    \"\"\"Return embedded poses (all data is in script).\"\"\"
    return EMBEDDED_POSES"""
)

# Also update the main function to use embedded data directly
new_script = new_script.replace(
    """    if poses_data is None:
        print("\nTrying to load embedded pose data...")
        poses_data = load_embedded_poses()
        if len(poses_data) <= 1:
            print("[ERROR] Embedded pose data not found or incomplete!")
            print("        Please ensure embedded_poses_data.py exists in the same directory,")
            print("        or run generate_embedded_poses.py to create it.")
            return""",
    """    if poses_data is None:
        print("\nUsing embedded pose data (included in script)...")
        poses_data = load_embedded_poses()
        if len(poses_data) <= 1:
            print("[ERROR] Embedded pose data incomplete!")
            return"""
)

# Write the combined script
output_file = script_dir / "blender_animate_standalone_complete.py"
with open(output_file, 'w') as f:
    f.write(new_script)

print(f"[OK] Created standalone script: {output_file}")
print(f"     Size: {len(new_script)} characters")
print(f"     Includes all {len(embedded_poses_data.split('# Frame')) - 1} frames of pose data")
