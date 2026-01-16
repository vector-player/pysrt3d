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
