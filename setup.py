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
