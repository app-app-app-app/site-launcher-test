"""
Google Sheets Integration
=========================

Запис результатів запусків в Google Sheets для моніторингу.
"""

from typing import Optional, List
from datetime import datetime
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import logging

logger = logging.getLogger(__name__)


class GoogleSheetsManager:
    """
    Manager для Google Sheets
    
    Записує результати запусків сайтів в таблицю:
    Дата | Бренд | Домен | Гео | Мова | Шаблон | Статус | Offer ID | Campaign ID
    """
    
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
    
    def __init__(
        self,
        credentials_json: str,
        spreadsheet_id: str,
        sheet_name: str = "Запуски"
    ):
        """
        Initialize Google Sheets manager
        
        Args:
            credentials_json: JSON credentials (from st.secrets or env)
            spreadsheet_id: Google Sheets ID (from URL)
            sheet_name: Sheet name to write to (default: "Запуски")
        
        Example:
            manager = GoogleSheetsManager(
                credentials_json=st.secrets["gcp"]["credentials"],
                spreadsheet_id="1BxiMVs0XRA5nFMKUVfIKewOlMmCgqQlz"
            )
        """
        self.credentials_json = credentials_json
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        
        self._service = None
        self._init_service()
    
    def _init_service(self):
        """Initialize Google Sheets API service"""
        try:
            creds = Credentials.from_service_account_info(
                self.credentials_json,
                scopes=self.SCOPES
            )
            
            self._service = build("sheets", "v4", credentials=creds)
            logger.info("✅ Google Sheets initialized")
        
        except Exception as e:
            logger.error(f"❌ Failed to init Google Sheets: {e}")
            raise
    
    def add_row(
        self,
        brand: str,
        domain: str,
        geo_code: str,
        lang_code: str,
        template: str = "",
        status: str = "pending",
        offer_id: Optional[int] = None,
        campaign_id: Optional[int] = None,
        error_message: str = ""
    ) -> bool:
        """
        Add row to Google Sheets
        
        Args:
            brand: Brand name
            domain: Domain name
            geo_code: Geographic code (UA, US, etc.)
            lang_code: Language code (uk, en, etc.)
            template: Template used (template_1, etc.)
            status: Launch status (pending, success, failed)
            offer_id: Keitaro offer ID
            campaign_id: Keitaro campaign ID
            error_message: Error description if failed
        
        Returns:
            True if successful
        """
        try:
            timestamp = datetime.now().isoformat()
            
            # Format values
            values = [[
                timestamp,                      # Дата/час
                brand,                          # Бренд
                domain,                         # Домен
                geo_code.upper(),              # Гео
                lang_code.lower(),             # Мова
                template,                       # Шаблон
                status,                         # Статус
                offer_id or "",                # Offer ID
                campaign_id or "",             # Campaign ID
                error_message                   # Помилка (якщо є)
            ]]
            
            # Append to sheet
            body = {"values": values}
            
            self._service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{self.sheet_name}'!A:J",
                valueInputOption="USER_ENTERED",
                body=body
            ).execute()
            
            logger.info(f"✅ Added to Sheets: {domain}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to add row: {e}")
            return False
    
    def update_row(
        self,
        domain: str,
        status: str,
        offer_id: Optional[int] = None,
        campaign_id: Optional[int] = None,
        error_message: str = ""
    ) -> bool:
        """
        Update row for domain (find by domain name)
        
        Args:
            domain: Domain name to find
            status: New status
            offer_id: Offer ID
            campaign_id: Campaign ID
            error_message: Error message
        
        Returns:
            True if updated
        """
        try:
            # Get all rows
            result = self._service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{self.sheet_name}'!A:J"
            ).execute()
            
            values = result.get("values", [])
            
            # Find row by domain
            row_index = None
            for i, row in enumerate(values, 1):
                if len(row) > 2 and row[2] == domain:
                    row_index = i
                    break
            
            if not row_index:
                logger.warning(f"Domain {domain} not found in sheet")
                return False
            
            # Update values in row
            update_values = [[
                "",                    # Дата (не міняємо)
                "",                    # Бренд (не міняємо)
                domain,               # Домен
                "",                   # Гео (не міняємо)
                "",                   # Мова (не міняємо)
                "",                   # Шаблон (не міняємо)
                status,               # Статус (ОНОВЛЮЄМО)
                offer_id or "",       # Offer ID (ОНОВЛЮЄМО)
                campaign_id or "",    # Campaign ID (ОНОВЛЮЄМО)
                error_message         # Помилка (ОНОВЛЮЄМО)
            ]]
            
            # Update range
            range_name = f"'{self.sheet_name}'!A{row_index}:J{row_index}"
            
            self._service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption="USER_ENTERED",
                body={"values": update_values}
            ).execute()
            
            logger.info(f"✅ Updated Sheets: {domain}")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to update row: {e}")
            return False
    
    def get_all_rows(self) -> List[dict]:
        """
        Get all rows from sheet
        
        Returns:
            List of dictionaries with row data
        """
        try:
            result = self._service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{self.sheet_name}'!A:J"
            ).execute()
            
            values = result.get("values", [])
            
            if not values:
                return []
            
            # First row is header
            header = values[0]
            rows = []
            
            for row in values[1:]:
                # Pad row if needed
                while len(row) < len(header):
                    row.append("")
                
                row_dict = {
                    "timestamp": row[0] if len(row) > 0 else "",
                    "brand": row[1] if len(row) > 1 else "",
                    "domain": row[2] if len(row) > 2 else "",
                    "geo": row[3] if len(row) > 3 else "",
                    "lang": row[4] if len(row) > 4 else "",
                    "template": row[5] if len(row) > 5 else "",
                    "status": row[6] if len(row) > 6 else "",
                    "offer_id": row[7] if len(row) > 7 else "",
                    "campaign_id": row[8] if len(row) > 8 else "",
                    "error": row[9] if len(row) > 9 else "",
                }
                
                rows.append(row_dict)
            
            return rows
        
        except Exception as e:
            logger.error(f"❌ Failed to get rows: {e}")
            return []
    
    def get_stats(self) -> dict:
        """
        Get statistics from sheet
        
        Returns:
            Dict with stats: {
                "total": int,
                "success": int,
                "failed": int,
                "pending": int
            }
        """
        rows = self.get_all_rows()
        
        stats = {
            "total": len(rows),
            "success": sum(1 for r in rows if r["status"] == "success"),
            "failed": sum(1 for r in rows if r["status"] == "failed"),
            "pending": sum(1 for r in rows if r["status"] == "pending"),
        }
        
        return stats
    
    def setup_header(self) -> bool:
        """
        Create header row if sheet is empty
        
        Returns:
            True if header created or already exists
        """
        try:
            result = self._service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{self.sheet_name}'!A1:J1"
            ).execute()
            
            values = result.get("values", [])
            
            # Header already exists
            if values and len(values[0]) > 0:
                logger.info("Header already exists")
                return True
            
            # Create header
            header = [[
                "Дата/Час",
                "Бренд",
                "Домен",
                "Гео",
                "Мова",
                "Шаблон",
                "Статус",
                "Offer ID",
                "Campaign ID",
                "Помилка"
            ]]
            
            self._service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=f"'{self.sheet_name}'!A1:J1",
                valueInputOption="USER_ENTERED",
                body={"values": header}
            ).execute()
            
            logger.info("✅ Header created")
            return True
        
        except Exception as e:
            logger.error(f"❌ Failed to setup header: {e}")
            return False


# ========================
# STREAMLIT INTEGRATION
# ========================

def init_google_sheets(st):
    """
    Initialize Google Sheets in Streamlit
    
    Usage in app.py:
        sheets = init_google_sheets(st)
        sheets.add_row(brand, domain, geo, lang)
    """
    try:
        manager = GoogleSheetsManager(
            credentials_json=st.secrets["gcp"]["credentials"],
            spreadsheet_id=st.secrets["sheets"]["spreadsheet_id"],
            sheet_name="Запуски"
        )
        
        # Setup header if needed
        manager.setup_header()
        
        return manager
    
    except Exception as e:
        st.error(f"❌ Failed to init Google Sheets: {e}")
        return None


def show_sheets_stats(st, sheets: GoogleSheetsManager):
    """
    Display Google Sheets stats in Streamlit
    
    Usage:
        show_sheets_stats(st, sheets)
    """
    if not sheets:
        return
    
    stats = sheets.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📊 Всього", stats["total"])
    
    with col2:
        st.metric("✅ Успіх", stats["success"])
    
    with col3:
        st.metric("❌ Помилок", stats["failed"])
    
    with col4:
        st.metric("⏳ Очікуючих", stats["pending"])
    
    # Show recent rows
    with st.expander("📋 Останні запуски"):
        rows = sheets.get_all_rows()
        
        if rows:
            # Show last 10
            import pandas as pd
            df = pd.DataFrame(rows[-10:])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Немає даних")


# ========================
# CONFIGURATION EXAMPLE
# ========================

"""
В secrets.toml:

[gcp]
credentials = \"\"\"
{
  "type": "service_account",
  "project_id": "my-project",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token"
}
\"\"\"

[sheets]
spreadsheet_id = "1BxiMVs0XRA5nFMKUVfIKewOlMmCgqQlz"  # З URL таблиці
"""


# ========================
# EXAMPLE USAGE
# ========================

if __name__ == "__main__":
    import os
    import json
    
    # For testing
    creds = json.loads(os.environ.get("GCP_CREDENTIALS", "{}"))
    sheet_id = os.environ.get("SHEET_ID", "")
    
    if creds and sheet_id:
        manager = GoogleSheetsManager(
            credentials_json=creds,
            spreadsheet_id=sheet_id
        )
        
        # Test add row
        manager.add_row(
            brand="Test Brand",
            domain="test.com",
            geo_code="UA",
            lang_code="uk",
            template="template_1",
            status="success",
            offer_id=123,
            campaign_id=456
        )
        
        # Get stats
        stats = manager.get_stats()
        print(f"Stats: {stats}")
