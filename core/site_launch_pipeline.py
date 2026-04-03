"""
Site Launch Pipeline
====================

Повностю автоматизований pipeline для запуску сайтів в Keitaro:
1. Google Sheets → Add row
2. Create Offer
3. Upload ZIP
4. Clone Campaign
5. Update Streams
"""

import time
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import logging

from core.keitaro_api import KeitaroClient, upload_zip_to_offer, KeitaroAPIError

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class SiteLaunchConfig:
    """Configuration for site launch"""
    brand: str
    domain: str
    geo_code: str
    lang_code: str
    
    # Keitaro settings
    template_campaign_id: Optional[int] = None  # ID of campaign to clone from
    group_id_offer: int = 3
    group_id_campaign: int = 2


class SiteLaunchPipeline:
    """
    Complete site launch pipeline
    
    Usage:
        pipeline = SiteLaunchPipeline(client, sheets_manager, config)
        result = pipeline.launch_site(brand, domain, geo, lang)
    """
    
    def __init__(
        self,
        keitaro_client: KeitaroClient,
        google_sheets_manager=None  # Your Google Sheets manager
    ):
        """
        Initialize pipeline
        
        Args:
            keitaro_client: KeitaroClient instance
            google_sheets_manager: Your Google Sheets integration (optional)
        """
        self.selenium_uploader = None  # Будет инициализирован при необходимости
        self.client = keitaro_client
        self.sheets = google_sheets_manager
    
    def launch_site(
        self,
        brand: str,
        domain: str,
        geo_code: str,
        lang_code: str,
        zip_bytes: bytes,
        template_campaign_id: Optional[int] = None,
        progress_callback=None
    ) -> Dict:
        """
        Launch a single site
        
        Steps:
        1. Add to Google Sheets
        2. Create Offer
        3. Upload ZIP
        4. Clone Campaign
        5. Update Streams
        
        Args:
            brand: Brand name
            domain: Domain name
            geo_code: Geographic code (e.g., "UA", "US")
            lang_code: Language code (e.g., "uk", "en")
            zip_bytes: ZIP file content
            template_campaign_id: Template campaign to clone from
            progress_callback: Callback for progress updates
        
        Returns:
            Dict with results: {
                "success": bool,
                "offer_id": int,
                "campaign_id": int,
                "errors": [str]
            }
        """
        
        result = {
            "success": False,
            "offer_id": None,
            "campaign_id": None,
            "errors": []
        }
        
        try:
            # === STEP 1: Google Sheets ===
            if self._progress(progress_callback, 10, f"📝 Adding to Google Sheets..."):
                self._add_to_sheets(brand, domain, geo_code, lang_code)
            
            # === STEP 2: Create Offer ===
            if self._progress(progress_callback, 20, f"📦 Creating offer for {domain}..."):
                offer = self._create_offer(domain)
                offer_id = offer.get("id") or offer.get("data", {}).get("id")
                
                if not offer_id:
                    raise KeitaroAPIError("Failed to create offer: no ID returned")
                
                result["offer_id"] = offer_id
                logger.info(f"✅ Offer created: {offer_id}")
            
            # === КРОК 1: ZIP Upload via Selenium ===
            from .selenium_uploader import upload_zip_to_keitaro
            import tempfile
            
            # Сохраняем ZIP во временный файл
            with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as f:
                f.write(zip_bytes)
                temp_zip_path = f.name
            
            # Загружаем через браузер вместо API
            offer_id = upload_zip_to_keitaro(
                keitaro_url=self.keitaro_client.base_url,
                username="твой_логин",  # ← ЗАМЕНИ НА СВОЙ
                password="твой_пароль",  # ← ЗАМЕНИ НА СВОЙ
                zip_file_path=temp_zip_path,
                offer_name=domain
            )
            
            if not offer_id:
                return {
                    "success": False,
                    "errors": ["Failed to upload ZIP via Selenium"]
                }
            
            print(f"✅ Offer {offer_id} created via Selenium")
            
            # === STEP 4: Clone Campaign (if template provided) ===
            if template_campaign_id:
                if self._progress(progress_callback, 60, f"📋 Cloning campaign..."):
                    campaign = self._clone_campaign(template_campaign_id, domain)
                    campaign_id = campaign.get("id")
                    
                    if not campaign_id:
                        raise KeitaroAPIError("Failed to clone campaign: no ID returned")
                    
                    result["campaign_id"] = campaign_id
                    logger.info(f"✅ Campaign cloned: {campaign_id}")
                
                # === STEP 5: Update Campaign Meta ===
                if self._progress(progress_callback, 70, f"⚙️ Updating campaign..."):
                    self._update_campaign_meta(campaign_id, domain)
                
                # === STEP 6: Get Streams ===
                if self._progress(progress_callback, 80, f"🔗 Linking offer to campaign..."):
                    streams = self._get_streams(campaign_id)
                    
                    if not streams:
                        raise KeitaroAPIError("Campaign has no streams")
                    
                    stream_id = streams[0].get("id")
                    
                    if not stream_id:
                        raise KeitaroAPIError("Stream has no ID")
                
                # === STEP 7: Update Stream ===
                if self._progress(progress_callback, 90, f"🎯 Assigning offer to stream..."):
                    self._update_stream(stream_id, offer_id)
                    logger.info(f"✅ Stream updated: offer {offer_id} assigned")
            
            # === FINAL ===
            if self._progress(progress_callback, 100, f"✅ Site launched!"):
                result["success"] = True
            
        except Exception as e:
            error_msg = str(e)
            result["errors"].append(error_msg)
            logger.error(f"❌ Pipeline failed: {error_msg}")
        
        return result
    
    def launch_batch(
        self,
        sites: List[SiteLaunchConfig],
        zip_files: Dict[str, bytes],
        template_campaign_id: Optional[int] = None,
        progress_callback=None
    ) -> List[Dict]:
        """
        Launch multiple sites
        
        Args:
            sites: List of SiteLaunchConfig objects
            zip_files: Dict mapping domain -> zip_bytes
            template_campaign_id: Template campaign to clone from
            progress_callback: Callback for progress
        
        Returns:
            List of results for each site
        """
        
        results = []
        total = len(sites)
        
        for i, config in enumerate(sites, 1):
            progress = int((i - 1) / total * 100)
            
            if progress_callback:
                progress_callback(progress, f"Processing {i}/{total}: {config.domain}")
            
            logger.info(f"--- [{i}/{total}] Launching {config.domain} ---")
            
            zip_bytes = zip_files.get(config.domain)
            
            if not zip_bytes:
                logger.warning(f"⚠️  No ZIP for {config.domain}, skipping")
                results.append({
                    "domain": config.domain,
                    "success": False,
                    "error": "No ZIP file provided"
                })
                continue
            
            result = self.launch_site(
                brand=config.brand,
                domain=config.domain,
                geo_code=config.geo_code,
                lang_code=config.lang_code,
                zip_bytes=zip_bytes,
                template_campaign_id=template_campaign_id,
                progress_callback=None  # Disable nested callback
            )
            
            result["domain"] = config.domain
            results.append(result)
            
            # Small delay between launches
            time.sleep(1)
        
        return results
    
    # ========================
    # PRIVATE METHODS
    # ========================
    
    def _progress(self, callback, percent: int, message: str) -> bool:
        """Helper to call progress callback"""
        if callback:
            callback(percent, message)
        return True
    
    def _add_to_sheets(self, brand: str, domain: str, geo_code: str, lang_code: str):
        """Add row to Google Sheets"""
        if not self.sheets:
            logger.warning("⚠️  Google Sheets manager not configured")
            return
        
        try:
            self.sheets.add_row(
                brand=brand,
                domain=domain,
                geo_code=geo_code,
                lang_code=lang_code
            )
            logger.info("✅ Added to Google Sheets")
        except Exception as e:
            logger.warning(f"⚠️  Could not add to Sheets: {e}")
    
    def _create_offer(self, domain: str) -> Dict:
        """Create new offer"""
        logger.info(f"Creating offer for {domain}...")
        
        offer = self.client.create_offer(
            name=domain,
            group_id=3,
            offer_type="local",
            action_type="local"
        )
        
        logger.debug(f"Offer response: {offer}")
        return offer
    
    def _upload_zip(self, offer_id: int, zip_bytes: bytes) -> bool:
        """Upload ZIP to offer"""
        logger.info(f"Uploading ZIP to offer {offer_id}...")
        
        success = upload_zip_to_offer(
            self.client,
            offer_id,
            zip_bytes,
            verbose=True
        )
        
        return success
    
    def _clone_campaign(self, template_id: int, domain: str) -> Dict:
        """Clone campaign from template"""
        logger.info(f"Cloning campaign {template_id} with name {domain}...")
        
        campaign = self.client.clone_campaign(
            template_campaign_id=template_id,
            new_name=domain
        )
        
        logger.debug(f"Campaign response: {campaign}")
        return campaign
    
    def _update_campaign_meta(self, campaign_id: int, domain: str):
        """Update campaign metadata"""
        logger.info(f"Updating campaign {campaign_id} metadata...")
        
        alias = domain.replace(".", "-") + "-" + str(int(time.time()))
        
        self.client.update_campaign(
            campaign_id=campaign_id,
            data={
                "name": domain,
                "alias": alias,
                "group_id": 2
            }
        )
    
    def _get_streams(self, campaign_id: int) -> List[Dict]:
        """Get campaign streams"""
        logger.info(f"Getting streams for campaign {campaign_id}...")
        
        streams = self.client.get_streams(campaign_id)
        
        if not streams:
            logger.warning(f"⚠️  Campaign {campaign_id} has no streams")
        
        return streams
    
    def _update_stream(self, stream_id: int, offer_id: int):
        """Update stream with offer"""
        logger.info(f"Assigning offer {offer_id} to stream {stream_id}...")
        
        self.client.update_stream(
            stream_id=stream_id,
            offer_id=offer_id,
            weight=100,
            position=1
        )


# ========================
# UTILITY FUNCTIONS
# ========================

def validate_config(config: SiteLaunchConfig) -> Tuple[bool, List[str]]:
    """
    Validate site launch configuration
    
    Returns:
        (is_valid, errors)
    """
    errors = []
    
    if not config.brand or not config.brand.strip():
        errors.append("Brand is required")
    
    if not config.domain or not config.domain.strip():
        errors.append("Domain is required")
    
    if not config.geo_code or not config.geo_code.strip():
        errors.append("Geo code is required")
    
    if not config.lang_code or not config.lang_code.strip():
        errors.append("Language code is required")
    
    # Validate domain format
    if "." not in config.domain:
        errors.append(f"Invalid domain: {config.domain}")
    
    return len(errors) == 0, errors


def print_results(results: List[Dict]):
    """Pretty print results"""
    print("\n" + "=" * 60)
    print("LAUNCH RESULTS")
    print("=" * 60)
    
    success_count = sum(1 for r in results if r.get("success"))
    total = len(results)
    
    for result in results:
        domain = result.get("domain", "?")
        success = result.get("success")
        
        if success:
            print(f"✅ {domain}")
            print(f"   Offer ID: {result.get('offer_id')}")
            print(f"   Campaign ID: {result.get('campaign_id')}")
        else:
            print(f"❌ {domain}")
            errors = result.get("errors", [])
            for error in errors:
                print(f"   • {error}")
    
    print("-" * 60)
    print(f"Summary: {success_count}/{total} successful")
    print("=" * 60 + "\n")
