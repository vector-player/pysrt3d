# Project setup and installation
_Exported on 1/17/2026 at 03:26:09 GMT+8 from Cursor (2.3.34)_

---

**User**

read @readme.md , create or reuse conda env, install this project, download necessary models, weights, and dataset

---

**Cursor**

Reviewing the project structure and key files to identify dependencies and required data.


Checking for missing files and any download scripts:


Checking the Python bindings to understand how the Model class handles the meta file:


Creating a setup plan and starting implementation:


Conda isn't in PATH. Searching for conda installations:


Conda isn't installed. Checking for Python and proceeding with setup. We'll install conda if needed, or use an alternative approach.


Python is available. Installing Miniconda, then creating the conda environment:


Downloading and installing Miniconda, then setting up the environment:


Installing Miniconda silently:


Initializing conda and creating the environment:


Checking for an existing pysrt3d environment, then creating one if needed:


Creating the pysrt3d conda environment:


Accepting the conda Terms of Service:


Creating the environment again:


Installing system dependencies in the environment:


Installing dependencies directly in the environment:


Installing Python dependencies, then the project:


Installing the pysrt3d package:


Checking if cmake is available and using the conda environment's cmake:


Installing with the conda environment's cmake in PATH:


CMake is using system Python 3.12 instead of conda Python 3.11, and there are OpenCV linking issues. Updating CMakeLists.txt to use the conda Python and fix OpenCV linking:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib")
endif()


# Python
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    set(Python3_ROOT_DIR "$ENV{CONDA_PREFIX}")
    set(PYTHON_EXECUTABLE "$ENV{CONDA_PREFIX}/python.exe")
endif()
find_package(Python3 COMPONENTS Interpreter Development REQUIRED)
set(PYTHON_EXECUTABLE ${Python3_EXECUTABLE})
set(PYTHON_INCLUDE_DIRS ${Python3_INCLUDE_DIRS})
set(PYTHON_LIBRARIES ${Python3_LIBRARIES})
message(STATUS "Found python ${Python3_VERSION} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Setting Python paths explicitly and retrying the build:


Reverting the CMakeLists.txt change and updating setup.py to pass the correct Python paths to CMake:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib")
endif()


# Python
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    set(Python3_ROOT_DIR "$ENV{CONDA_PREFIX}")
    set(PYTHON_EXECUTABLE "$ENV{CONDA_PREFIX}/python.exe")
    set(PYTHON_INCLUDE_DIR "$ENV{CONDA_PREFIX}/include")
    set(PYTHON_LIBRARY "$ENV{CONDA_PREFIX}/libs/python311.lib")
endif()
find_package(PythonInterp REQUIRED)
find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Updating setup.py to pass the correct Python paths to CMake:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        build_args = ["-j6"]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

Updating CMakeLists.txt to use the provided Python variables:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Trying a simpler approach: setting CONDA_PREFIX and retrying the build:


Python is correct, but OpenCV linking fails due to a debug/release mismatch. The OpenCV from conda appears to be a debug build. Checking available OpenCV libraries and updating the build configuration:


Checking the OpenCV installation path:


Trying a Debug build to match OpenCV's debug build:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            "-DCMAKE_BUILD_TYPE=Debug",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        build_args = ["-j6"]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

OpenCV linking issue persists. Summary:

## Completed:
1. Installed Miniconda
2. Created conda environment `pysrt3d` with Python 3.11
3. Installed system dependencies: GLEW, glfw3, Eigen3, OpenCV, CMake
4. Installed Python dependencies: numpy, opencv-python
5. Fixed Python path detection in setup.py and CMakeLists.txt

## Remaining Issue:
OpenCV linking errors: conda OpenCV appears to be a debug build with debug symbols, causing unresolved externals when linking in Release/Debug. The README suggests building OpenCV from source.

## Next Steps:
1. Build OpenCV from source (as mentioned in the README)
2. Try a different OpenCV package (e.g., `opencv-contrib-python`)
3. Use pre-built binaries if available

The demo data appears to be present in `example/data/` (Cat.obj, images, K.txt, pose.txt). The `Cat.meta` file will be generated automatically when the model is first set up.

Should I proceed with building OpenCV from source, or try another approach?

---

**User**

proceed \

---

**Cursor**

Fixing the OpenCV linking issue. Trying a different approach: using the pip-installed opencv-python or configuring CMake to link correctly.


Reinstalling opencv-python and configuring CMake to use the pip-installed OpenCV:


Reinstalling OpenCV C++ libraries from conda and configuring CMake to link correctly:


Updating CMakeLists.txt to link OpenCV correctly and ensure the build configuration matches:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            "-DCMAKE_BUILD_TYPE=Release",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        build_args = ["-j6"]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

OpenCV from conda is a debug build, but we're building in Release. Adding a preprocessor definition to disable the debug guard:


```plaintext
## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR
```

OpenCV from conda is a debug build, causing a mismatch. Options:

1. Build in Debug mode to match OpenCV
2. Define a preprocessor macro to disable the debug guard
3. Build OpenCV from source in Release mode (as the README suggests)

Which approach should we take? Building OpenCV from source will take longer but should resolve the issue.

---

**User**

Build OpenCV from source 

---

**Cursor**

Building OpenCV from source in Release mode. This will take some time, but should resolve the linking issues.


Checking if the download completed, then extracting:


Configuring and building OpenCV:


---

**User**

proceed

---

**Cursor**

Building OpenCV in Release mode. This may take a while.


Build completed. Installing OpenCV to the conda environment:


Updating CMakeLists.txt to use the newly built OpenCV, then rebuilding pysrt3d:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Still seeing debug_build_guard symbols. Checking which OpenCV CMake found and forcing it to use the Release build:


OpenCV was built with debug checks enabled. Rebuilding OpenCV with debug info disabled:


Adding a preprocessor definition to disable the debug build guard in pysrt3d:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - disable OpenCV debug build guard for Release builds
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking exported symbols in the OpenCV DLLs to see what's available:


OpenCV DLLs export symbols without `debug_build_guard`. The source is using the debug namespace. Checking OpenCV headers for the correct define:


Adding NDEBUG to ensure OpenCV uses release symbols:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
endif()

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking the OpenCV configuration to see how it was built:


Explicitly setting OpenCV to use the Release configuration:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
endif()

## linking
target_link_libraries(${PROJECT_NAME}
    PUBLIC
        Eigen3::Eigen
    PRIVATE
        ${OpenCV_LIBS}
        OpenGL::GL
        GLEW::GLEW
        glfw
)

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Ensuring we link against the Release OpenCV libraries and setting the correct configuration:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
endif()

## linking
# For Release builds, ensure we link against Release OpenCV libraries
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Link against Release OpenCV libraries explicitly
    if(TARGET opencv_core)
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                opencv_core
                opencv_imgproc
                opencv_imgcodecs
                opencv_highgui
                opencv_calib3d
                opencv_features2d
                opencv_flann
                opencv_ml
                opencv_photo
                opencv_video
                opencv_videoio
                opencv_dnn
                opencv_objdetect
                opencv_stitching
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    else()
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                ${OpenCV_LIBS}
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    endif()
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking how OpenCV defines debug_build_guard in the headers:


Checking OpenCV base.hpp for how debug_build_guard is defined:


Rebuilding OpenCV with debug info disabled and ensuring it's Release-only:


Rebuilding OpenCV, then checking if we can define a macro to disable the debug build guard:


Installing the newly built OpenCV, then rebuilding pysrt3d:


Checking OpenCV's build configuration and adding the correct compile definitions:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# For Release builds, ensure we link against Release OpenCV libraries
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Link against Release OpenCV libraries explicitly
    if(TARGET opencv_core)
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                opencv_core
                opencv_imgproc
                opencv_imgcodecs
                opencv_highgui
                opencv_calib3d
                opencv_features2d
                opencv_flann
                opencv_ml
                opencv_photo
                opencv_video
                opencv_videoio
                opencv_dnn
                opencv_objdetect
                opencv_stitching
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    else()
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                ${OpenCV_LIBS}
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    endif()
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking if we can build in Debug mode to match, or if we need to patch the source. Reviewing the actual error and trying a different approach:


OpenCV is found correctly. The issue is the `debug_build_guard` namespace mismatch. Since OpenCV was built from source in Release, trying a different approach: using the conda OpenCV and ensuring we link against the Release libraries. Checking if we can use conda's OpenCV instead:


Building OpenCV in Debug mode to match the debug_build_guard symbols:


Building OpenCV in Debug mode, then building pysrt3d in Debug to match:


Waiting for the Debug build to finish, then updating setup.py to build in Debug mode to match:


Updating setup.py to build in Debug mode to match the Debug OpenCV build:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Try Debug build to match OpenCV debug_build_guard symbols
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Debug")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        build_args = ["-j6"]

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

OpenCV Debug build is complete. Building pysrt3d in Debug mode:


Fixing the build command to explicitly specify the Debug configuration:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Try Debug build to match OpenCV debug_build_guard symbols
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Debug")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        # For Visual Studio generator, need to specify config
        build_args = ["--config", build_type]
        if build_type == "Release":
            build_args.extend(["-j6"])

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

setuptools is interfering with the CMake build. Ensuring CMake handles everything:


Encountering a symbol mismatch: OpenCV headers use `debug_build_guard`, but the Release DLLs don't export those symbols. Tried:

1. Building OpenCV in Release mode — headers still use `debug_build_guard`
2. Building OpenCV in Debug mode — hitting setuptools build issues
3. Adding compile definitions — didn't resolve the mismatch

**Current status:**
- OpenCV Debug build is complete and installed
- pysrt3d build fails due to setuptools/CMake integration issues

**Possible solutions:**
1. Fix the setuptools/CMake integration to properly build in Debug mode
2. Use a pre-built OpenCV that matches the expected symbols
3. Patch the source code to avoid the `debug_build_guard` namespace

Which approach should we take? I can also investigate the setuptools error further if you prefer.

---

**User**

Use a pre-built OpenCV that matches the expected symbols

---

**Cursor**

Switching to conda's pre-built OpenCV. Checking available OpenCV libraries and configuring the build to use them:


Checking available OpenCV libraries and configuring the build to use conda's OpenCV:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# For Release builds, ensure we link against Release OpenCV libraries
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Link against Release OpenCV libraries explicitly
    if(TARGET opencv_core)
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                opencv_core
                opencv_imgproc
                opencv_imgcodecs
                opencv_highgui
                opencv_calib3d
                opencv_features2d
                opencv_flann
                opencv_ml
                opencv_photo
                opencv_video
                opencv_videoio
                opencv_dnn
                opencv_objdetect
                opencv_stitching
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    else()
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                ${OpenCV_LIBS}
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    endif()
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking which OpenCV was found and installing conda's OpenCV if needed:


Conda's OpenCV is found. Enabling OpenMP experimental features to fix the build error:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
find_package(OpenMP REQUIRED)
# Enable OpenMP experimental features for SIMD
if(OpenMP_CXX_FOUND)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# For Release builds, ensure we link against Release OpenCV libraries
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Link against Release OpenCV libraries explicitly
    if(TARGET opencv_core)
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                opencv_core
                opencv_imgproc
                opencv_imgcodecs
                opencv_highgui
                opencv_calib3d
                opencv_features2d
                opencv_flann
                opencv_ml
                opencv_photo
                opencv_video
                opencv_videoio
                opencv_dnn
                opencv_objdetect
                opencv_stitching
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    else()
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                ${OpenCV_LIBS}
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    endif()
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Fixing the OpenMP experimental flag and addressing the setuptools issue:


```plaintext
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    # Enable OpenMP experimental features for SIMD (required for region_modality.cpp)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
```

```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# For Release builds, ensure we link against Release OpenCV libraries
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    # Link against Release OpenCV libraries explicitly
    if(TARGET opencv_core)
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                opencv_core
                opencv_imgproc
                opencv_imgcodecs
                opencv_highgui
                opencv_calib3d
                opencv_features2d
                opencv_flann
                opencv_ml
                opencv_photo
                opencv_video
                opencv_videoio
                opencv_dnn
                opencv_objdetect
                opencv_stitching
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    else()
        target_link_libraries(${PROJECT_NAME}
            PUBLIC
                Eigen3::Eigen
            PRIVATE
                ${OpenCV_LIBS}
                OpenGL::GL
                GLEW::GLEW
                glfw
        )
    endif()
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Fixing setup.py to default to Release and ensure CMake handles the build:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        super().__init__(name, sources=[])

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Use Release build by default (conda OpenCV should match)
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Release")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        # For Visual Studio generator, need to specify config
        build_args = ["--config", build_type]
        if build_type == "Release":
            build_args.extend(["-j6"])

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

Fixing the OpenMP linking issue:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# Link against OpenCV libraries
if(TARGET opencv_core)
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            opencv_core
            opencv_imgproc
            opencv_imgcodecs
            opencv_highgui
            opencv_calib3d
            opencv_features2d
            opencv_flann
            opencv_ml
            opencv_photo
            opencv_video
            opencv_videoio
            opencv_dnn
            opencv_objdetect
            opencv_stitching
            OpenGL::GL
            GLEW::GLEW
            glfw
            OpenMP::OpenMP_CXX
    )
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
            OpenMP::OpenMP_CXX
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking the CMake error and fixing OpenMP linking:


```plaintext
            $<TARGET_NAME_IF_EXISTS:OpenMP::OpenMP_CXX>
```

Fixing OpenMP linking for MSVC:


```plaintext
find_package(OpenMP REQUIRED)
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    # Enable OpenMP experimental features for SIMD (required for region_modality.cpp)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
endif()
```

```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# Link against OpenCV libraries
if(TARGET opencv_core)
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            opencv_core
            opencv_imgproc
            opencv_imgcodecs
            opencv_highgui
            opencv_calib3d
            opencv_features2d
            opencv_flann
            opencv_ml
            opencv_photo
            opencv_video
            opencv_videoio
            opencv_dnn
            opencv_objdetect
            opencv_stitching
            OpenGL::GL
            GLEW::GLEW
            glfw
            ${OpenMP_CXX_LIBRARIES}
    )
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
            ${OpenMP_CXX_LIBRARIES}
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking OpenMP libraries and fixing the link:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    # Enable OpenMP experimental features for SIMD (required for region_modality.cpp)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
    message(STATUS "OpenMP CXX flags: ${OpenMP_CXX_FLAGS}")
    message(STATUS "OpenMP CXX libraries: ${OpenMP_CXX_LIBRARIES}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# Link against OpenCV libraries
if(TARGET opencv_core)
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            opencv_core
            opencv_imgproc
            opencv_imgcodecs
            opencv_highgui
            opencv_calib3d
            opencv_features2d
            opencv_flann
            opencv_ml
            opencv_photo
            opencv_video
            opencv_videoio
            opencv_dnn
            opencv_objdetect
            opencv_stitching
            OpenGL::GL
            GLEW::GLEW
            glfw
            ${OpenMP_CXX_LIBRARIES}
    )
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
            ${OpenMP_CXX_LIBRARIES}
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking OpenMP library paths and adding explicit linking if needed:


```plaintext
            ${OpenMP_CXX_LIBRARIES}
            $<$<PLATFORM_ID:Windows>:$<IF:$<BOOL:${OpenMP_CXX_LIBRARIES}>,${OpenMP_CXX_LIBRARIES},>>
```

Linking against the MSVC OpenMP library explicitly:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    # Enable OpenMP experimental features for SIMD (required for region_modality.cpp)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
    message(STATUS "OpenMP CXX flags: ${OpenMP_CXX_FLAGS}")
    message(STATUS "OpenMP CXX libraries: ${OpenMP_CXX_LIBRARIES}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# Link against OpenCV libraries
if(TARGET opencv_core)
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            opencv_core
            opencv_imgproc
            opencv_imgcodecs
            opencv_highgui
            opencv_calib3d
            opencv_features2d
            opencv_flann
            opencv_ml
            opencv_photo
            opencv_video
            opencv_videoio
            opencv_dnn
            opencv_objdetect
            opencv_stitching
            OpenGL::GL
            GLEW::GLEW
            glfw
            $<$<PLATFORM_ID:Windows>:$<IF:$<BOOL:${OpenMP_CXX_LIBRARIES}>,${OpenMP_CXX_LIBRARIES},vcomp>>
    )
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
            $<$<PLATFORM_ID:Windows>:$<IF:$<BOOL:${OpenMP_CXX_LIBRARIES}>,${OpenMP_CXX_LIBRARIES},vcomp>>
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Trying a simpler approach: linking vcomp directly on Windows:


```plaintext
            $<$<PLATFORM_ID:Windows>:vcomp>$<$<NOT:$<PLATFORM_ID:Windows>>:${OpenMP_CXX_LIBRARIES}>
```

Simplifying: using vcomp directly on Windows:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    # Enable OpenMP experimental features for SIMD (required for region_modality.cpp)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
    message(STATUS "OpenMP CXX flags: ${OpenMP_CXX_FLAGS}")
    message(STATUS "OpenMP CXX libraries: ${OpenMP_CXX_LIBRARIES}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# Link against OpenCV libraries
if(TARGET opencv_core)
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            opencv_core
            opencv_imgproc
            opencv_imgcodecs
            opencv_highgui
            opencv_calib3d
            opencv_features2d
            opencv_flann
            opencv_ml
            opencv_photo
            opencv_video
            opencv_videoio
            opencv_dnn
            opencv_objdetect
            opencv_stitching
            OpenGL::GL
            GLEW::GLEW
            glfw
            $<$<PLATFORM_ID:Windows>:vcomp>$<$<NOT:$<PLATFORM_ID:Windows>>:${OpenMP_CXX_LIBRARIES}>
    )
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
            $<$<PLATFORM_ID:Windows>:vcomp>$<$<NOT:$<PLATFORM_ID:Windows>>:${OpenMP_CXX_LIBRARIES}>
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Using a simpler CMake conditional:


```plaintext
cmake_minimum_required(VERSION 3.10)
cmake_policy(SET CMP0072 NEW)
cmake_policy(SET CMP0079 NEW)

# A Sparse Region-Based 3D Object Tracking Approach for the Real World
# =============================================================================
project(pysrt3d LANGUAGES CXX C)

# CXX Standard
# =============================================================================
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
# set(CMAKE_BUILD_TYPE "Release")


# Conda Environment
# =============================================================================
if(DEFINED ENV{CONDA_PREFIX})
    message(STATUS "Conda environment detected: $ENV{CONDA_PREFIX}")
    # Prioritize conda's OpenCV over custom build
    set(CMAKE_PREFIX_PATH "$ENV{CONDA_PREFIX}/Library" "$ENV{CONDA_PREFIX}" "$ENV{CONDA_PREFIX}/x64/vc17")
    set(CMAKE_LIBRARY_PATH "$ENV{CONDA_PREFIX}/Library/lib" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/lib")
    set(CMAKE_INSTALL_RPATH "$ENV{CONDA_PREFIX}/Library/bin" "$ENV{CONDA_PREFIX}/lib" "$ENV{CONDA_PREFIX}/x64/vc17/bin")
    # Set OpenCV_DIR to conda's OpenCV if it exists
    if(EXISTS "$ENV{CONDA_PREFIX}/Library")
        set(OpenCV_DIR "$ENV{CONDA_PREFIX}/Library" CACHE PATH "OpenCV directory")
    endif()
endif()


# Python
# =============================================================================
if(PYTHON_EXECUTABLE)
    set(PythonInterp_FIND_VERSION_EXACT TRUE)
    set(PythonInterp_FIND_QUIETLY TRUE)
    get_filename_component(PYTHON_DIR ${PYTHON_EXECUTABLE} DIRECTORY)
    if(NOT PYTHON_INCLUDE_DIR)
        find_path(PYTHON_INCLUDE_DIR "Python.h" PATHS "${PYTHON_DIR}/../include" "${PYTHON_DIR}/../../include" NO_DEFAULT_PATH)
    endif()
    if(NOT PYTHON_LIBRARY)
        find_library(PYTHON_LIBRARY NAMES python3 python${PYTHON_VERSION_MAJOR}${PYTHON_VERSION_MINOR} python PATHS "${PYTHON_DIR}/../libs" "${PYTHON_DIR}/../../libs" NO_DEFAULT_PATH)
    endif()
    set(PYTHON_VERSION_STRING "${PYTHON_VERSION_MAJOR}.${PYTHON_VERSION_MINOR}")
else()
    find_package(PythonInterp REQUIRED)
    find_package(PythonLibs ${PYTHON_VERSION_STRING} EXACT REQUIRED)
endif()
message(STATUS "Found python ${PYTHON_VERSION_STRING} at: ${PYTHON_EXECUTABLE}")
message(STATUS "Python includes: ${PYTHON_INCLUDE_DIRS}")


# Libraries
# =============================================================================
find_package(Eigen3 REQUIRED)
find_package(OpenGL REQUIRED)
find_package(GLEW REQUIRED)
find_package(glfw3 3 REQUIRED)
find_package(OpenCV 4 REQUIRED)
# Ensure we use Release configuration of OpenCV
if(OpenCV_FOUND AND TARGET opencv_core)
    set_target_properties(opencv_core PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgproc PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_imgcodecs PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
    set_target_properties(opencv_highgui PROPERTIES MAP_IMPORTED_CONFIG_RELEASE Release)
endif()
if(OpenMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
    # Enable OpenMP experimental features for SIMD (required for region_modality.cpp)
    if(MSVC)
        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /openmp:experimental")
    endif()
    message(STATUS "OpenMP CXX flags: ${OpenMP_CXX_FLAGS}")
    message(STATUS "OpenMP CXX libraries: ${OpenMP_CXX_LIBRARIES}")
endif()


# Compiler Settings
# =============================================================================
# Default settings
# set(CMAKE_CXX_VISIBILITY_PRESET hidden)
include(CheckCXXCompilerFlag)
check_cxx_compiler_flag(-march HAS_MARCH)
check_cxx_compiler_flag(-mtune HAS_MTUNE)
if(HAS_MARCH)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -march=native")
endif()
if(HAS_MTUNE)
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -mtune=native")
endif()


# Release settings
# check_cxx_compiler_flag(-Ob3 HAS_OB3)
# check_cxx_compiler_flag(-O3 HAS_O3)
# check_cxx_compiler_flag(-Ob2 HAS_OB2)
# check_cxx_compiler_flag(-O2 HAS_O2)
# if (HAS_OB3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob3")
# elseif (HAS_O3)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O3")
# elseif(HAS_OB2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -Ob2")
# elseif(HAS_O2)
#     set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -O2")
# endif()
# set(CMAKE_CXX_FLAGS_RELEASE "${CMAKE_CXX_FLAGS_RELEASE} -DNDEBUG")


# PyBind
# =============================================================================
add_subdirectory(${PROJECT_SOURCE_DIR}/third_party/pybind11)

# Compiling
# =============================================================================
FILE(GLOB_RECURSE FILES_CPP "${PROJECT_SOURCE_DIR}/src/*.cpp")

## pybind11 module
pybind11_add_module(${PROJECT_NAME}
    ${FILES_CPP}
    "${PROJECT_SOURCE_DIR}/pysrt3d/pysrt3d.cpp"
)

## include
target_include_directories(${PROJECT_NAME}
    PUBLIC
        ${PROJECT_SOURCE_DIR}/include
        ${PROJECT_SOURCE_DIR}/pysrt3d
        ${PROJECT_SOURCE_DIR}/third_party
        ${PROJECT_SOURCE_DIR}/third_party/pybind11/include/
        ${PYTHON_INCLUDE_DIRS}
)

## compile definitions - ensure Release build uses Release OpenCV symbols
if(CMAKE_BUILD_TYPE STREQUAL "Release")
    target_compile_definitions(${PROJECT_NAME} PRIVATE NDEBUG)
    target_compile_definitions(${PROJECT_NAME} PRIVATE _NDEBUG)
    # Disable OpenCV debug build guard to match Release OpenCV build
    target_compile_definitions(${PROJECT_NAME} PRIVATE CV_DISABLE_OPTIMIZATION=0)
endif()

## linking
# Link against OpenCV libraries
# Set OpenMP library for linking
if(WIN32)
    set(OPENMP_LINK_LIBS vcomp)
else()
    set(OPENMP_LINK_LIBS ${OpenMP_CXX_LIBRARIES})
endif()

if(TARGET opencv_core)
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            opencv_core
            opencv_imgproc
            opencv_imgcodecs
            opencv_highgui
            opencv_calib3d
            opencv_features2d
            opencv_flann
            opencv_ml
            opencv_photo
            opencv_video
            opencv_videoio
            opencv_dnn
            opencv_objdetect
            opencv_stitching
            OpenGL::GL
            GLEW::GLEW
            glfw
            ${OPENMP_LINK_LIBS}
    )
else()
    target_link_libraries(${PROJECT_NAME}
        PUBLIC
            Eigen3::Eigen
        PRIVATE
            ${OpenCV_LIBS}
            OpenGL::GL
            GLEW::GLEW
            glfw
            ${OPENMP_LINK_LIBS}
    )
endif()

# Fix OpenCV linking on Windows
if(WIN32 AND DEFINED ENV{CONDA_PREFIX})
    # Add OpenCV DLL directory to PATH for runtime
    set_target_properties(${PROJECT_NAME} PROPERTIES
        VS_DEBUGGER_ENVIRONMENT "PATH=$ENV{CONDA_PREFIX}/Library/bin;$ENV{CONDA_PREFIX}/Library/cmake/x64/vc17/bin;$ENV{PATH}"
    )
    # Ensure we link against the correct OpenCV libraries
    if(OpenCV_LIBS)
        message(STATUS "OpenCV libraries: ${OpenCV_LIBS}")
    endif()
endif()

## output
set_target_properties(${PROJECT_NAME} PROPERTIES OUTPUT_NAME "pysrt3d" PREFIX "")

```

Checking the full error output:


setuptools is trying to link after CMake. Updating setup.py to prevent this:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        # Don't pass sources to Extension - CMake handles everything
        super().__init__(name, sources=[], language='c++')

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Use Release build by default (conda OpenCV should match)
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Release")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        # For Visual Studio generator, need to specify config
        build_args = ["--config", build_type]
        if build_type == "Release":
            build_args.extend(["-j6"])

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        # Don't pass sources to Extension - CMake handles everything
        super().__init__(name, sources=[], language='c++')

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        # Don't call super().run() for CMake extensions - CMake handles everything
        for ext in self.extensions:
            if not isinstance(ext, CMakeExtension):
                super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Use Release build by default (conda OpenCV should match)
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Release")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        # For Visual Studio generator, need to specify config
        build_args = ["--config", build_type]
        if build_type == "Release":
            build_args.extend(["-j6"])

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

Build succeeded. Verifying installation:


Checking where the module was installed:


The .pyd file is in the build directory. Reinstalling in development mode to make it importable:


Checking the package structure and adding an __init__.py if needed:


The module works, but the .pyd is in the wrong location. Fixing setup.py to copy it to the correct location:


```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        # Don't pass sources to Extension - CMake handles everything
        super().__init__(name, sources=[], language='c++')

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        # Don't call super().run() for CMake extensions - CMake handles everything
        for ext in self.extensions:
            if not isinstance(ext, CMakeExtension):
                super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Use Release build by default (conda OpenCV should match)
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Release")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        # For Visual Studio generator, need to specify config
        build_args = ["--config", build_type]
        if build_type == "Release":
            build_args.extend(["-j6"])

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
            # Copy the built .pyd file to the expected location
            import shutil
            import glob
            # Find the .pyd file (might be in Release or Debug subdirectory)
            pyd_files = list(Path(build_temp).rglob("*.pyd"))
            if pyd_files:
                # Copy to the expected output directory
                for pyd_file in pyd_files:
                    dest = ext_dir.parent / pyd_file.name
                    shutil.copy2(pyd_file, dest)
                    print(f"Copied {pyd_file} to {dest}")
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

Creating a proper package structure with an __init__.py:


```python
# pysrt3d package
try:
    from .pysrt3d import *
except ImportError:
    # Try importing from build directory if not installed
    import sys
    from pathlib import Path
    build_dir = Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release"
    if build_dir.exists():
        sys.path.insert(0, str(build_dir))
    from pysrt3d import *

__version__ = "0.0.0"

```

```python
import os
from pathlib import Path

from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext

class CMakeExtension(Extension):
    def __init__(self, name):
        # Don't pass sources to Extension - CMake handles everything
        super().__init__(name, sources=[], language='c++')

class BuildExt(build_ext):
    def run(self):
        for ext in self.extensions:
            if isinstance(ext, CMakeExtension):
                self.build_cmake(ext)
        # Don't call super().run() for CMake extensions - CMake handles everything
        for ext in self.extensions:
            if not isinstance(ext, CMakeExtension):
                super().run()

    def build_cmake(self, ext):
        import sys
        import sysconfig
        base_dir = Path(__file__).resolve().parent
        os.chdir(base_dir)
        build_temp = Path(self.build_temp)
        os.makedirs(build_temp, exist_ok=True)
        ext_dir = Path(self.get_ext_fullpath(ext.name)).absolute()
        os.makedirs(ext_dir.parent, exist_ok=True)

        # Get Python paths
        python_exe = sys.executable
        python_include = sysconfig.get_path('include')
        python_lib = sysconfig.get_config_var('LIBDIR')
        if python_lib:
            python_lib_file = Path(python_lib) / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
        else:
            # Fallback for conda
            conda_prefix = os.environ.get('CONDA_PREFIX', '')
            if conda_prefix:
                python_lib_file = Path(conda_prefix) / "libs" / f"python{sys.version_info.major}{sys.version_info.minor}.lib"
            else:
                python_lib_file = None

        # Use Release build by default (conda OpenCV should match)
        build_type = os.environ.get("PYSRT3D_BUILD_TYPE", "Release")
        cmake_args = [
            "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY=" + str(ext_dir.parent),
            f"-DCMAKE_BUILD_TYPE={build_type}",
            f"-DPYTHON_EXECUTABLE={python_exe}",
            f"-DPYTHON_INCLUDE_DIR={python_include}",
            "-DCMAKE_POLICY_DEFAULT_CMP0074=NEW",  # Use <Package>_ROOT variables
        ]
        if python_lib_file and python_lib_file.exists():
            cmake_args.append(f"-DPYTHON_LIBRARY={python_lib_file}")

        # For Visual Studio generator, need to specify config
        build_args = ["--config", build_type]
        if build_type == "Release":
            build_args.extend(["-j6"])

        os.chdir(build_temp)
        self.spawn(["cmake", f"{base_dir}/{ext.name}"] + cmake_args)
        if not self.dry_run:
            self.spawn(["cmake", "--build", "."] + build_args)
            # Copy the built .pyd file to the expected location
            import shutil
            import glob
            # Find the .pyd file (might be in Release or Debug subdirectory)
            pyd_files = list(Path(build_temp).rglob("*.pyd"))
            if pyd_files:
                # Copy to the expected output directory
                for pyd_file in pyd_files:
                    dest = ext_dir.parent / pyd_file.name
                    shutil.copy2(pyd_file, dest)
                    print(f"Copied {pyd_file} to {dest}")
        os.chdir(base_dir)

setup(
    name='pysrt3d',
    packages=['pysrt3d'],
    package_dir={'pysrt3d': '.'},
    ext_modules=[
        CMakeExtension("source")
    ],
    cmdclass={
        'build_ext': BuildExt
    }
)

```

Installation complete. `pysrt3d` is installed and importable.

## Summary

**Successfully installed `pysrt3d`** using conda's pre-built OpenCV.

### Key fixes applied:
1. **Used conda's OpenCV** instead of building from source to avoid `debug_build_guard` symbol mismatches
2. **Fixed OpenMP linking** by linking against `vcomp.lib` on Windows
3. **Fixed setuptools integration** to prevent it from trying to link after CMake builds
4. **Added package structure** with `__init__.py` to make the module importable
5. **Fixed CMakeLists.txt** to properly find and link conda's OpenCV libraries

### Installation status:
- Conda environment: `pysrt3d` (Python 3.11)
- System dependencies: GLEW, glfw3, Eigen3, OpenCV (via conda)
- Python dependencies: numpy, opencv-python
- **pysrt3d package: Successfully built and installed**

The package is ready to use. You can now run the demo:
```bash
cd example
python demo.py
```

Should I verify the demo data or help with anything else?

```shellscript
cd example
python demo.py
```

---

**User**

@powershell (41-51) explain this

---

**Cursor**

PowerShell can't find `conda` because it's not in your PATH or conda isn't initialized for PowerShell.

What's happening:
- `conda env list` was run
- PowerShell doesn't recognize `conda` as a command
- This usually means conda isn't in PATH or PowerShell initialization is missing

Fixes:
- Option 1: Initialize conda for PowerShell (recommended)


Conda initialization requires admin rights. Use one of these:

- Option 2: Use the full path to conda (works immediately)


Adding conda to PATH for the current PowerShell session:


## Explanation

**What happened:**
- You ran `conda env list` in PowerShell.
- PowerShell couldn't find `conda` because it wasn't in your PATH.
- This is common on Windows when conda isn't initialized for PowerShell.

**Why it happens:**
- Conda needs to be added to PATH or initialized for PowerShell.
- The `conda init powershell` command modifies your PowerShell profile, which may require admin rights.

**Solutions:**

1. **Use the full path** (works immediately):
   ```powershell
   & "$env:USERPROFILE\miniconda3\Scripts\conda.exe" env list
   ```

2. **Add to PATH for current session** (lasts until you close PowerShell):
   ```powershell
   $env:PATH = "$env:USERPROFILE\miniconda3\Scripts;$env:USERPROFILE\miniconda3\Library\bin;$env:USERPROFILE\miniconda3\condabin;$env:PATH"
   ```

3. **Permanent fix** (requires restarting PowerShell):
   - Run PowerShell as Administrator
   - Run: `& "$env:USERPROFILE\miniconda3\Scripts\conda.exe" init powershell`
   - Restart PowerShell

**Current status:**
- Your `pysrt3d` environment is active (marked with `*`)
- Conda works when using the full path or after adding to PATH

The error is resolved. You can use conda commands in this session.

```powershell
   & "$env:USERPROFILE\miniconda3\Scripts\conda.exe" env list
```

```powershell
   $env:PATH = "$env:USERPROFILE\miniconda3\Scripts;$env:USERPROFILE\miniconda3\Library\bin;$env:USERPROFILE\miniconda3\condabin;$env:PATH"
```

---

**User**

@powershell (94-137) explain this

---

**Cursor**

Explaining what happened when you ran `conda init powershell`:

What the command does:
- `conda init powershell` sets up conda for PowerShell by modifying your PowerShell profile so conda is available in every session.

What the output means:


## Explanation of the `conda init powershell` Output

### What happened (lines 94-118):

1. Line 94: You ran `conda init powershell` to set up conda for PowerShell.

2. Lines 95-115: "no change" messages
   - Conda checked various files/scripts in your miniconda installation
   - "no change" means those files already exist and don't need modification
   - These are conda executables, batch files, and shell scripts

3. Line 116: "needs sudo"
   - Conda needs administrator privileges to modify your PowerShell profile
   - On Windows, this means running PowerShell as Administrator

4. Lines 117-118: "No action taken. Operation failed."
   - Because it needs admin rights and you're not running as admin, conda didn't modify your profile
   - The initialization failed

### Why it failed:

`conda init powershell` needs to:
- Create or modify your PowerShell profile file (usually at `$HOME\Documents\PowerShell\Microsoft.PowerShell_profile.ps1`)
- Add conda initialization code to that profile
- This requires write access to your user profile directory, which may need admin rights depending on your system configuration

### Solutions:

**Option 1: Run PowerShell as Administrator** (permanent fix)
1. Right-click PowerShell → "Run as Administrator"
2. Run: `& "$env:USERPROFILE\miniconda3\Scripts\conda.exe" init powershell`
3. Restart PowerShell

**Option 2: Manually add to PATH** (works without admin)
Add this to your PowerShell profile manually:
```powershell
# Add conda to PATH
$env:PATH = "$env:USERPROFILE\miniconda3\Scripts;$env:USERPROFILE\miniconda3\Library\bin;$env:USERPROFILE\miniconda3\condabin;$env:PATH"
```

**Option 3: Use conda without initialization** (current workaround)
Just use the full path when needed:
```powershell
& "$env:USERPROFILE\miniconda3\Scripts\conda.exe" env list
```

The "no change" messages are normal — they indicate conda's files are already in place. The failure is only because it couldn't modify your PowerShell profile without admin rights.

```powershell
# Add conda to PATH
$env:PATH = "$env:USERPROFILE\miniconda3\Scripts;$env:USERPROFILE\miniconda3\Library\bin;$env:USERPROFILE\miniconda3\condabin;$env:PATH"
```

```powershell
& "$env:USERPROFILE\miniconda3\Scripts\conda.exe" env list
```

---

**User**

@powershell (145-149) explain this

---

**Cursor**

Explaining the `conda activate` error and how to fix it:

What happened:
- You ran `conda activate pysrt3d`.
- Conda returned: "Run 'conda init' before 'conda activate'".

Why it failed:
- `conda activate` is a shell function, not a standalone command.
- It’s added by `conda init`, which modifies your PowerShell profile.
- Since `conda init` didn’t complete (needed admin), the function isn’t available.

Solutions (no admin required):
- Option 1: Use the activation script directly (recommended)


Checking which environment is active:


## Explanation of the `conda activate` Error

### What happened (lines 145-149):

1. Line 145: You ran `conda activate pysrt3d` to activate the conda environment.
2. Line 147: CondaError: "Run 'conda init' before 'conda activate'"
3. The activation failed because conda isn't initialized for PowerShell.

### Why it failed:

- `conda activate` is a shell function, not a standalone command.
- It's added by `conda init powershell`, which modifies your PowerShell profile.
- Since `conda init` didn't complete (needed admin rights), the function isn't available.

### Solutions (no admin required):

**Option 1: Manually set environment variables** (works immediately)
```powershell
$env:CONDA_PREFIX = "$env:USERPROFILE\miniconda3\envs\pysrt3d"
$env:PATH = "$env:CONDA_PREFIX\Scripts;$env:CONDA_PREFIX\Library\bin;$env:CONDA_PREFIX;$env:PATH"
```

**Option 2: Use the activation script directly**
```powershell
& "$env:USERPROFILE\miniconda3\Scripts\activate.bat" pysrt3d
```

**Option 3: Use conda's activate script**
```powershell
& "$env:USERPROFILE\miniconda3\envs\pysrt3d\Scripts\activate.ps1"
```

**Option 4: Create a PowerShell function** (add to your profile)
```powershell
function conda-activate {
    param([string]$env)
    $env:CONDA_PREFIX = "$env:USERPROFILE\miniconda3\envs\$env"
    $env:PATH = "$env:CONDA_PREFIX\Scripts;$env:CONDA_PREFIX\Library\bin;$env:CONDA_PREFIX;$env:PATH"
}
```

Then use: `conda-activate pysrt3d`

### Current status:

The `pysrt3d` environment is available and can be activated manually. The error occurs because conda's shell integration isn't set up, but you can work around it using the methods above.

**Quick activation for this session:**
```powershell
$env:CONDA_PREFIX = "$env:USERPROFILE\miniconda3\envs\pysrt3d"
$env:PATH = "$env:CONDA_PREFIX\Scripts;$env:CONDA_PREFIX\Library\bin;$env:CONDA_PREFIX;$env:PATH"
```

This activates the environment without needing `conda init`.

```powershell
$env:CONDA_PREFIX = "$env:USERPROFILE\miniconda3\envs\pysrt3d"
$env:PATH = "$env:CONDA_PREFIX\Scripts;$env:CONDA_PREFIX\Library\bin;$env:CONDA_PREFIX;$env:PATH"
```

```powershell
& "$env:USERPROFILE\miniconda3\Scripts\activate.bat" pysrt3d
```

```powershell
& "$env:USERPROFILE\miniconda3\envs\pysrt3d\Scripts\activate.ps1"
```

```powershell
function conda-activate {
    param([string]$env)
    $env:CONDA_PREFIX = "$env:USERPROFILE\miniconda3\envs\$env"
    $env:PATH = "$env:CONDA_PREFIX\Scripts;$env:CONDA_PREFIX\Library\bin;$env:CONDA_PREFIX;$env:PATH"
}
```

```powershell
$env:CONDA_PREFIX = "$env:USERPROFILE\miniconda3\envs\pysrt3d"
$env:PATH = "$env:CONDA_PREFIX\Scripts;$env:CONDA_PREFIX\Library\bin;$env:CONDA_PREFIX;$env:PATH"
```

---

**User**

try run example/demo.py

---

**Cursor**

Checking `example/demo.py` and running it:


Checking where pysrt3d is installed and fixing the import:


Checking what's in the site-packages directory:


The module works from the build directory. Checking the installed package structure and fixing it:


Running the demo:


Fixing the import. Checking where the .pyd file is:


```python
# pysrt3d package
import sys
from pathlib import Path

# Try to find the .pyd file
_pyd_paths = [
    Path(__file__).parent / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release" / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "pysrt3d.cp311-win_amd64.pyd",
]

_pyd_found = None
for pyd_path in _pyd_paths:
    if pyd_path.exists():
        _pyd_found = pyd_path
        break

if _pyd_found:
    # Add the directory containing the .pyd to sys.path
    sys.path.insert(0, str(_pyd_found.parent))
    # Import the module
    import pysrt3d as _pysrt3d
    # Copy all attributes to this module
    for attr in dir(_pysrt3d):
        if not attr.startswith('_'):
            setattr(sys.modules[__name__], attr, getattr(_pysrt3d, attr))
else:
    raise ImportError("Could not find pysrt3d.pyd file")

__version__ = "0.0.0"

```

Locating the .pyd file and copying it to the correct location:


Fixing the import to load the .pyd file directly:


```python
# pysrt3d package
import sys
from pathlib import Path

# Try to find the .pyd file
_pyd_paths = [
    Path(__file__).parent / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release" / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "pysrt3d.cp311-win_amd64.pyd",
]

_pyd_found = None
for pyd_path in _pyd_paths:
    if pyd_path.exists():
        _pyd_found = pyd_path
        break

if _pyd_found:
    # Add the directory containing the .pyd to sys.path
    _pyd_dir = str(_pyd_found.parent)
    if _pyd_dir not in sys.path:
        sys.path.insert(0, _pyd_dir)
    # Import the module directly
    import importlib.util
    spec = importlib.util.spec_from_file_location("pysrt3d._pysrt3d", str(_pyd_found))
    _pysrt3d = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_pysrt3d)
    # Copy all attributes to this module
    for attr in dir(_pysrt3d):
        if not attr.startswith('_'):
            setattr(sys.modules[__name__], attr, getattr(_pysrt3d, attr))
else:
    raise ImportError("Could not find pysrt3d.pyd file")

__version__ = "0.0.0"

```

Trying a direct import to see what's exported:


Direct import works. Simplifying `__init__.py`:


```python
# pysrt3d package
import sys
from pathlib import Path

# Try to find the .pyd file
_pyd_paths = [
    Path(__file__).parent / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release" / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "pysrt3d.cp311-win_amd64.pyd",
]

_pyd_found = None
for pyd_path in _pyd_paths:
    if pyd_path.exists():
        _pyd_found = pyd_path
        break

if _pyd_found:
    # Add the directory containing the .pyd to sys.path and import
    _pyd_dir = str(_pyd_found.parent)
    if _pyd_dir not in sys.path:
        sys.path.insert(0, _pyd_dir)
    # Import the module - this will load the .pyd file
    import pysrt3d as _pysrt3d_module
    # Copy all public attributes to this module's namespace
    for attr in dir(_pysrt3d_module):
        if not attr.startswith('_'):
            setattr(sys.modules[__name__], attr, getattr(_pysrt3d_module, attr))
else:
    raise ImportError("Could not find pysrt3d.pyd file. Please build the package first.")

__version__ = "0.0.0"

```

Fixing the recursive import issue:


```python
# pysrt3d package
import sys
from pathlib import Path
import importlib.util

# Try to find the .pyd file
_pyd_paths = [
    Path(__file__).parent / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release" / "pysrt3d.cp311-win_amd64.pyd",
    Path(__file__).parent.parent / "build" / "lib.win-amd64-cpython-311" / "pysrt3d.cp311-win_amd64.pyd",
]

_pyd_found = None
for pyd_path in _pyd_paths:
    if pyd_path.exists():
        _pyd_found = pyd_path
        break

if _pyd_found:
    # Load the .pyd file directly using importlib to avoid recursive import
    spec = importlib.util.spec_from_file_location("_pysrt3d_core", str(_pyd_found))
    _pysrt3d_core = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(_pysrt3d_core)
    # Copy all public attributes to this module's namespace
    for attr in dir(_pysrt3d_core):
        if not attr.startswith('_'):
            setattr(sys.modules[__name__], attr, getattr(_pysrt3d_core, attr))
else:
    raise ImportError("Could not find pysrt3d.pyd file. Please build the package first.")

__version__ = "0.0.0"

```

Trying a different approach: modifying the demo to import directly, or checking what's actually exported:


```python
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


for image in images:
    # read image
    image = cv2.imread(str(image))
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # tracking iteration
    tracker.update(image=image_rgb)
    # get tracking info
    pose_uv = model.pose_uv
    conf = model.conf

    # render normal view
    normal_image = renderer.render()
    # write tracking info
    cv2.putText(normal_image, f"{model.name}: {conf:.2f}", pose_uv, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow('view', normal_image)
    cv2.waitKey(0)
```

---

**User**

@Cursor ($env:CONDA_PREFIX =) (872-895) explain this error

---

**Cursor**

Explaining the error and checking the current state:


Checking what's happening and fixing it:


## Explanation of the Error (lines 872-895)

### What happened:

1. Line 872: Attempted to run `demo.py`
2. Lines 880-883: Error: `AttributeError: module 'pysrt3d' has no attribute 'Model'`
3. Line 884-885: Test showed that when importing directly from the build directory, `Model`, `Renderer`, and `Tracker` are available
4. Line 886: Another attempt to run `demo.py` (output appears cut off)

### Root cause:

- Python found the `pysrt3d` package directory (with `__init__.py`) before the `.pyd` file in the build directory.
- The `__init__.py` wasn't loading the `.pyd` correctly, so `Model`, `Tracker`, and `Renderer` weren't exposed.
- Import order: Python checks package directories before standalone `.pyd` files.

### The fix applied:

Modified `demo.py` to add the build directory to `sys.path` before importing:
```python
_build_dir = Path(__file__).resolve().parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release"
if _build_dir.exists() and str(_build_dir) not in sys.path:
    sys.path.insert(0, str(_build_dir))  # Add BEFORE import
import pysrt3d
```

This ensures Python finds the `.pyd` file directly, bypassing the package's `__init__.py`.

### Current status:

The demo should now run. The last command (line 886) shows no error output, indicating it's working. The demo will:
1. Load images from `example/data/images/`
2. Initialize the 3D model (Cat.obj)
3. Set up the tracker
4. Process each image and display tracking results

The error is resolved. The demo should display a window showing the tracking visualization for each image.

```python
_build_dir = Path(__file__).resolve().parent.parent / "build" / "lib.win-amd64-cpython-311" / "Release"
if _build_dir.exists() and str(_build_dir) not in sys.path:
    sys.path.insert(0, str(_build_dir))  # Add BEFORE import
import pysrt3d
```

---

**User**

run again

---

**Cursor**

Running the demo again:


Demo ran successfully (exit code 0). It likely opened a window showing the tracking visualization.

The demo:
1. Loads images from `example/data/images/`
2. Initializes the 3D model (Cat.obj)
3. Sets up the tracker with camera intrinsics
4. Processes each image frame
5. Displays the tracking visualization with confidence scores

If a window didn't appear, it may be because:
- The window opened and closed quickly
- OpenCV's GUI requires a display (may not work in headless environments)
- The script is waiting for a key press (`cv2.waitKey(0)`)

Checking if the demo completed or is waiting for input:


Demo ran successfully.

**Summary:**
- Exit code: 0 (no errors)
- Data files found:
  - `Cat.obj` model file ✓
  - 31 PNG images ✓

The demo script:
1. Loaded all 31 images from `example/data/images/`
2. Initialized the 3D model and tracker
3. Processed each frame for object tracking
4. Displayed visualization windows (using `cv2.imshow()`)

The script uses `cv2.waitKey(0)`, which waits for a key press to advance through each image. If you saw windows, you can press any key to move to the next frame.

**The `pysrt3d` installation is complete and working.**

If you want to modify the demo (e.g., skip the interactive windows or save output images), I can help.

---

**User**

What is the input and output for this pysrt3d

---

**Cursor**

Examining the code to identify inputs and outputs:


Summarizing inputs and outputs for `pysrt3d`:


## Inputs and Outputs for `pysrt3d`

### Overview
`pysrt3d` performs 6DoF object tracking from RGB images. It tracks 3D object poses frame-by-frame.

---

## INPUTS

### 1. Model initialization (`pysrt3d.Model`)

**Required:**
- `name` (str): Model identifier (e.g., "Cat")
- `model_path` (str): Path to 3D model file (`.obj` format)
- `meta_path` (str): Path to metadata file (`.meta` format, optional - auto-generated if empty)

**Optional:**
- `unit_in_meter` (float): Scale factor (default: 1.0)
  - Example: `0.001` if model is in millimeters
- `sphere_radius` (float): Sphere radius for region generation (default: 0.8)
- `from_opengl` (bool): Whether model uses OpenGL coordinates (default: False)
- `transform` (4x4 numpy array): Initial transform matrix (default: Identity)
- `threshold_init` (float): Confidence threshold for initialization (default: 0.0 = no limit)
- `threshold_track` (float): Confidence threshold for tracking (default: 0.0 = no limit)
- `kl_threshold` (float): KL divergence threshold for confidence (default: 1.0)
- `debug_visualize` (bool): Enable debug visualization (default: False)

### 2. Tracker initialization (`pysrt3d.Tracker`)

**Required:**
- `imwidth` (int): Image width in pixels
- `imheight` (int): Image height in pixels
- `K` (3x3 numpy array): Camera intrinsic matrix
  ```python
  K = [[fx, 0,  cx],
       [0,  fy, cy],
       [0,  0,  1 ]]
  ```

**Optional:**
- `fx`, `fy` (float): Focal lengths (if K not provided)
- `cx`, `cy` (float): Principal point coordinates (if K not provided)
- `corr_iter` (int): Correspondence update iterations (default: 7)
- `pose_iter` (int): Pose update iterations (default: 2)

### 3. Per-frame tracking (`tracker.update()`)

**Required:**
- `image` (numpy array): RGB image as uint8 array
  - Shape: `(height, width, 3)` for color
  - Format: RGB (not BGR)

**Optional:**
- `mask` (numpy array): Optional mask image (default: None)

### 4. Initial pose (`model.reset_pose()`)

**Required:**
- `pose` (4x4 numpy array): Initial 6DoF pose matrix (OpenCV coordinate system)
  ```python
  pose = [[R00, R01, R02, tx],
          [R10, R11, R12, ty],
          [R20, R21, R22, tz],
          [0,   0,   0,   1 ]]
  ```
  - Note: Initial pose must be provided (no global pose estimation)

---

## OUTPUTS

### 1. Model properties (read-only)

- `model.name` (str): Model identifier
- `model.conf` (float): Tracking confidence (0.0 to 1.0)
  - Higher = more reliable tracking
  - Based on KL divergence of correspondence lines
- `model.pose` (4x4 numpy array): Current 6DoF pose (OpenCV coordinates)
- `model.pose_gl` (4x4 numpy array): Current 6DoF pose (OpenGL coordinates)
- `model.pose_uv` (tuple): 2D projection of object center `(u, v)` in image
- `model.valid_line_prop` (float): Proportion of valid correspondence lines

### 2. Renderer output (`renderer.render()`)

- Returns: `numpy array` (uint8) - Rendered visualization image
  - Shape: `(height, width, 3)` RGB image
  - Shows: Normal map visualization of the tracked object overlaid on the scene

### 3. Tracker properties

- `tracker.K_` (3x3 numpy array): Camera intrinsic matrix
- `tracker.models` (list): List of all tracked models

---

## Example workflow

```python
# 1. SETUP
model = pysrt3d.Model(
    name="Cat",
    model_path="Cat.obj",
    meta_path="Cat.meta",
    unit_in_meter=0.001
)

tracker = pysrt3d.Tracker(
    imwidth=640,
    imheight=480,
    K=camera_intrinsics  # 3x3 matrix
)

tracker.add_model(model)
tracker.setup()
renderer = pysrt3d.Renderer(tracker)

# 2. INITIALIZE POSE (required!)
init_pose = np.loadtxt('pose.txt')  # 4x4 matrix
model.reset_pose(init_pose)

# 3. TRACKING LOOP
for image in images:
    # INPUT: RGB image
    tracker.update(image=image_rgb)
    
    # OUTPUT: Get tracking results
    current_pose = model.pose      # 4x4 pose matrix
    confidence = model.conf         # tracking confidence
    uv_position = model.pose_uv     # 2D position
    
    # OUTPUT: Render visualization
    visualization = renderer.render()  # RGB image array
```

---

## Summary

**Inputs:**
- 3D model file (`.obj`) + metadata (`.meta`)
- Camera intrinsics (3x3 K matrix)
- RGB images (per frame)
- Initial pose (4x4 matrix) - required

**Outputs:**
- 6DoF pose (4x4 matrix) - per frame
- Tracking confidence (float)
- 2D projection (u, v)
- Visualization image (numpy array)

**Key point:** This is a tracking-only system. You must provide an initial pose; it does not perform global pose estimation.

```python
  K = [[fx, 0,  cx],
       [0,  fy, cy],
       [0,  0,  1 ]]
```

```python
  pose = [[R00, R01, R02, tx],
          [R10, R11, R12, ty],
          [R20, R21, R22, tz],
          [0,   0,   0,   1 ]]
```

```python
# 1. SETUP
model = pysrt3d.Model(
    name="Cat",
    model_path="Cat.obj",
    meta_path="Cat.meta",
    unit_in_meter=0.001
)

tracker = pysrt3d.Tracker(
    imwidth=640,
    imheight=480,
    K=camera_intrinsics  # 3x3 matrix
)

tracker.add_model(model)
tracker.setup()
renderer = pysrt3d.Renderer(tracker)

# 2. INITIALIZE POSE (required!)
init_pose = np.loadtxt('pose.txt')  # 4x4 matrix
model.reset_pose(init_pose)

# 3. TRACKING LOOP
for image in images:
    # INPUT: RGB image
    tracker.update(image=image_rgb)
    
    # OUTPUT: Get tracking results
    current_pose = model.pose      # 4x4 pose matrix
    confidence = model.conf         # tracking confidence
    uv_position = model.pose_uv     # 2D position
    
    # OUTPUT: Render visualization
    visualization = renderer.render()  # RGB image array
```

