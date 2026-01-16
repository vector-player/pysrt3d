@echo off
REM Batch script to run demo.py with conda environment
REM Usage: run_demo.bat [env_name]

setlocal
set ENV_NAME=%1
if "%ENV_NAME%"=="" set ENV_NAME=pysrt3d

REM Check if conda is available
where conda >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: conda is not found in PATH. Please install Anaconda/Miniconda first.
    exit /b 1
)

REM Initialize conda
call conda init cmd.exe >nul 2>&1

REM Check if environment exists, if not create it
conda env list | findstr /R /C:"^%ENV_NAME% " >nul
if %ERRORLEVEL% NEQ 0 (
    echo Creating conda environment: %ENV_NAME%
    conda create -n %ENV_NAME% python=3.11 -y
)

REM Activate the environment
echo Activating conda environment: %ENV_NAME%
call conda activate %ENV_NAME%

REM Install dependencies
echo Installing dependencies...
conda install -y glew glfw eigen libopencv
pip install numpy opencv-python

REM Install pysrt3d package if not already installed
echo Installing pysrt3d package...
cd /d %~dp0
pip install -e .

REM Run the demo
echo Running demo.py...
cd example
python demo.py

endlocal
