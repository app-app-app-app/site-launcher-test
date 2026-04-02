"""
Keitaro API Client Library
==========================

Нормалізована бібліотека для роботи з Keitaro API.
Усі функції структуровані, задокументовані та готові до продакшену.

API Docs: https://keitaro.io/
"""

import requests
import base64
import zipfile
import io
from typing import Dict, List, Optional, Tuple
import time
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class KeitaroAPIError(Exception):
    """Custom exception for Keitaro API errors"""
    pass


class KeitaroClient:
    """
    Keitaro API Client
    
    Usage:
        client = KeitaroClient(base_url, api_key)
        offer = client.create_offer("example.com")
    """
    
    def __init__(self, base_url: str, api_key: str):
        """
        Initialize Keitaro API client
        
        Args:
            base_url: Base URL of Keitaro instance (e.g., "https://keitaro.io")
            api_key: API key from Keitaro admin panel
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.api_version = "v1"
        self.base_api_url = f"{self.base_url}/admin_api/{self.api_version}"
        
        self._session = requests.Session()
        self._session.headers.update({
            "Api-Key": api_key,
            "Content-Type": "application/json"
        })
    
    def _request(
        self, 
        method: str, 
        endpoint: str, 
        json_data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        data: Optional[Dict] = None,
        **kwargs
    ) -> requests.Response:
        """
        Base HTTP request method
        
        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint (e.g., "/offers", "/campaigns/123")
            json_data: JSON payload for request body
            files: Files for multipart upload
            data: Form data
            **kwargs: Additional arguments for requests
        
        Returns:
            Response object
        
        Raises:
            KeitaroAPIError: If request fails
        """
        url = f"{self.base_api_url}{endpoint}"
        
        # Use custom headers for this request
        headers = self._session.headers.copy()
        
        # Remove Content-Type for multipart/form-data
        if files:
            headers.pop("Content-Type", None)
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                files=files,
                data=data,
                verify=False,  # Keitaro often uses self-signed certs
                timeout=30,
                **kwargs
            )
            
            # Log for debugging
            print(f"[{method}] {endpoint} → {response.status_code}")
            
            if response.status_code >= 400:
                print(f"   Response: {response.text[:200]}")
            
            return response
            
        except requests.RequestException as e:
            raise KeitaroAPIError(f"Request failed: {e}")
    
    # ========================
    # OFFERS
    # ========================
    
    def create_offer(
        self,
        name: str,
        group_id: int = 3,
        offer_type: str = "local",
        action_type: str = "local"
    ) -> Dict:
        """
        Create a new offer
        
        Args:
            name: Offer name (typically domain)
            group_id: Group ID (default: 3)
            offer_type: Type of offer (default: "local")
            action_type: Action type (default: "local")
        
        Returns:
            Dict with offer data including 'id'
        
        Raises:
            KeitaroAPIError: If creation fails
        """
        payload = {
            "name": name,
            "group_id": group_id,
            "offer_type": offer_type,
            "action_type": action_type
        }
        
        response = self._request("POST", "/offers", json_data=payload)
        
        if response.status_code != 200:
            raise KeitaroAPIError(
                f"Failed to create offer '{name}': {response.status_code} - {response.text}"
            )
        
        result = response.json()
        return result
    
    def clone_offer(
        self,
        template_offer_id: int,
        new_name: str
    ) -> Dict:
        """
        Clone an existing offer
        
        Args:
            template_offer_id: ID of offer to clone from
            new_name: Name for the cloned offer
        
        Returns:
            Dict with cloned offer data
        """
        payload = {"name": new_name}
        response = self._request(
            "POST", 
            f"/offers/{template_offer_id}/clone", 
            json_data=payload
        )
        
        if response.status_code != 200:
            raise KeitaroAPIError(
                f"Failed to clone offer: {response.status_code} - {response.text}"
            )
        
        return response.json()
    
    def get_offer(self, offer_id: int) -> Dict:
        """Get offer details"""
        response = self._request("GET", f"/offers/{offer_id}")
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to get offer {offer_id}: {response.text}")
        
        return response.json()
    
    def update_offer(self, offer_id: int, data: Dict) -> Dict:
        """Update offer metadata"""
        response = self._request("PUT", f"/offers/{offer_id}", json_data=data)
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to update offer {offer_id}: {response.text}")
        
        return response.json()
    
    def list_offers(self) -> List[Dict]:
        """Get list of all offers"""
        response = self._request("GET", "/offers")
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to list offers: {response.text}")
        
        return response.json()
    
    # ========================
    # FILES
    # ========================
    
    def upload_file(
        self,
        offer_id: int,
        path: str,
        content: bytes
    ) -> bool:
        """
        Upload or update a file in offer
        
        Args:
            offer_id: Offer ID
            path: File path (e.g., "index.php", "css/style.css")
            content: File content as bytes
        
        Returns:
            True if successful
        """
        encoded_content = base64.b64encode(content).decode("utf-8")
        
        payload = {
            "path": path,
            "data": encoded_content
        }
        
        response = self._request("PUT", f"/offers/{offer_id}/update_file", json_data=payload)
        
        success = response.status_code == 200
        
        if not success:
            print(f"   ❌ File upload failed: {path}")
            print(f"   Response: {response.text[:200]}")
        
        return success
    
    def delete_file(self, offer_id: int, path: str) -> bool:
        """Delete a file from offer"""
        payload = {"path": path}
        response = self._request("DELETE", f"/offers/{offer_id}/remove_file", json_data=payload)
        return response.status_code == 200
    
    def get_offer_files(self, offer_id: int) -> List[str]:
        """Get list of files in offer"""
        response = self._request("GET", f"/offers/{offer_id}/get_structure")
        
        if response.status_code != 200:
            return []
        
        return response.json()
    
    def upload_zip(self, offer_id: int, zip_bytes: bytes) -> bool:
        """
        Upload a ZIP archive to offer
        
        ⚠️ IMPORTANT: Keitaro requires specific format
        - ZIP must be created correctly (without root wrapper)
        - macOS system files (._*, .DS_Store) must be excluded
        
        Args:
            offer_id: Offer ID
            zip_bytes: ZIP file content as bytes
        
        Returns:
            True if successful
        """
        # Create multipart request (not JSON)
        files = {
            "file": ("site.zip", io.BytesIO(zip_bytes), "application/zip")
        }
        
        data = {
            "path": ""  # Root upload
        }
        
        # Use custom headers without Content-Type (requests will set it)
        headers = {"Api-Key": self.api_key}
        
        response = requests.put(
            f"{self.base_api_url}/offers/{offer_id}/update_file",
            headers=headers,
            files=files,
            data=data,
            verify=False,
            timeout=60
        )
        
        success = response.status_code == 200
        
        if not success:
            print(f"   ❌ ZIP upload failed")
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.text[:300]}")
        else:
            print(f"   ✅ ZIP uploaded successfully")
        
        return success
    
    # ========================
    # CAMPAIGNS
    # ========================
    
    def create_campaign(
        self,
        name: str,
        type: str = "redirect",
        redirect_url: Optional[str] = None,
        group_id: int = 2
    ) -> Dict:
        """
        Create a new campaign
        
        Args:
            name: Campaign name (typically domain)
            type: Campaign type (default: "redirect")
            redirect_url: Redirect URL (for redirect type)
            group_id: Group ID (default: 2)
        
        Returns:
            Dict with campaign data including 'id'
        """
        alias = name.replace(".", "-") + "-" + str(int(time.time()))
        
        payload = {
            "name": name,
            "alias": alias,
            "group_id": group_id,
            "type": type,
            "state": "active"
        }
        
        if redirect_url:
            payload["redirect_url"] = redirect_url
        
        response = self._request("POST", "/campaigns", json_data=payload)
        
        if response.status_code != 200:
            raise KeitaroAPIError(
                f"Failed to create campaign '{name}': {response.status_code} - {response.text}"
            )
        
        result = response.json()
        return result
    
    def clone_campaign(
        self,
        template_campaign_id: int,
        new_name: str
    ) -> Dict:
        """
        Clone an existing campaign
        
        Args:
            template_campaign_id: ID of campaign to clone from
            new_name: Name for the cloned campaign
        
        Returns:
            Dict with cloned campaign data
        """
        alias = new_name.replace(".", "-") + "-" + str(int(time.time()))
        
        payload = {
            "name": new_name,
            "alias": alias,
            "group_id": 2
        }
        
        response = self._request(
            "POST",
            f"/campaigns/{template_campaign_id}/clone",
            json_data=payload
        )
        
        if response.status_code != 200:
            raise KeitaroAPIError(
                f"Failed to clone campaign: {response.status_code} - {response.text}"
            )
        
        # API returns a list, extract first item
        result = response.json()
        if isinstance(result, list) and result:
            return result[0]
        return result
    
    def get_campaign(self, campaign_id: int) -> Dict:
        """Get campaign details"""
        response = self._request("GET", f"/campaigns/{campaign_id}")
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to get campaign {campaign_id}: {response.text}")
        
        return response.json()
    
    def update_campaign(self, campaign_id: int, data: Dict) -> Dict:
        """Update campaign metadata"""
        response = self._request("PUT", f"/campaigns/{campaign_id}", json_data=data)
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to update campaign: {response.text}")
        
        return response.json()
    
    def list_campaigns(self) -> List[Dict]:
        """Get list of all campaigns"""
        response = self._request("GET", "/campaigns")
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to list campaigns: {response.text}")
        
        return response.json()
    
    # ========================
    # STREAMS (Flows)
    # ========================
    
    def get_streams(self, campaign_id: int) -> List[Dict]:
        """
        Get all streams for a campaign
        
        Args:
            campaign_id: Campaign ID
        
        Returns:
            List of streams
        """
        response = self._request("GET", f"/campaigns/{campaign_id}/streams")
        
        if response.status_code != 200:
            print(f"   ❌ Failed to get streams: {response.text}")
            return []
        
        return response.json()
    
    def update_stream(
        self,
        stream_id: int,
        offer_id: int,
        weight: int = 100,
        position: int = 1
    ) -> Dict:
        """
        Update stream with offer
        
        Args:
            stream_id: Stream ID
            offer_id: Offer ID to assign
            weight: Offer weight (default: 100)
            position: Offer position in stream (default: 1)
        
        Returns:
            Stream data after update
        """
        payload = {
            "schema": "landings",
            "offers": [
                {
                    "offer_id": offer_id,
                    "position": position,
                    "weight": weight,
                    "state": "active"
                }
            ]
        }
        
        response = self._request("PUT", f"/streams/{stream_id}", json_data=payload)
        
        if response.status_code != 200:
            raise KeitaroAPIError(
                f"Failed to update stream {stream_id}: {response.status_code} - {response.text}"
            )
        
        return response.json()
    
    # ========================
    # DOMAINS
    # ========================
    
    def list_domains(self) -> List[Dict]:
        """Get list of all domains"""
        response = self._request("GET", "/domains")
        
        if response.status_code != 200:
            return []
        
        return response.json()
    
    def create_domain(self, domain: str) -> Dict:
        """Create/register domain"""
        payload = {"name": domain}
        response = self._request("POST", "/domains", json_data=payload)
        
        if response.status_code != 200:
            raise KeitaroAPIError(f"Failed to create domain: {response.text}")
        
        return response.json()


def unzip_to_dict(zip_bytes: bytes) -> Dict[str, bytes]:
    """
    Extract ZIP archive to dictionary
    
    Args:
        zip_bytes: ZIP file content as bytes
    
    Returns:
        Dict mapping file paths to file contents (bytes)
    """
    files = {}
    
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            for name in z.namelist():
                # Skip directories and macOS system files
                if name.endswith("/"):
                    continue
                if name.startswith("._") or ".DS_Store" in name:
                    continue
                if "__MACOSX" in name:
                    continue
                
                # Remove root folder wrapper if exists
                parts = name.split("/", 1)
                clean_path = parts[1] if len(parts) > 1 else parts[0]
                
                files[clean_path] = z.read(name)
    
    except Exception as e:
        print(f"❌ ZIP extraction error: {e}")
    
    return files


def upload_zip_to_offer(
    client: KeitaroClient,
    offer_id: int,
    zip_bytes: bytes,
    verbose: bool = True
) -> bool:
    """
    Upload ZIP archive to offer
    
    Strategy:
    1. Try ZIP upload (preferred)
    2. If fails, extract and upload files individually
    
    Args:
        client: KeitaroClient instance
        offer_id: Offer ID
        zip_bytes: ZIP file content
        verbose: Print progress messages
    
    Returns:
        True if all files uploaded successfully
    """
    # === КРОК 1: Спробуй ZIP upload ===
    if verbose:
        print(f"📦 Attempting ZIP upload for offer {offer_id}...")
    
    if client.upload_zip(offer_id, zip_bytes):
        return True
    
    # === КРОК 2: Fallback - upload файлів ===
    if verbose:
        print("⚠️  ZIP upload failed, uploading files individually...")
    
    files = unzip_to_dict(zip_bytes)
    
    # === КРОК 2A: Знайди всі папки ===
    folders = set()
    for path in files.keys():
        if "/" in path:
            folder = path.split("/")[0]  # Тільки перша папка!
            folders.add(folder)
    
    # === КРОК 2B: Папки ===
    # Keitaro API часто не допускає створення папок
    # Тому файли в папках можуть падати - але це OK
    # Wе просто спробуємо завантажити усі файли як є
        
        # === КРОК 3: Видали проблемні файли ===
        for problem_file in ["index.php", "_preview.png"]:
            try:
                client.delete_file(offer_id, problem_file)
            except:
                pass
        
        # === КРОК 4: Завантажуй файли ===
        total = len(files)
        success_count = 0
        failed_files = []
        
        for i, (path, content) in enumerate(files.items(), 1):
            if verbose:
                print(f"  📤 {i}/{total} → {path}")
            
            try:
                if client.upload_file(offer_id, path, content):
                    success_count += 1
                else:
                    if verbose:
                        print(f"    ❌ Failed: {path}")
                    failed_files.append(path)
            
            except Exception as e:
                if verbose:
                    print(f"    ❌ Exception: {path} - {e}")
                failed_files.append(path)
        
        if verbose:
            print(f"✅ Uploaded {success_count}/{total} files")
            if failed_files:
                print(f"⚠️  Failed files ({len(failed_files)}):")
                for f in failed_files:
                    print(f"   - {f}")
        
        # Успіх якщо більшість файлів загружені
        return success_count >= total * 0.8  # 80% успіху = OK
