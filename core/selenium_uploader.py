from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os

def upload_zip_to_keitaro(keitaro_url, username, password, zip_file_path, offer_name):
    """Загружает ZIP в Keitaro через браузер вместо API"""
    
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    
    driver = webdriver.Chrome(options=options)
    
    try:
        # 1. Логин
        driver.get(f"{keitaro_url}/login")
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys(username)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(3)
        
        # 2. Переходим на Create Offer
        driver.get(f"{keitaro_url}/offers/create")
        time.sleep(2)
        
        # 3. Выбираем Local тип
        driver.find_element(By.XPATH, "//input[@value='local']").click()
        time.sleep(1)
        
        # 4. Пишем имя
        driver.find_element(By.NAME, "name").send_keys(offer_name)
        time.sleep(1)
        
        # 5. Загружаем ZIP
        file_input = driver.find_element(By.XPATH, "//input[@type='file']")
        file_input.send_keys(os.path.abspath(zip_file_path))
        time.sleep(3)
        
        # 6. Кликаем Create
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(5)
        
        # 7. Получаем offer_id
        current_url = driver.current_url
        offer_id = current_url.split('/offers/')[-1].split('/')[0]
        
        return int(offer_id)
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return None
    finally:
        driver.quit()
