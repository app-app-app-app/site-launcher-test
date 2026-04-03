import os
import time
import streamlit as st

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# ================================
# 🔥 LOGGER (UI + console)
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

    # --- STREAMLIT CLOUD FIXES ---
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")

    # --- SSL FIX ---
    options.add_argument("--ignore-certificate-errors")
    options.add_argument("--ignore-ssl-errors")
    options.add_argument("--allow-insecure-localhost")

    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 25)

    try:
        # =========================
        # 1. OPEN LOGIN
        # =========================
        log(f"🔐 Opening login page: {keitaro_url}")
        driver.get(f"{keitaro_url}/admin/")

        wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "app-login"))
        )

        log("✍️ Filling login form...")

        username_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='login']"))
        )

        password_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='password']"))
        )

        # --- IMPORTANT FOR ANGULAR ---
        username_input.click()
        username_input.clear()
        username_input.send_keys(username)

        password_input.click()
        password_input.clear()
        password_input.send_keys(password)

        log("🖱 Submitting login (ENTER)...")

        password_input.send_keys(Keys.ENTER)

        # =========================
        # 2. VERIFY LOGIN
        # =========================
        time.sleep(4)

        current_url = driver.current_url
        log(f"🌐 After login URL: {current_url}")

        html = driver.page_source

        if "login-form" in html:
            log("❌ LOGIN FAILED (still on login page)")
            return None

        log("✅ LOGIN SUCCESS")

        # =========================
        # 3. OPEN CREATE OFFER
        # =========================
        log("📁 Opening offer creation page...")
        driver.get(f"{keitaro_url}/admin/#!/offers/new")

        time.sleep(3)

        # =========================
        # 4. SELECT LOCAL TYPE
        # =========================
        log("📝 Selecting LOCAL offer type...")

        try:
            local_radio = wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[@type='radio' and @value='local']")
                )
            )
            local_radio.click()
        except:
            log("⚠️ Local type not found (skip)")

        # =========================
        # 5. FILL NAME
        # =========================
        log(f"✍️ Entering offer name: {offer_name}")

        name_input = wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//input[@type='text']")
            )
        )

        name_input.clear()
        name_input.send_keys(offer_name)

        # =========================
        # 6. UPLOAD ZIP
        # =========================
        abs_path = os.path.abspath(zip_file_path)

        log(f"📦 Uploading ZIP: {abs_path}")

        file_input = wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//input[@type='file']")
            )
        )

        file_input.send_keys(abs_path)

        log("⏳ Waiting for upload...")
        time.sleep(5)

        # =========================
        # 7. CREATE OFFER
        # =========================
        log("🖱 Clicking CREATE...")

        create_btn = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@type='submit']")
            )
        )

        create_btn.click()

        # =========================
        # 8. WAIT RESULT
        # =========================
        log("⏳ Waiting for result...")
        time.sleep(6)

        final_url = driver.current_url
        log(f"🌐 Final URL: {final_url}")

        # =========================
        # 9. GET OFFER ID
        # =========================
        if "/offers/" in final_url:
            try:
                offer_id = final_url.split("/offers/")[1].split("/")[0]
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

        log("❌ Offer creation not detected")
        return None

    except Exception as e:
        import traceback

        log("❌ FULL ERROR:")
        log(str(e))
        log(traceback.format_exc())
        return None

    finally:
        driver.quit()
        log("🔒 Browser closed")
