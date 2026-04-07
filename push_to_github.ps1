# Git Push Script for Kawach Project
$ErrorActionPreference = "Stop"

Write-Host "=== Starting Git Push Process ===" -ForegroundColor Green

# Change to project directory
Set-Location "d:\disease_final"

# Remove old git directory if exists
if (Test-Path ".git") {
    Write-Host "Removing old .git directory..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force .git
}

# Initialize new git repository
Write-Host "Initializing new git repository..." -ForegroundColor Green
git init

# Configure git user
Write-Host "Configuring git user..." -ForegroundColor Green
git config user.name "Jagriti Arora"
git config user.email "jagriti@example.com"

# Add remote origin
Write-Host "Adding GitHub remote..." -ForegroundColor Green
git remote add origin https://github.com/jagriti2325/kawach.git

# Stage all files
Write-Host "Staging all files..." -ForegroundColor Green
git add -A

# Create initial commit
Write-Host "Creating commit..." -ForegroundColor Green
git commit -m "Kawach AI Medical Diagnostic Hub - Complete UI Redesign

- Professional dark mode theme with gradient backgrounds
- Enhanced header with large title and subtitle
- Modern form styling with rounded corners
- Grad-CAM visualization improvements
- Professional medical report cards
- Improved navigation (Home/About buttons)
- Modern alert boxes and status indicators
- Removed sidebar
- Better visual hierarchy and spacing
- Responsive design with professional UI components"

# Verify commit
Write-Host "Commit history:" -ForegroundColor Green
git log --oneline -3

# Push to GitHub
Write-Host "Pushing to GitHub (master branch)..." -ForegroundColor Green
git push -u origin master --force

Write-Host "=== Push Complete ===" -ForegroundColor Green
Write-Host "Your code is now on GitHub at: https://github.com/jagriti2325/kawach" -ForegroundColor Cyan
