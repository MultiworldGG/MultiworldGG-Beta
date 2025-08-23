# MultiWorldGG Build Script for Windows
# Run this script from the src directory

param(
    [switch]$Clean,
    [switch]$SkipRequirements,
    [switch]$SkipWheels,
    [switch]$SkipModules,
    [switch]$Verify,
    [switch]$Help
)

if ($Help) {
    Write-Host @"
MultiWorldGG Build Script for Windows

Usage: .\build_exe.ps1 [OPTIONS]

Options:
    -Clean              Clean build directory before building
    -SkipRequirements   Skip requirements installation
    -SkipWheels         Skip wheel installation  
    -SkipModules        Skip module update
    -Verify             Verify build output after building
    -Help               Show this help message

Examples:
    .\build_exe.ps1 -Clean -Verify
    .\build_exe.ps1 -SkipRequirements -SkipWheels
    .\build_exe.ps1 -SkipRequirements -SkipWheels -SkipModules

"@
    exit 0
}

Write-Host "MultiWorldGG Build Script for Windows" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green

# Check if we're in the right directory
if (-not (Test-Path "setup.py")) {
    Write-Host "Error: setup.py not found. Please run this script from the src directory." -ForegroundColor Red
    exit 1
}

# Check Python version
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Python not found in PATH" -ForegroundColor Red
    exit 1
}

Write-Host "Python version: $pythonVersion" -ForegroundColor Yellow

# Check if Python version is 3.12+
$versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
if ($versionMatch) {
    $major = [int]$matches[1]
    $minor = [int]$matches[2]
    if ($major -lt 3 -or ($major -eq 3 -and $minor -lt 12)) {
        Write-Host "Error: Python 3.12 or higher is required" -ForegroundColor Red
        exit 1
    }
}

# Clean build directory if requested
if ($Clean) {
    Write-Host "Cleaning build directory..." -ForegroundColor Yellow
    if (Test-Path "build") {
        Remove-Item -Recurse -Force "build"
        Write-Host "Build directory cleaned" -ForegroundColor Green
    }
}

# Install cx_Freeze
Write-Host "Checking cx_Freeze installation..." -ForegroundColor Yellow
try {
    python -c "import cx_Freeze" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "cx_Freeze is already installed" -ForegroundColor Green
    } else {
        throw "cx_Freeze not found"
    }
} catch {
    Write-Host "Installing cx_Freeze..." -ForegroundColor Yellow
    python -m pip install "cx-Freeze>=6.15.0"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Error: Failed to install cx_Freeze" -ForegroundColor Red
        exit 1
    }
    Write-Host "cx_Freeze installed successfully" -ForegroundColor Green
}

# Install requirements
if (-not $SkipRequirements) {
    Write-Host "Installing requirements from main requirements.txt..." -ForegroundColor Yellow
    if (Test-Path "requirements.txt") {
        # Use absolute path to ensure we're using the correct requirements.txt
        $absReqFile = (Resolve-Path "requirements.txt").Path
        python -m pip install -r $absReqFile
        if ($LASTEXITCODE -ne 0) {
            Write-Host "Error: Failed to install requirements" -ForegroundColor Red
            exit 1
        }
        Write-Host "Requirements installed successfully" -ForegroundColor Green
    } else {
        Write-Host "requirements.txt not found, skipping requirements installation" -ForegroundColor Yellow
    }
}

# Install wheels
if (-not $SkipWheels) {
    Write-Host "Installing wheels from default_wheels..." -ForegroundColor Yellow
    if (Test-Path "default_wheels") {
        $wheels = Get-ChildItem "default_wheels/*.whl"
        $successCount = 0
        $totalCount = $wheels.Count
        
        foreach ($wheel in $wheels) {
            Write-Host "Installing $($wheel.Name)..." -ForegroundColor Cyan
            python -m pip install $wheel.FullName --no-deps --force-reinstall
            if ($LASTEXITCODE -eq 0) {
                Write-Host "✓ Installed $($wheel.Name)" -ForegroundColor Green
                $successCount++
            } else {
                Write-Host "✗ Failed to install $($wheel.Name)" -ForegroundColor Red
            }
        }
        
        Write-Host "Wheel installation complete: $successCount/$totalCount successful" -ForegroundColor Yellow
    } else {
        Write-Host "default_wheels directory not found, skipping wheel installation" -ForegroundColor Yellow
    }
}

# Update modules (skip world requirements)
if (-not $SkipModules) {
    Write-Host "Updating modules..." -ForegroundColor Yellow
    $env:SKIP_REQUIREMENTS_UPDATE = "1"
    python -c "import ModuleUpdate; ModuleUpdate.update(yes=True)"
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Module update completed" -ForegroundColor Green
    } else {
        Write-Host "Warning: Module update failed" -ForegroundColor Yellow
    }
}

# Run cx_Freeze build
Write-Host "Starting cx_Freeze build..." -ForegroundColor Yellow
python setup.py build_exe
if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: cx_Freeze build failed" -ForegroundColor Red
    exit 1
}
Write-Host "cx_Freeze build completed successfully" -ForegroundColor Green

# Verify build output
if ($Verify) {
    Write-Host "Verifying build output..." -ForegroundColor Yellow
    
    if (-not (Test-Path "build")) {
        Write-Host "Error: Build directory not found" -ForegroundColor Red
        exit 1
    }
    
    $exeDirs = Get-ChildItem "build" -Directory | Where-Object { $_.Name -like "exe.*" }
    if ($exeDirs.Count -eq 0) {
        Write-Host "Error: No executable build directory found" -ForegroundColor Red
        exit 1
    }
    
    $exeDir = $exeDirs[0]
    Write-Host "Checking build output in: $($exeDir.FullName)" -ForegroundColor Cyan
    
    # Check for expected executables
    $expectedExes = @("MultiWorld.exe", "MultiServer.exe", "Generate.exe", "Patch.exe", "MultiWorldDebug.exe")
    $missingExes = @()
    
    foreach ($exe in $expectedExes) {
        $exePath = Join-Path $exeDir.FullName $exe
        if (Test-Path $exePath) {
            Write-Host "✓ Found $exe" -ForegroundColor Green
        } else {
            Write-Host "✗ Missing $exe" -ForegroundColor Red
            $missingExes += $exe
        }
    }
    
    if ($missingExes.Count -gt 0) {
        Write-Host "Build verification failed: $($missingExes.Count) executables missing" -ForegroundColor Red
        exit 1
    }
    
    # Check for required directories
    $requiredDirs = @("data", "lib")
    $missingDirs = @()
    
    foreach ($dir in $requiredDirs) {
        $dirPath = Join-Path $exeDir.FullName $dir
        if (Test-Path $dirPath) {
            Write-Host "✓ Found $dir/" -ForegroundColor Green
        } else {
            Write-Host "✗ Missing $dir/" -ForegroundColor Red
            $missingDirs += $dir
        }
    }
    
    if ($missingDirs.Count -gt 0) {
        Write-Host "Build verification failed: $($missingDirs.Count) directories missing" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Build verification passed!" -ForegroundColor Green
}

Write-Host "=====================================" -ForegroundColor Green
Write-Host "Build completed successfully!" -ForegroundColor Green

# Show build location
if (Test-Path "build") {
    $exeDirs = Get-ChildItem "build" -Directory | Where-Object { $_.Name -like "exe.*" }
    if ($exeDirs.Count -gt 0) {
        Write-Host "Executables are located in: $($exeDirs[0].FullName)" -ForegroundColor Cyan
    }
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
