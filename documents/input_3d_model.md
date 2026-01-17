# 3D Model Format Support in pysrt3d

## Summary

**Only Wavefront OBJ format (`.obj`) is supported.** Other formats such as GLB, GLTF, PLY, STL, or FBX are **not supported**.

## Technical Details

### Library Used: `tiny_obj_loader`

The `pysrt3d` library uses the **tiny_obj_loader** library (included in `source/third_party/tiny_obj_loader/`) which is specifically designed to load only **Wavefront OBJ format** files.

### Code Evidence

#### 1. Model Loading in `body.cpp`

**File:** `source/src/body.cpp` (lines 120-126)

```cpp
if (!tinyobj::LoadObj(&attributes, &shapes, &materials, &warning, &error,
                      geometry_path_.string().c_str(), nullptr, true,
                      false)) {
  std::cerr << "TinyObjLoader failed to load data from " << geometry_path_
            << std::endl;
  return;
}
```

This function explicitly calls `tinyobj::LoadObj()`, which only supports OBJ files.

#### 2. Mesh Loading in `renderer_geometry.cpp`

**File:** `source/src/renderer_geometry.cpp` (lines 180-186)

```cpp
if (!tinyobj::LoadObj(&attributes, &shapes, &materials, &warning, &error,
                      body.geometry_path().string().c_str(), nullptr, true,
                      false)) {
  std::cerr << "TinyObjLoader failed to load data from "
            << body.geometry_path() << std::endl;
  return false;
}
```

Again, only `LoadObj()` is used - no other format loaders exist.

#### 3. tiny_obj_loader API

**File:** `source/third_party/tiny_obj_loader/tiny_obj_loader.h` (lines 346-383)

The library provides only these functions:
- `LoadObj()` - Loads `.obj` files
- `LoadObjWithCallback()` - Loads `.obj` files with callbacks
- `LoadMtl()` - Loads `.mtl` material files (used with OBJ)

**No functions exist for:**
- GLB/GLTF files
- PLY files
- STL files
- FBX files
- Any other 3D format

### Supported Format: Wavefront OBJ

**Format:** Wavefront OBJ (`.obj`)

**Features supported:**
- Vertices (`v`)
- Texture coordinates (`vt`)
- Normals (`vn`)
- Faces (`f`)
- Materials (via `.mtl` files)

**Requirements:**
- The mesh must be triangulated (triangular faces only)
- Non-triangular faces will be skipped with a warning

**Example from code:**
```cpp
if (shape.mesh.num_face_vertices[f] != 3) {
  std::cerr << "Mesh contains non triangle shapes" << std::endl;
  index_offset += shape.mesh.num_face_vertices[f];
  continue;  // Skip non-triangular faces
}
```

## Converting Other Formats to OBJ

If you have a model in another format (GLB, GLTF, PLY, STL, FBX, etc.), you need to convert it to OBJ format first.

### Conversion Tools

#### 1. **Blender** (Free, Open Source)
```bash
# Using Blender command line:
blender --background --python convert_to_obj.py

# Or use Blender GUI:
# File → Export → Wavefront (.obj)
```

#### 2. **MeshLab** (Free, Open Source)
- Open your model
- File → Export Mesh As → Wavefront OBJ

#### 3. **Assimp** (Command Line)
```bash
assimp export input.glb output.obj
```

#### 4. **Online Converters**
- Various online tools can convert GLB/GLTF to OBJ
- **Note:** Be cautious with online tools for sensitive data

#### 5. **Python Libraries**
```python
# Using trimesh
import trimesh
mesh = trimesh.load('model.glb')
mesh.export('model.obj')

# Using pyassimp
import pyassimp
scene = pyassimp.load('model.glb')
pyassimp.export(scene, 'model.obj', 'obj')
```

### Conversion Checklist

When converting to OBJ:

1. ✅ **Triangulate the mesh** - OBJ supports quads, but pysrt3d requires triangles
2. ✅ **Export normals** - Helps with rendering quality
3. ✅ **Check scale** - Note the units (meters, millimeters, etc.) for `unit_in_meter` parameter
4. ✅ **Export materials** - If needed, export `.mtl` file alongside `.obj`
5. ✅ **Test the OBJ file** - Verify it loads correctly before using with pysrt3d

## Current Implementation Limitations

### Why Only OBJ?

1. **Historical choice**: The original SRT3D library was designed to work with OBJ format
2. **Simplicity**: OBJ is a simple, text-based format that's easy to parse
3. **Widely supported**: OBJ is one of the most common 3D formats
4. **No dependencies**: tiny_obj_loader is a header-only library with no external dependencies

### Could Other Formats Be Added?

**Theoretically yes, but it would require:**

1. **Adding a new loader library** (e.g., `assimp`, `tinygltf`, `plylib`)
2. **Modifying `body.cpp`** to detect file format and call appropriate loader
3. **Modifying `renderer_geometry.cpp`** to use the new loader
4. **Handling format-specific features** (e.g., GLB binary format, GLTF JSON)
5. **Testing and validation** across different formats

**Current status:** No plans or code exist for supporting other formats.

## Example Usage

### Correct (OBJ format):
```python
model = pysrt3d.Model(
    name="MyObject",
    model_path="model.obj",  # ✅ OBJ format
    meta_path="model.meta",
    unit_in_meter=0.001
)
```

### Incorrect (Other formats):
```python
model = pysrt3d.Model(
    name="MyObject",
    model_path="model.glb",  # ❌ Will fail - GLB not supported
    meta_path="model.meta",
    unit_in_meter=0.001
)
```

**Error you'll get:**
```
TinyObjLoader failed to load data from model.glb
```

## Recommendations

1. **For new projects**: Use OBJ format from the start
2. **For existing models**: Convert to OBJ using one of the tools mentioned above
3. **For batch conversion**: Use command-line tools (Blender, Assimp) for automation
4. **For quality**: Ensure OBJ files are properly triangulated and have normals

## References

- **Wavefront OBJ Format**: https://en.wikipedia.org/wiki/Wavefront_.obj_file
- **tiny_obj_loader**: https://github.com/tinyobjloader/tinyobjloader
- **SRT3D Library**: Original implementation by Manuel Stoiber, DLR

---

**Last Updated:** Based on codebase analysis of pysrt3d v0.0.0
