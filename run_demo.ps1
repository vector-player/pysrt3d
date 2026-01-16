# PowerShell script to run demo.py with conda environment
# Usage: .\run_demo.ps1 [env_name]

param(
    [string]$EnvName = "pysrt3d"
)

# Check if conda is available
if (-not (Get-Command conda -ErrorAction SilentlyContinue)) {
    Write-Host "Error: conda is not found in PATH. Please install Anaconda/Miniconda first." -ForegroundColor Red
    exit 1
}

# Initialize conda for PowerShell (if not already done)
& conda shell.powershell hook | Out-String | Invoke-Expression

# Check if environment exists, if not create it
$envExists = conda env list | Select-String -Pattern "^$EnvName\s"
if (-not $envExists) {
    Write-Host "Creating conda environment: $EnvName" -ForegroundColor Yellow
    conda create -n $EnvName python=3.11 -y
}

# Activate the environment
Write-Host "Activating conda environment: $EnvName" -ForegroundColor Green
conda activate $EnvName

# Install dependencies
Write-Host "Installing dependencies..." -ForegroundColor Yellow
conda install -y glew glfw eigen libopencv
pip install numpy opencv-python

# Install pysrt3d package if not already installed
Write-Host "Installing pysrt3d package..." -ForegroundColor Yellow
$repoRoot = Split-Path -Parent $PSScriptRoot
Set-Location $repoRoot
pip install -e .

# Run the demo
Write-Host "Running demo.py..." -ForegroundColor Green
Set-Location "$repoRoot\example"
python demo.py
