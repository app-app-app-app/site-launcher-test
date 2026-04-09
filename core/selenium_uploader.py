"""
Selenium-based ZIP uploader for Keitaro
БЕЗ зависимости от webdriver-manager (максимальная совместимость)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os


def upload_zip_to_keitaro(keitaro_url, username, password, zip_file_path, offer_name):
    """
    Загружает ZIP в Keitaro через браузер вместо API
    
    Args:
        keitaro_url: URL Keitaro (например http://186.2.174.144)
        username: Логин админа
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
    options.add_argument('--disable-gpu')
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    
    driver = None
    
    try:
        print("\n" + "=" * 70)
        print("🚀 ЗАПУСКАЮ SELENIUM UPLOADER")
        print("=" * 70)
        print(f"📍 Keitaro URL: {keitaro_url}")
        print(f"👤 Username: {username}")
        print(f"🔑 Password: {'*' * min(len(password), 5)}")
        print(f"📦 ZIP file: {zip_file_path}")
        print(f"📝 Offer name: {offer_name}")
        print("=" * 70 + "\n")
        
        print("📥 Запускаю Chrome...")
        
        # Просто запускаем Chrome без webdriver-manager
        # Работает везде: Streamlit Cloud, localhost, Docker и т.д.
        driver = webdriver.Chrome(options=options)
        print("✅ Chrome запущен!")
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 1: ЛОГИН
        # ═══════════════════════════════════════════════════════════
        
        # Normalize URL
        if not keitaro_url.startswith('http'):
            keitaro_url = f'http://{keitaro_url}'
        
        print(f"🔐 КРОК 1: Логинюсь в Keitaro ({keitaro_url})...")
        
        login_url = f"{keitaro_url}/login"
        print(f"   Открываю: {login_url}")
        
        driver.get(login_url)
        print("   ⏳ Жду загрузки страницы (4 сек)...")
        time.sleep(4)
        print("   ✓ Страница загрузилась")
        
        print("✍️ Заполняю форму...")
        print(f"   Username: {username}")
        print(f"   Password: {'*' * len(password)}")
        
        # DEBUG: Сохраняем HTML для отладки
        print("\n🔍 DEBUG: HTML страницы логина:")
        print("-" * 60)
        page_html = driver.page_source
        # Показываем только важные части
        import re
        inputs = re.findall(r'<input[^>]*>', page_html)
        for inp in inputs:
            print(f"   {inp}")
        print("-" * 60 + "\n")
        
        # USERNAME - name="login" для Keitaro
        try:
            username_field = driver.find_element(By.NAME, "login")
            print("   ✓ Username field найдено (name='login')")
        except Exception as e:
            print(f"   ⚠️ name='login' не нашли: {e}")
            try:
                username_field = driver.find_element(By.XPATH, "//input[@type='text']")
                print("   ✓ Username field найдено (fallback xpath)")
            except Exception as e2:
                print(f"❌ Username field не найдено! Ошибка: {e2}")
                print(f"   HTML: {page_html[:1000]}")
                return None
        
        print(f"   Вводим username: {username}")
        username_field.clear()
        username_field.send_keys(username)
        time.sleep(0.5)
        
        # PASSWORD
        try:
            password_field = driver.find_element(By.NAME, "password")
            print("   ✓ Password field найдено (name='password')")
        except Exception as e:
            print(f"   ⚠️ name='password' не нашли: {e}")
            try:
                password_field = driver.find_element(By.XPATH, "//input[@type='password']")
                print("   ✓ Password field найдено (fallback xpath)")
            except Exception as e2:
                print(f"❌ Password field не найдено! Ошибка: {e2}")
                return None
        
        print(f"   Вводим пароль (скрыто)")
        password_field.clear()
        password_field.send_keys(password)
        time.sleep(0.5)
        
        # SUBMIT
        print("🖱 Отправляю форму...")
        submitted = False
        try:
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            print("   ✓ Submit button найдено")
            print("   Кликаю...")
            submit_btn.click()
            submitted = True
        except Exception as e:
            print(f"   ⚠️ Submit button error: {e}")
            print("   Использую ENTER...")
            password_field.send_keys("\n")
            submitted = True
        
        print("   ⏳ Жду редиректа (5 сек)...")
        time.sleep(5)
        
        # CHECK
        current_url = driver.current_url
        print(f"🌐 URL после логина: {current_url}")
        
        if '/login' in current_url:
            print("❌ LOGIN FAILED - Все ещё на странице логина!")
            print(f"\n🔍 DEBUG: Проверяю что случилось...")
            
            # Смотрим что на странице
            error_text = driver.find_elements(By.XPATH, "//*[contains(text(), 'error') or contains(text(), 'Error') or contains(text(), 'invalid')]")
            if error_text:
                print(f"   Error messages на странице:")
                for elem in error_text[:3]:
                    try:
                        print(f"   - {elem.text}")
                    except:
                        pass
            
            # Сохраняем HTML для отладки
            with open("/tmp/keitaro_login_debug.html", "w") as f:
                f.write(driver.page_source)
            print(f"   HTML страницы сохранен в /tmp/keitaro_login_debug.html")
            print(f"   Первые 500 chars: {driver.page_source[:500]}")
            
            return None
        
        print("✅ Логин успешен!")
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 2: CREATE OFFER PAGE
        # ═══════════════════════════════════════════════════════════
        
        print("📁 Переходу на создание Offer...")
        driver.get(f"{keitaro_url}/offers/create")
        time.sleep(3)
        
        # Выбираем Local
        print("📝 Выбираю Local...")
        try:
            local_radio = driver.find_element(By.XPATH, "//input[@value='local' and @type='radio']")
            local_radio.click()
            time.sleep(0.5)
        except:
            print("   ⚠️ Local option not found, continuing...")
        
        # Name field
        print(f"✍️ Вписую имя: {offer_name}")
        try:
            name_field = driver.find_element(By.NAME, "name")
            name_field.clear()
            name_field.send_keys(offer_name)
            time.sleep(0.5)
        except Exception as e:
            print(f"   ⚠️ Name field error: {e}")
        
        # ZIP upload
        print("📦 Загружаю ZIP...")
        abs_path = os.path.abspath(zip_file_path)
        
        if not os.path.exists(abs_path):
            print(f"❌ ZIP не найден: {abs_path}")
            return None
        
        try:
            file_input = driver.find_element(By.XPATH, "//input[@type='file']")
            file_input.send_keys(abs_path)
            print("   ✓ ZIP отправлен")
            time.sleep(4)
        except Exception as e:
            print(f"   ⚠️ File upload error: {e}")
        
        # Submit
        print("🖱 Создаю Offer...")
        try:
            submit_btn = driver.find_element(By.XPATH, "//button[@type='submit']")
            submit_btn.click()
            time.sleep(6)
        except:
            print("   ⚠️ Submit error")
        
        # ═══════════════════════════════════════════════════════════
        # КРОК 3: EXTRACT OFFER_ID
        # ═══════════════════════════════════════════════════════════
        
        current_url = driver.current_url
        print(f"🌐 Final URL: {current_url}")
        
        # Из URL
        if '/offers/' in current_url:
            parts = current_url.split('/offers/')
            if len(parts) > 1:
                try:
                    offer_id = int(parts[1].split('/')[0])
                    print(f"✅ Offer создан! ID: {offer_id}")
                    return offer_id
                except:
                    pass
        
        # Из HTML
        page_source = driver.page_source
        if 'offer' in page_source.lower():
            import re
            matches = re.findall(r'/offers/(\d+)', page_source)
            if matches:
                try:
                    offer_id = int(matches[0])
                    print(f"✅ Offer создан! ID: {offer_id}")
                    return offer_id
                except:
                    pass
        
        print("❌ Не смог извлечь offer_id")
        return None
    
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        return None
    finally:
        if driver:
            driver.quit()
            print("🔒 Browser закрыт")
