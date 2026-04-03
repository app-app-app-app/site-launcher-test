from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time
import os


def upload_zip_to_keitaro(keitaro_url, username, password, zip_file_path, offer_name):

    options = webdriver.ChromeOptions()

    # --- ОБОВʼЯЗКОВО ДЛЯ STREAMLIT CLOUD ---
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # --- ФІКС SSL ---
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--allow-insecure-localhost')

    # --- СТАБІЛЬНІСТЬ ---
    options.add_argument('--disable-blink-features=AutomationControlled')

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)

    wait = WebDriverWait(driver, 25)

    try:
        print(f"🔐 Login to Keitaro: {keitaro_url}")

        # --- 1. OPEN ADMIN ---
        driver.get(f"{keitaro_url}/admin/")

        # --- DEBUG (можеш закоментити потім) ---
        time.sleep(3)
        print("CURRENT URL:", driver.current_url)
        html = driver.page_source
        print("PAGE LENGTH:", len(html))
        print(html[:1000])

        # --- 2. WAIT ANGULAR APP ---
        wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "app-login"))
        )

        print("✅ Angular login loaded")

        # --- 3. LOGIN ---
        username_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "login"))
        )
        username_field.clear()
        username_field.send_keys(username)

        password_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "password"))
        )
        password_field.clear()
        password_field.send_keys(password)

        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_btn.click()

        print("⏳ Logging in...")

        time.sleep(4)

        # --- 4. OPEN CREATE OFFER ---
        driver.get(f"{keitaro_url}/admin/#!/offers/new")

        print("📁 Open create offer page")

        # --- 5. WAIT PAGE ---
        wait.until(
            EC.visibility_of_element_located((By.TAG_NAME, "body"))
        )

        time.sleep(2)

        # --- 6. OFFER NAME ---
        name_field = wait.until(
            EC.visibility_of_element_located((By.NAME, "name"))
        )
        name_field.send_keys(offer_name)

        print(f"✍️ Offer name: {offer_name}")

        # --- 7. SELECT LOCAL (якщо є) ---
        try:
            local_radio = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "input[value='local']"))
            )
            local_radio.click()
        except:
            print("⚠️ Local radio not found (skip)")

        # --- 8. UPLOAD ZIP ---
        abs_path = os.path.abspath(zip_file_path)

        file_input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(abs_path)

        print(f"📦 ZIP uploaded: {abs_path}")

        # --- 9. CREATE ---
        submit_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        submit_btn.click()

        print("🚀 Creating offer...")

        time.sleep(5)

        # --- 10. GET OFFER ID ---
        current_url = driver.current_url
        print("FINAL URL:", current_url)

        if '/offers/' in current_url:
            try:
                offer_id = current_url.split('/offers/')[1].split('/')[0]
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
