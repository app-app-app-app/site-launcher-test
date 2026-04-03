"""
Site Launch Pipeline с Selenium-based ZIP upload
Использует браузер для загрузки ZIP в Keitaro вместо неработающего API
"""

import io
import json
import tempfile
from typing import Optional, Callable, Dict, Any
from dataclasses import dataclass


@dataclass
class SiteLaunchConfig:
    """Конфиг для запуска сайта"""
    brand: str
    domain: str
    geo_code: str
    lang_code: str
    template_campaign_id: int = 373


def validate_config(config: SiteLaunchConfig) -> tuple[bool, str]:
    """Валидирует конфиг"""
    if not config.domain:
        return False, "Domain is required"
    if not config.template_campaign_id:
        return False, "Template campaign ID is required"
    return True, ""


class SiteLaunchPipeline:
    """
    Полный pipeline для запуска сайтов:
    1. Создание Offer через Selenium (ZIP upload)
    2. Клонирование Campaign через API
    3. Обновление Streams через API
    4. Логирование в Google Sheets
    """
    
    def __init__(self, keitaro_client, google_sheets_manager=None, 
                 keitaro_username="admin", keitaro_password=""):
        self.keitaro_client = keitaro_client
        self.sheets = google_sheets_manager
        self.keitaro_username = keitaro_username
        self.keitaro_password = keitaro_password
    
    def launch_site(self, 
                    brand: str,
                    domain: str,
                    geo_code: str,
                    lang_code: str,
                    zip_bytes: bytes,
                    template_campaign_id: int = 373,
                    progress_callback: Optional[Callable] = None) -> Dict[str, Any]:
        """
        ОСНОВНОЙ МЕТОД: Запускает сайт за один раз
        
        Args:
            brand: Бренд/имя платформы
            domain: Доменное имя
            geo_code: Код страны (CZ, AT и т.д.)
            lang_code: Код языка (cs-CZ, de-DE и т.д.)
            zip_bytes: ZIP файл в виде bytes
            template_campaign_id: ID кампании-шаблона для клонирования
            progress_callback: Функция для обновления прогресса: callback(percent, message)
        
        Returns:
            {
                "success": bool,
                "offer_id": int или None,
                "campaign_id": int или None,
                "errors": [str, ...],
                "status": str
            }
        """
        
        errors = []
        offer_id = None
        campaign_id = None
        
        def progress(percent, message):
            """Хелпер для прогресса"""
            if progress_callback:
                progress_callback(percent, message)
            print(f"[{percent}%] {message}")
        
        try:
            # ═══════════════════════════════════════════════════════════
            # КРОК 1: ZIP UPLOAD ЧЕРЕЗ SELENIUM (вместо API)
            # ═══════════════════════════════════════════════════════════
            progress(10, f"📦 Загружаю ZIP {domain} через браузер...")
            
            # Импортируем Selenium uploader
            from core.selenium_uploader import upload_zip_to_keitaro
            
            # Сохраняем ZIP временно
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as f:
                f.write(zip_bytes)
                temp_zip_path = f.name
            
            # Загружаем через Selenium
            offer_id = upload_zip_to_keitaro(
                keitaro_url=self.keitaro_client.base_url,
                username=self.keitaro_username,
                password=self.keitaro_password,
                zip_file_path=temp_zip_path,
                offer_name=domain
            )
            
            if not offer_id:
                errors.append("❌ Failed to upload ZIP via Selenium")
                return {
                    "success": False,
                    "offer_id": None,
                    "campaign_id": None,
                    "errors": errors,
                    "status": "UPLOAD_FAILED"
                }
            
            progress(25, f"✅ Offer {offer_id} создан через Selenium")
            
            # ═══════════════════════════════════════════════════════════
            # КРОК 2: КЛОНУВАННЯ CAMPAIGN ЧЕРЕЗ API
            # ═══════════════════════════════════════════════════════════
            progress(40, f"📋 Клонирую campaign {template_campaign_id}...")
            
            try:
                campaign = self.keitaro_client.clone_campaign(
                    template_id=template_campaign_id,
                    new_name=domain
                )
                campaign_id = campaign.get('id')
                
                if not campaign_id:
                    errors.append(f"❌ Failed to clone campaign, got: {campaign}")
                    return {
                        "success": False,
                        "offer_id": offer_id,
                        "campaign_id": None,
                        "errors": errors,
                        "status": "CAMPAIGN_CLONE_FAILED"
                    }
                
                progress(55, f"✅ Campaign {campaign_id} клонирован")
            
            except Exception as e:
                errors.append(f"❌ Campaign clone error: {str(e)}")
                return {
                    "success": False,
                    "offer_id": offer_id,
                    "campaign_id": None,
                    "errors": errors,
                    "status": "CAMPAIGN_CLONE_ERROR"
                }
            
            # ═══════════════════════════════════════════════════════════
            # КРОК 3: ОНОВЛЕННЯ CAMPAIGN METADATA
            # ═══════════════════════════════════════════════════════════
            progress(65, f"🔧 Обновляю metadata campaign...")
            
            try:
                self.keitaro_client.update_campaign(campaign_id, {
                    'name': domain,
                    'alias': domain.replace('.', '-')
                })
                progress(70, f"✅ Campaign metadata обновлен")
            
            except Exception as e:
                # Не критично, продолжаем
                print(f"⚠️  Campaign update warning: {e}")
            
            # ═══════════════════════════════════════════════════════════
            # КРОК 4: ОНОВЛЕННЯ STREAMS
            # ═══════════════════════════════════════════════════════════
            progress(75, f"🌊 Обновляю streams...")
            
            try:
                streams = self.keitaro_client.get_streams(campaign_id)
                
                for stream in streams:
                    self.keitaro_client.update_stream(stream['id'], offer_id)
                
                progress(85, f"✅ {len(streams)} streams обновлены с offer_id={offer_id}")
            
            except Exception as e:
                errors.append(f"⚠️  Stream update warning: {str(e)}")
                # Не критично, продолжаем
                print(f"Stream warning: {e}")
            
            # ═══════════════════════════════════════════════════════════
            # КРОК 5: ЛОГИРОВАНИЕ В GOOGLE SHEETS
            # ═══════════════════════════════════════════════════════════
            progress(90, f"📊 Логирую в Google Sheets...")
            
            if self.sheets:
                try:
                    self.sheets.add_row(
                        brand=brand or domain,
                        domain=domain,
                        geo=geo_code,
                        lang=lang_code,
                        template=template_campaign_id,
                        status="LAUNCHED",
                        offer_id=offer_id,
                        campaign_id=campaign_id,
                        error_message=""
                    )
                    progress(95, f"✅ Записано в Google Sheets")
                
                except Exception as e:
                    print(f"⚠️  Google Sheets warning: {e}")
                    # Не критично, продолжаем
            
            # ═══════════════════════════════════════════════════════════
            # УСПЕХ!
            # ═══════════════════════════════════════════════════════════
            progress(100, f"✅ {domain} успешно запущен!")
            
            return {
                "success": True,
                "offer_id": offer_id,
                "campaign_id": campaign_id,
                "errors": errors,
                "status": "LAUNCHED"
            }
        
        except Exception as e:
            errors.append(f"❌ Critical error: {str(e)}")
            import traceback
            print(traceback.format_exc())
            
            return {
                "success": False,
                "offer_id": offer_id,
                "campaign_id": campaign_id,
                "errors": errors,
                "status": "CRITICAL_ERROR"
            }
