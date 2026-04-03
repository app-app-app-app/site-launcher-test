"""
Selenium-based ZIP uploader for Keitaro
Загружает ZIP файлы в Keitaro через веб-интерфейс (обходит неработающий API)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os


def upload_zip_to_keitaro(keitaro_url, username, password, zip_file_path, offer_name):
    """
    Загружает ZIP в Keitaro через браузер вместо API
    
    Args:
        keitaro_url: URL Keitaro (например https://твой-keitaro.com)
        username: Логин админа
        password: Пароль админа
        zip_file_path: Полный путь к ZIP файлу
        offer_name: Имя оффера (обычно домен)
    
    Returns:
        offer_id (int) или None если ошибка
    """
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    from selenium.webdriver.chrome.service import Service

    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        print(f"🔐 Логинюсь в Keitaro ({keitaro_url})...")
        
        # 1️⃣ Логин
        driver.get(f"{keitaro_url}/admin#!/login")
        time.sleep(3)
        
        # Ищем поле username
        try:
            wait = WebDriverWait(driver, 10)

            username_field = wait.until(
                EC.presence_of_element_located((By.NAME, "login"))
            )
        except:
            username_field = driver.find_element(By.XPATH, "//input[@placeholder*='ogname' or @placeholder*='ser']")
        
        username_field.send_keys(username)
        time.sleep(1)
        
        # Ищем поле password
        try:
            password_field = wait.until(
                EC.presence_of_element_located((By.NAME, "password"))
            )
        except:
            password_field = driver.find_element(By.XPATH, "//input[@type='password']")
        
        password_field.send_keys(password)
        time.sleep(1)
        
        # Кликаем Submit
        try:
            submit_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
            )
            time.sleep(3)
        except:
            submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'login')]")
        
        submit_btn.click()
        time.sleep(4)
        
        print("✅ Логин успешен")
        print(f"📁 Переходу на страницу создания Offer...")
        
        # 2️⃣ Переходим на Create Offer
        driver.get(f"{keitaro_url}/offers/create")
        time.sleep(3)
        
        print("📝 Выбираю Local тип...")
        
        # 3️⃣ Выбираем Local тип (ищем radio button)
        try:
            local_radio = driver.find_element(By.XPATH, "//input[@value='local' and @type='radio']")
            local_radio.click()
        except:
            # Альтернативный селектор
            local_radio = driver.find_element(By.XPATH, "//label[contains(text(), 'Local')]/preceding-sibling::input")
            local_radio.click()
        
        time.sleep(1)
        
        print(f"✍️ Вписую имя: {offer_name}")
        
        # 4️⃣ Заполняем имя оффера
        try:
            name_field = driver.find_element(By.NAME, "name")
        except:
            name_field = driver.find_element(By.XPATH, "//input[@placeholder*='ame' or @placeholder*='Name']")
        
        name_field.send_keys(offer_name)
        time.sleep(1)
        
        print(f"📦 Загружаю ZIP файл: {zip_file_path}")
        
        # 5️⃣ Загружаем ZIP файл (ПОЛНЫЙ АБСОЛЮТНЫЙ ПУТЬ!)
        abs_path = os.path.abspath(zip_file_path)
        print(f"   Путь: {abs_path}")
        
        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        except:
            file_input = driver.find_element(By.XPATH, "//input[@accept*='zip']")
        
        file_input.send_keys(abs_path)
        time.sleep(4)
        
        print("🖱️ Кликаю Create...")
        
        # 6️⃣ Кликаем Create/Submit кнопку
        try:
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
        except:
            submit_btn = driver.find_element(By.XPATH, "//button[contains(text(), 'Create')]")
        
        submit_btn.click()
        time.sleep(6)
        
        print("⏳ Жду редиректа...")
        
        # 7️⃣ Извлекаем offer_id из URL или ждем загрузки
        current_url = driver.current_url
        print(f"   Текущий URL: {current_url}")
        
        # Ищем offer_id в URL: /offers/123 или /offers/123/edit
        if '/offers/' in current_url:
            parts = current_url.split('/offers/')
            if len(parts) > 1:
                offer_id = parts[1].split('/')[0]
                try:
                    offer_id = int(offer_id)
                    print(f"\n✅ Offer успешно создан!")
                    print(f"   Offer ID: {offer_id}")
                    return offer_id
                except:
                    pass
        
        # Если не нашли в URL, ищем в HTML (может быть в success message)
        page_source = driver.page_source
        if 'offer' in page_source.lower() and offer_name in page_source:
            print(f"✅ Offer создан (найден по контенту страницы)")
            # Пробуем парсить из других мест
            import re
            matches = re.findall(r'/offers/(\d+)', page_source)
            if matches:
                offer_id = int(matches[0])
                print(f"   Offer ID: {offer_id}")
                return offer_id
        
        print("❌ Не удалось извлечь offer_id")
        return None
        
    except Exception as e:
        print(f"❌ Ошибка Selenium: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        driver.quit()
        print("🔒 Браузер закрыт")
