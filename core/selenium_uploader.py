"""
Selenium-based ZIP uploader for Keitaro
Загружает ZIP файлы в Keitaro через веб-интерфейс (обходит неработающий API)

РАБОТАЕТ НА:
- Локальном компьютере (Windows/macOS/Linux)
- Streamlit Cloud
- Других хостингах с Chrome/Chromium
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# Conditional import для webdriver_manager (может не быть на Streamlit Cloud)
try:
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    WEBDRIVER_MANAGER_AVAILABLE = True
except ImportError:
    WEBDRIVER_MANAGER_AVAILABLE = False


def upload_zip_to_keitaro(keitaro_url, username, password, zip_file_path, offer_name):
    """
    Загружает ZIP в Keitaro через браузер вместо API
    
    Args:
        keitaro_url: URL Keitaro (например https://твой-keitaro.com)
        username: Логин админа (для Keitaro: обычно "admin")
        password: Пароль админа
        zip_file_path: Полный путь к ZIP файлу
        offer_name: Имя оффера (обычно домен)
    
    Returns:
        offer_id (int) или None если ошибка
    """
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--no-first-run')
    options.add_argument('--no-default-browser-check')
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-dev-tools')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    # ИНИЦИАЛИЗАЦИЯ WEBDRIVER
    driver = None
    try:
        print("📥 Инициализирую Chrome WebDriver...")
        
        # Способ 1: webdriver_manager (если доступен)
        if WEBDRIVER_MANAGER_AVAILABLE:
            try:
                from selenium.webdriver.chrome.service import Service
                service = Service(ChromeDriverManager().install())
                driver = webdriver.Chrome(service=service, options=options)
                print("✓ WebDriver инициализирован через webdriver_manager")
            except Exception as e:
                print(f"⚠️  webdriver_manager failed ({e}), trying fallback...")
                driver = None
        
        # Способ 2: Прямой запуск Chrome (для Streamlit Cloud)
        if driver is None:
            try:
                driver = webdriver.Chrome(options=options)
                print("✓ WebDriver инициализирован напрямую")
            except Exception as e:
                print(f"❌ Chrome инициализация не удалась: {e}")
                return None
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 1: ЛОГИН В KEITARO
        # ═══════════════════════════════════════════════════════════
        
        # Normalize URL
        if not keitaro_url.startswith('http'):
            keitaro_url = f'http://{keitaro_url}'
        
        print(f"🔐 Логинюсь в Keitaro ({keitaro_url})...")
        
        login_url = f"{keitaro_url}/login" if not keitaro_url.endswith('/login') else keitaro_url
        print(f"   Opening: {login_url}")
        
        driver.get(login_url)
        time.sleep(4)
        
        # Проверяем что страница загрузилась
        page_source = driver.page_source
        if not page_source or len(page_source) < 100:
            print("❌ Login page не загрузилась!")
            return None
        
        print("✍️ Заполняю форму входа...")
        
        # USERNAME поле - ГЛАВНЫЙ СЕЛЕКТОР ДЛЯ KEITARO: name="login"
        username_field = None
        username_selectors = [
            (By.NAME, "login"),  # ← KEITARO использует "login"
            (By.NAME, "username"),
            (By.XPATH, "//input[@type='text'][1]"),
        ]
        
        for by_type, selector in username_selectors:
            try:
                username_field = driver.find_element(by_type, selector)
                print(f"   ✓ Username field найдено: {by_type}={selector}")
                break
            except:
                pass
        
        if not username_field:
            print("❌ Username field не найдено!")
            return None
        
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(0.5)
        
        # PASSWORD поле
        print("🔑 Заполняю пароль...")
        
        password_field = None
        password_selectors = [
            (By.NAME, "password"),
            (By.XPATH, "//input[@type='password']"),
        ]
        
        for by_type, selector in password_selectors:
            try:
                password_field = driver.find_element(by_type, selector)
                print(f"   ✓ Password field найдено: {by_type}={selector}")
                break
            except:
                pass
        
        if not password_field:
            print("❌ Password field не найдено!")
            return None
        
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)
        
        # SUBMIT КНОПКА
        print("🖱 Отправляю форму...")
        
        submitted = False
        submit_selectors = [
            (By.XPATH, "//button[@type='submit']"),
            (By.XPATH, "//button"),
        ]
        
        for by_type, selector in submit_selectors:
            try:
                submit_btn = driver.find_element(by_type, selector)
                print(f"   ✓ Submit button найдено: {by_type}={selector}")
                submit_btn.click()
                submitted = True
                break
            except:
                pass
        
        if not submitted:
            print("   Using ENTER key...")
            password_field.send_keys("\n")
        
        time.sleep(5)
        
        # ПРОВЕРКА РЕЗУЛЬТАТА ЛОГИНА
        current_url = driver.current_url
        print(f"🌐 URL после логина: {current_url}")
        
        if '/login' in current_url:
            print("❌ LOGIN FAILED - Все ещё на странице логина!")
            print(f"   Проверь username/password")
            return None
        
        print("✅ Логин успешен!")
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 2: ПЕРЕХОД НА СТРАНИЦУ СОЗДАНИЯ OFFER
        # ═══════════════════════════════════════════════════════════
        
        print(f"📁 Переходу на страницу создания Offer...")
        driver.get(f"{keitaro_url}/offers/create")
        time.sleep(3)
        
        print("📝 Выбираю Local тип...")
        
        # Выбираем Local тип
        try:
            local_radio = driver.find_element(By.XPATH, "//input[@value='local' and @type='radio']")
            local_radio.click()
        except:
            try:
                local_radio = driver.find_element(By.XPATH, "//label[contains(text(), 'Local')]/preceding-sibling::input")
                local_radio.click()
            except:
                print("⚠️  Не смог выбрать Local, пробую дальше...")
        
        time.sleep(1)
        
        print(f"✍️ Вписую имя: {offer_name}")
        
        # Заполняем имя оффера
        name_field = None
        name_selectors = [
            (By.NAME, "name"),
            (By.XPATH, "//input[@placeholder*='Name' or @placeholder*='name']"),
        ]
        
        for by_type, selector in name_selectors:
            try:
                name_field = driver.find_element(by_type, selector)
                print(f"   ✓ Name field найдено: {by_type}={selector}")
                break
            except:
                pass
        
        if name_field:
            name_field.clear()
            name_field.send_keys(offer_name)
            time.sleep(0.5)
        else:
            print("⚠️  Name field не найдено, продолжаю...")
        
        print(f"📦 Загружаю ZIP файл...")
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 3: ЗАГРУЗКА ZIP
        # ═══════════════════════════════════════════════════════════
        
        abs_path = os.path.abspath(zip_file_path)
        print(f"   Путь: {abs_path}")
        
        if not os.path.exists(abs_path):
            print(f"❌ ZIP файл не найдено: {abs_path}")
            return None
        
        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            print(f"   ✓ File input найдено")
            file_input.send_keys(abs_path)
            time.sleep(4)
        except Exception as e:
            print(f"⚠️  File upload problem: {e}")
            pass
        
        print("🖱 Кликаю Create...")
        
        try:
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            time.sleep(6)
        except:
            print("⚠️  Submit button not found after file upload")
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 4: ИЗВЛЕЧЕНИЕ OFFER_ID
        # ═══════════════════════════════════════════════════════════
        
        print("⏳ Парсю результат...")
        
        current_url = driver.current_url
        print(f"🌐 Final URL: {current_url}")
        
        # Пробуем найти offer_id в URL
        if '/offers/' in current_url:
            parts = current_url.split('/offers/')
            if len(parts) > 1:
                offer_id_str = parts[1].split('/')[0]
                try:
                    offer_id = int(offer_id_str)
                    print(f"\n✅ Offer успешно создан!")
                    print(f"   Offer ID: {offer_id}")
                    return offer_id
                except:
                    pass
        
        # Пробуем найти в HTML
        page_source = driver.page_source
        if 'offer' in page_source.lower():
            import re
            matches = re.findall(r'/offers/(\d+)', page_source)
            if matches:
                offer_id = int(matches[0])
                print(f"\n✅ Offer успешно создан!")
                print(f"   Offer ID: {offer_id}")
                return offer_id
        
        print("❌ Не смог извлечь offer_id из URL или HTML")
        return None
    
    except Exception as e:
        print(f"❌ Критична ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser закрыт")
