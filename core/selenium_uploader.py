from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os


def upload_zip_to_keitaro(keitaro_url, username, password, zip_file_path, offer_name):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 20)

    try:
        print(f"🔐 Login to Keitaro: {keitaro_url}")

        # --- 1. OPEN ADMIN ---
        driver.get(f"{keitaro_url}/admin/")

        # wait for Angular login form
        wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.login-form"))
        )

        print("✅ Login page loaded")

        # --- 2. LOGIN ---
        username_field = wait.until(
            EC.presence_of_element_located((By.NAME, "login"))
        )
        username_field.send_keys(username)

        password_field = wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(password)

        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_btn.click()

        print("⏳ Logging in...")

        # wait after login
        time.sleep(3)

        # --- 3. OPEN CREATE OFFER ---
        driver.get(f"{keitaro_url}/offers/create")

        print("📁 Opened create offer page")

        # --- 4. WAIT PAGE ---
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # --- 5. SELECT LOCAL ---
        try:
            local_radio = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='local']"))
            )
            local_radio.click()
        except:
            print("⚠️ Local radio not found (skip)")

        # --- 6. OFFER NAME ---
        name_field = wait.until(
            EC.presence_of_element_located((By.NAME, "name"))
        )
        name_field.send_keys(offer_name)

        print(f"✍️ Offer name: {offer_name}")

        # --- 7. UPLOAD ZIP ---
        abs_path = os.path.abspath(zip_file_path)

        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(abs_path)

        print(f"📦 ZIP uploaded: {abs_path}")

        # --- 8. CREATE ---
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_btn.click()

        print("🚀 Creating offer...")

        time.sleep(5)

        # --- 9. GET OFFER ID ---
        current_url = driver.current_url
        print("URL:", current_url)

        if '/offers/' in current_url:
            parts = current_url.split('/offers/')
            if len(parts) > 1:
                offer_id = parts[1].split('/')[0]
                try:
                    return int(offer_id)
                except:
                    pass

        print("❌ Offer ID not found")
        return None

    except Exception as e:
        print("❌ Selenium error:", e)
        import traceback
        traceback.print_exc()
        return None

    finally:
        driver.quit()
        print("🔒 Browser closed")
