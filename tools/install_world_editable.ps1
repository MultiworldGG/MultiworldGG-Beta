#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Install a world as an editable package.

.DESCRIPTION
    This script installs a world package as editable using pip install -e.
    It temporarily moves pyproject.toml to the project root, then installs the package.

.PARAMETER World
    The name of the world to install (e.g., kh2, sc2, minecraft)

.EXAMPLE
    .\install_world_editable.ps1 -World kh2
    .\install_world_editable.ps1 -World sc2 -Verbose
#>

[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)]
    [string]$World
)

$ErrorActionPreference = "Stop"

# Get project root (parent of src directory)
$scriptPath = $PSScriptRoot
$projectRoot = Split-Path -Parent $scriptPath

# Paths
$worldsDir = Join-Path $projectRoot "worlds"
$worldPath = Join-Path $worldsDir $World
$pyprojectPath = Join-Path $worldPath "pyproject.toml"
$pyprojectInRoot = Join-Path $projectRoot "pyproject.toml"
$manifestPath = Join-Path $projectRoot "MANIFEST.in"

# Check if world directory exists
if (-not (Test-Path $worldPath)) {
    Write-Host "Error: World directory '$World' not found in $worldsDir" -ForegroundColor Red
    exit 1
}

# Check if pyproject.toml exists
if (-not (Test-Path $pyprojectPath)) {
    Write-Host "Error: pyproject.toml not found in $World directory" -ForegroundColor Red
    exit 1
}

# Check if we're in a virtual environment
$pythonExe = (Get-Command python).Source
if ($pythonExe -notmatch "venv") {
    Write-Host "Warning: You may not be running from a virtual environment" -ForegroundColor Yellow
    Write-Host "Python executable: $pythonExe" -ForegroundColor Yellow
}

try {
    Write-Host "Processing world: $World" -ForegroundColor Yellow
    
    # Create MANIFEST.in.
    # Exclude pattern is *.py[co] (not *.py[cod]) — [cod] would also match
    # `.pyd`, i.e. Windows native extensions, which we want to ship.
    $manifestContent = @"
global-exclude *
graft src/worlds/$World
global-exclude *~ *.py[co]
include pyproject.toml
"@
    Set-Content -Path $manifestPath -Value $manifestContent
    Write-Verbose "  Created MANIFEST.in"
    
    # Move pyproject.toml to project root
    Move-Item -Path $pyprojectPath -Destination $pyprojectInRoot -Force
    Write-Verbose "  Moved pyproject.toml to project root"
    
    # Change to project root
    Push-Location $projectRoot
    
    try {
        # Install as editable
        Write-Host "  Installing as editable..." -ForegroundColor Cyan
        $installArgs = @("-m", "pip", "install", "-e", ".")
        
        if ($VerbosePreference -eq 'Continue') {
            $result = & python $installArgs
        } else {
            $result = & python $installArgs 2>&1
        }
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "  [OK] Installed $World as editable" -ForegroundColor Green
        } else {
            Write-Host "  [FAILED] Installation failed for $World" -ForegroundColor Red
            Write-Host "  Install output:" -ForegroundColor Gray
            $result | ForEach-Object {
                if ($_.ToString().Trim()) {
                    Write-Host "    $_" -ForegroundColor Gray
                }
            }
            exit 1
        }
    } finally {
        Pop-Location
    }
    
    # Move pyproject.toml back
    if (Test-Path $pyprojectInRoot) {
        Move-Item -Path $pyprojectInRoot -Destination $pyprojectPath -Force
        Write-Verbose "  Moved pyproject.toml back to $World/"
    } else {
        Write-Host "  Warning: pyproject.toml not found in root directory after install" -ForegroundColor Yellow
    }
    
} catch {
    Write-Host "  [FAILED] Error processing $World : $_" -ForegroundColor Red
    
    # Restore pyproject.toml if needed
    if ((Test-Path $pyprojectInRoot) -and -not (Test-Path $pyprojectPath)) {
        Move-Item -Path $pyprojectInRoot -Destination $pyprojectPath -Force
        Write-Verbose "  Restored pyproject.toml to $World/"
    }
    
    exit 1
} finally {
    # Remove MANIFEST.in
    if (Test-Path $manifestPath) {
        Remove-Item $manifestPath
        Write-Verbose "  Removed MANIFEST.in"
    }
}

Write-Host "`nInstallation completed!" -ForegroundColor Green

