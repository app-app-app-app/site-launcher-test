import os
import time
import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ================================
# 🔥 LOG FUNCTION (UI + console)
# ================================
def log(msg):
    print(msg)
    try:
        st.write(msg)
    except:
        pass


# ================================
# 🚀 MAIN FUNCTION
# ================================
def upload_zip_to_keitaro(
    keitaro_url,
    username,
    password,
    zip_file_path,
    offer_name
):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-insecure-localhost")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 20)

    try:
        log(f"🔐 Opening login page: {keitaro_url}")

        # ------------------------
        # 1. OPEN LOGIN
        # ------------------------
        driver.get(f"{keitaro_url}/admin/")
        
        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "app-login"))
        )

        log("✍️ Filling login...")

        username_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='login']"))
        )

        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )

        username_input.send_keys(username)
        password_input.send_keys(password)

        log("🖱 Clicking login...")

        login_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        login_btn.click()

        # ------------------------
        # 2. WAIT LOGIN SUCCESS
        # ------------------------
        log("⏳ Waiting for login to complete...")

        wait.until(
            EC.invisibility_of_element_located((By.TAG_NAME, "app-login"))
        )

        log("✅ Logged in!")

        # ------------------------
        # 3. OPEN CREATE OFFER
        # ------------------------
        log("📁 Opening offer creation page...")

        driver.get(f"{keitaro_url}/admin/#!/offers/new")

        # IMPORTANT: Angular delay
        time.sleep(2)

        # ------------------------
        # 4. SELECT LOCAL TYPE
        # ------------------------
        log("📝 Selecting LOCAL offer type...")

        local_radio = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//input[@type='radio' and @value='local']")
            )
        )
        local_radio.click()

        # ------------------------
        # 5. FILL NAME
        # ------------------------
        log(f"✍️ Entering offer name: {offer_name}")

        name_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@type='text']")
            )
        )
        name_input.clear()
        name_input.send_keys(offer_name)

        # ------------------------
        # 6. UPLOAD ZIP
        # ------------------------
        log(f"📦 Uploading ZIP: {zip_file_path}")

        abs_path = os.path.abspath(zip_file_path)

        file_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='file']")
            )
        )
        file_input.send_keys(abs_path)

        log("⏳ Waiting for upload...")
        time.sleep(5)

        # ------------------------
        # 7. CLICK CREATE
        # ------------------------
        log("🖱 Clicking CREATE...")

        create_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit']")
            )
        )
        create_btn.click()

        # ------------------------
        # 8. WAIT RESULT
        # ------------------------
        log("⏳ Waiting for redirect...")

        time.sleep(6)

        current_url = driver.current_url
        log(f"🌐 Current URL: {current_url}")

        # ------------------------
        # 9. EXTRACT OFFER ID
        # ------------------------
        if "/offers/" in current_url:
            offer_id = current_url.split("/offers/")[1].split("/")[0]
            try:
                offer_id = int(offer_id)
                log(f"✅ Offer created! ID: {offer_id}")
                return offer_id
            except:
                pass

        # fallback
        page = driver.page_source

        if offer_name in page:
            log("✅ Offer created (detected in page)")
            return True

        log("❌ Failed to detect offer creation")
        return None

    except Exception as e:
        log(f"❌ Selenium error: {e}")
        import traceback
        traceback.print_exc()
        return None

    finally:
        driver.quit()
        log("🔒 Browser closed")
