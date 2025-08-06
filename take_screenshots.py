#!/usr/bin/env python3
"""
Screenshot helper script for VRT Calculator documentation
"""

import os
import time
import subprocess
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Setup Chrome driver with appropriate options"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Remove this line to see the browser
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    try:
        # Try using system chromedriver first
        driver = webdriver.Chrome(options=chrome_options)
        return driver
    except Exception as e1:
        try:
            # Fallback to webdriver-manager
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=chrome_options)
            return driver
        except Exception as e2:
            print(f"Error setting up Chrome driver with system chromedriver: {e1}")
            print(f"Error setting up Chrome driver with webdriver-manager: {e2}")
            print("Make sure you have Chrome installed and chromedriver in PATH")
            return None

def start_flask_app():
    """Start the Flask app in the background"""
    try:
        print("Starting Flask app...")
        proc = subprocess.Popen([sys.executable, 'app.py'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
        
        # Wait for the app to start
        time.sleep(5)
        
        # Check if it's running
        if proc.poll() is None:
            print("Flask app started successfully on http://localhost:5000")
            return proc
        else:
            stdout, stderr = proc.communicate()
            print(f"Flask app failed to start:")
            print(f"STDOUT: {stdout.decode()}")
            print(f"STDERR: {stderr.decode()}")
            return None
            
    except Exception as e:
        print(f"Error starting Flask app: {e}")
        return None

def stop_flask_app(proc):
    """Stop the Flask app"""
    if proc and proc.poll() is None:
        proc.terminate()
        proc.wait()
        print("Flask app stopped")

def take_screenshot(driver, url, filename, wait_for_element=None):
    """Take a screenshot of a specific page"""
    try:
        driver.get(url)
        
        if wait_for_element:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, wait_for_element))
            )
        
        time.sleep(2)  # Allow page to fully load
        
        screenshot_path = f"static/images/screenshots/{filename}"
        driver.save_screenshot(screenshot_path)
        print(f"Screenshot saved: {screenshot_path}")
        
    except Exception as e:
        print(f"Error taking screenshot {filename}: {e}")

def take_mobile_screenshot(driver, url, filename):
    """Take a mobile-sized screenshot"""
    try:
        # Set mobile viewport
        driver.set_window_size(375, 812)  # iPhone X size
        driver.get(url)
        time.sleep(2)
        
        screenshot_path = f"static/images/screenshots/{filename}"
        driver.save_screenshot(screenshot_path)
        print(f"Mobile screenshot saved: {screenshot_path}")
        
        # Reset to desktop size
        driver.set_window_size(1920, 1080)
        
    except Exception as e:
        print(f"Error taking mobile screenshot {filename}: {e}")

def main():
    """Main function to take all screenshots"""
    base_url = "http://localhost:5000"
    
    # Create screenshots directory if it doesn't exist
    os.makedirs("static/images/screenshots", exist_ok=True)
    
    # Start Flask app
    flask_proc = start_flask_app()
    if not flask_proc:
        print("Failed to start Flask app. Please start it manually with: python3 app.py")
        return
    
    driver = setup_driver()
    if not driver:
        stop_flask_app(flask_proc)
        return
    
    try:
        print("Taking screenshots for VRT Calculator...")
        
        # Main interface
        print("📸 Taking main interface screenshot...")
        take_screenshot(driver, base_url, "main-interface.png", ".card")
        
        # Fill out form and take results screenshot
        print("📸 Taking results page screenshot...")
        driver.get(base_url)
        time.sleep(2)
        
        # Fill out the form with correct field IDs
        driver.find_element(By.ID, "uk_price").send_keys("15000")
        driver.find_element(By.ID, "co2_emissions").send_keys("150")
        driver.find_element(By.ID, "vehicle_age").send_keys("4")  # 4 years old
        
        # Select fuel type
        fuel_select = driver.find_element(By.ID, "fuel_type")
        fuel_select.send_keys("petrol")
        
        # Scroll to submit button and click using JavaScript
        submit_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        time.sleep(1)
        driver.execute_script("arguments[0].click();", submit_button)
        
        # Wait for results page and take screenshot
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".container"))
        )
        take_screenshot(driver, driver.current_url, "results-page.png")
        
        # About page
        print("📸 Taking about page screenshot...")
        take_screenshot(driver, f"{base_url}/about", "about-page.png", ".container")
        
        # Mobile screenshots
        print("📸 Taking mobile view screenshot...")
        take_mobile_screenshot(driver, base_url, "mobile-view.png")
        
        print("\n✅ All screenshots taken successfully!")
        print("Screenshots saved in: static/images/screenshots/")
        print("\nScreenshots created:")
        for filename in ["main-interface.png", "results-page.png", "about-page.png", "mobile-view.png"]:
            filepath = f"static/images/screenshots/{filename}"
            if os.path.exists(filepath):
                size = os.path.getsize(filepath)
                print(f"  ✓ {filename} ({size:,} bytes)")
            else:
                print(f"  ✗ {filename} (not created)")
        
    except Exception as e:
        print(f"Error during screenshot process: {e}")
        print("Make sure the Flask app is running and accessible")
        
    finally:
        driver.quit()
        stop_flask_app(flask_proc)

if __name__ == "__main__":
    main()
