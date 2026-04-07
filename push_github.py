#!/usr/bin/env python3
"""Push Kawach project to GitHub"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a shell command and return output"""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        if result.stdout:
            print(f"✓ {result.stdout.strip()}")
        if result.stderr and "warning" not in result.stderr.lower():
            print(f"! {result.stderr.strip()}")
        return result.returncode == 0
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def main():
    project_dir = r"d:\disease_final"
    os.chdir(project_dir)
    
    print("=" * 60)
    print("PUSHING KAWACH PROJECT TO GITHUB")
    print("=" * 60)
    
    # Step 1: Remove old git if exists
    print("\n[1/7] Removing old git repository...")
    if Path(".git").exists():
        import shutil
        shutil.rmtree(".git")
        print("✓ Old git repository removed")
    
    # Step 2: Initialize git
    print("\n[2/7] Initializing git repository...")
    if run_command("git init"):
        print("✓ Git repository initialized")
    else:
        print("✗ Failed to initialize git")
        return
    
    # Step 3: Configure git user
    print("\n[3/7] Configuring git user...")
    run_command('git config user.name "Jagriti Arora"')
    run_command('git config user.email "jagriti@example.com"')
    print("✓ Git user configured")
    
    # Step 4: Add all files
    print("\n[4/7] Adding all files...")
    if run_command("git add -A"):
        print("✓ All files added")
    else:
        print("✗ Failed to add files")
        return
    
    # Step 5: Create commit
    print("\n[5/7] Creating commit...")
    commit_msg = """Kawach AI Medical Diagnostic Hub - Complete Redesign

- Professional dark mode theme with gradient backgrounds
- Enhanced header with enlarged title
- Modern form styling and improved UX
- Grad-CAM visualization
- Professional medical report cards
- Improved navigation
- Modern alert boxes and components
- Responsive design"""
    
    if run_command(f'git commit -m "{commit_msg}"'):
        print("✓ Commit created")
    else:
        print("✗ Failed to commit")
        return
    
    # Step 6: Rename branch to main
    print("\n[6/7] Setting up main branch...")
    run_command("git branch -M main")
    print("✓ Main branch ready")
    
    # Step 7: Add remote and push
    print("\n[7/7] Pushing to GitHub...")
    run_command("git remote add origin https://github.com/jagriti2325/kawach.git")
    
    if run_command("git push -u origin main --force"):
        print("✓ Successfully pushed to GitHub!")
        print("\nRepository: https://github.com/jagriti2325/kawach")
    else:
        print("\n⚠ Push may require authentication")
        print("GitHub may need your Personal Access Token")
        print("\nTo fix:")
        print("1. Go to GitHub.com → Settings → Developer settings → Personal access tokens")
        print("2. Generate a new token with 'repo' scope")
        print("3. Run: git push -u origin main --force")
        print("   Use your username and token when prompted")
    
    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)

if __name__ == "__main__":
    main()
