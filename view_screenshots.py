#!/usr/bin/env python3
"""
Simple script to view the generated screenshots
"""

import os
import subprocess
import sys

def view_screenshots():
    """Open all screenshots in the default image viewer"""
    screenshot_dir = "static/images/screenshots"
    
    if not os.path.exists(screenshot_dir):
        print(f"Screenshot directory {screenshot_dir} does not exist")
        return
    
    screenshots = [
        "main-interface.png",
        "results-page.png", 
        "about-page.png",
        "mobile-view.png"
    ]
    
    print("📸 VRT Calculator Screenshots:")
    print("=" * 40)
    
    for screenshot in screenshots:
        filepath = os.path.join(screenshot_dir, screenshot)
        if os.path.exists(filepath):
            size = os.path.getsize(filepath)
            print(f"✓ {screenshot} ({size:,} bytes)")
            
            # Open in default image viewer (macOS)
            try:
                subprocess.run(["open", filepath], check=True)
            except subprocess.CalledProcessError:
                print(f"  Could not open {screenshot}")
        else:
            print(f"✗ {screenshot} (missing)")
    
    print("\nScreenshots should now be open in your default image viewer!")

if __name__ == "__main__":
    view_screenshots()
