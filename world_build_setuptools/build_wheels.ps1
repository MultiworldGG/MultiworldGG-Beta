# Build wheels for all worlds
# This script moves each world's pyproject.toml to the worlds/ directory,
# builds the wheel, then moves it back to the original location

param(
    [switch]$Clean = $false,
    [switch]$Verbose = $false
)

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $ScriptDir

#Activate virtual environment
$VenvPath = Join-Path $ScriptDir "src\venv\Scripts\Activate.ps1"
if (Test-Path $VenvPath) {
    Write-Host "Activating virtual environment..." -ForegroundColor Cyan
    & $VenvPath
    Write-Host "Virtual environment activated" -ForegroundColor Green
} else {
    Write-Host "Warning: Virtual environment not found at $VenvPath" -ForegroundColor Yellow
    Write-Host "Continuing with system Python..." -ForegroundColor Yellow
}

# Find all pyproject.toml files in subdirectories
$WorldsDir = Join-Path $ScriptDir "src\worlds"
$WorldsWithPyProject = Get-ChildItem -Path $WorldsDir -Name "pyproject.toml" -Recurse | ForEach-Object {
    Split-Path -Parent $_
} | Sort-Object

Write-Host "Found $($WorldsWithPyProject.Count) worlds with pyproject.toml files" -ForegroundColor Green

# Create backup directory for pyproject.toml files
$BackupDir = Join-Path $WorldsDir "pyproject_backups"
if (Test-Path $BackupDir) {
    Remove-Item $BackupDir -Recurse -Force
}
New-Item -ItemType Directory -Path $BackupDir | Out-Null

# Track successful and failed builds
$SuccessfulBuilds = @()
$FailedBuilds = @()
$SkippedBuilds = @()

foreach ($World in $WorldsWithPyProject) {
    $WorldPath = Join-Path $WorldsDir $World
    $PyProjectPath = Join-Path $WorldPath "pyproject.toml"
    $BackupPath = Join-Path $BackupDir "$World.pyproject.toml"
    
    Write-Host "Processing world: $World" -ForegroundColor Yellow
    
    # Check if pyproject.toml exists 
    if (-not (Test-Path $PyProjectPath)) {
        Write-Host "  Skipping $World - no pyproject.toml found" -ForegroundColor Red
        $FailedBuilds += "$World (no pyproject.toml)"
        continue
    }
    
    # Check if wheel already exists in dist directory
    $DistDir = Join-Path $ScriptDir "dist"
    if (Test-Path $DistDir) {
        $ExistingWheels = Get-ChildItem -Path $DistDir -Filter "*.whl" | Where-Object { 
            $_.Name -like "worlds_$World-*"
        }
        if ($ExistingWheels.Count -gt 0) {
            Write-Host "  Skipping $World - wheel already exists in dist/" -ForegroundColor Blue
            $SkippedBuilds += $World
            continue
        }
    }
    
    # Create MANIFEST.in for this world
    "global-exclude *" | Out-File -FilePath "MANIFEST.in"
    "graft src/worlds/$World" | Out-File -FilePath "MANIFEST.in" -Append
    "global-exclude *~ *.py[cod]" | Out-File -FilePath "MANIFEST.in" -Append
    "include pyproject.toml" | Out-File -FilePath "MANIFEST.in" -Append
    
    try {
        # Backup original pyproject.toml
        Copy-Item $PyProjectPath $BackupPath
        
        # Move pyproject.toml to worlds/ directory
        Move-Item $PyProjectPath $ScriptDir
        
        if ($Verbose) {
            Write-Host "  Moved pyproject.toml to src/ parent directory" -ForegroundColor Gray
        }
        
        # Run build command
        Write-Host "  Building wheel..." -ForegroundColor Cyan
        $BuildResult = & python -m build 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  ✓ Build successful for $World" -ForegroundColor Green
            $SuccessfulBuilds += $World
        } else {
            Write-Host "  ✗ Build failed for $World" -ForegroundColor Red
            Write-Host "  Build output:" -ForegroundColor Gray
            $BuildResult | ForEach-Object { Write-Host "    $_" -ForegroundColor Gray }
            $FailedBuilds += $World
        }
        
        # Move pyproject.toml back to original location
        $PyProjectInWorlds = Join-Path $ScriptDir "pyproject.toml"
        if (Test-Path $PyProjectInWorlds) {
            Move-Item $PyProjectInWorlds $PyProjectPath
            if ($Verbose) {
                Write-Host "  Moved pyproject.toml back to $World/" -ForegroundColor Gray
            }
        } else {
            Write-Host "  Warning: pyproject.toml not found in worlds/ directory after build" -ForegroundColor Yellow
        }
        
    } catch {
        Write-Host "  ✗ Error processing $World : $($_.Exception.Message)" -ForegroundColor Red
        $FailedBuilds += "$World (error: $($_.Exception.Message))"
        
        # Try to restore pyproject.toml from backup
        if (Test-Path $BackupPath) {
            $PyProjectInWorlds = Join-Path $WorldsDir "pyproject.toml"
            if (Test-Path $PyProjectInWorlds) {
                Remove-Item $PyProjectInWorlds -Force
            }
            Move-Item $BackupPath $PyProjectPath
            Write-Host "  Restored pyproject.toml from backup" -ForegroundColor Yellow
        }
    }
}

# Cleanup backup directory
if (Test-Path $BackupDir) {
    Remove-Item $BackupDir -Recurse -Force
}
Remove-Item "MANIFEST.in"

# Summary
Write-Host "`nBuild Summary:" -ForegroundColor Magenta
Write-Host "=============" -ForegroundColor Magenta
Write-Host "Skipped builds: $($SkippedBuilds.Count)" -ForegroundColor Yellow
Write-Host "Successful builds: $($SuccessfulBuilds.Count)" -ForegroundColor Green
Write-Host "Failed builds: $($FailedBuilds.Count)" -ForegroundColor Red

if ($SkippedBuilds.Count -gt 0) {
    Write-Host "`nSkipped builds:" -ForegroundColor Yellow
    $SkippedBuilds | ForEach-Object { Write-Host "  ✗ $_" -ForegroundColor Yellow }
}

if ($SuccessfulBuilds.Count -gt 0) {
    Write-Host "`nSuccessful builds:" -ForegroundColor Green
    $SuccessfulBuilds | ForEach-Object { Write-Host "  ✓ $_" -ForegroundColor Green }
}

if ($FailedBuilds.Count -gt 0) {
    Write-Host "`nFailed builds:" -ForegroundColor Red
    $FailedBuilds | ForEach-Object { Write-Host "  ✗ $_" -ForegroundColor Red }
}

Write-Host "`nBuild process completed!" -ForegroundColor Green