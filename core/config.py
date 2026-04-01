"""
CONFIGURATION & BEST PRACTICES
===============================

Production-ready конфігурація та рекомендації.
"""

import os
import logging
from pathlib import Path


# ════════════════════════════════════════════════════════════════
# 1. LOGGING SETUP
# ════════════════════════════════════════════════════════════════

def setup_logging(
    level=logging.INFO,
    log_file: str = None,
    format_string: str = None
):
    """
    Setup logging for the application
    
    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR)
        log_file: Optional log file path
        format_string: Custom format string
    
    Example:
        setup_logging(level=logging.DEBUG, log_file="app.log")
    """
    
    if not format_string:
        format_string = (
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
    
    formatter = logging.Formatter(format_string)
    
    # Root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    
    # Suppress noisy libraries
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("requests").setLevel(logging.WARNING)
    logging.getLogger("google").setLevel(logging.WARNING)
    
    root_logger.info(f"Logging initialized at level {logging.getLevelName(level)}")


# ════════════════════════════════════════════════════════════════
# 2. CONFIG MANAGEMENT
# ════════════════════════════════════════════════════════════════

class Config:
    """
    Application configuration
    
    Loads from environment and st.secrets
    """
    
    # KEITARO
    KEITARO_URL: str = None
    KEITARO_API_KEY: str = None
    KEITARO_TIMEOUT: int = 30
    KEITARO_VERIFY_SSL: bool = False  # Often has self-signed certs
    
    # GOOGLE SHEETS
    GCP_CREDENTIALS: dict = None
    SHEETS_SPREADSHEET_ID: str = None
    SHEETS_ENABLED: bool = True
    
    # GOOGLE SEARCH CONSOLE (future)
    GSC_ENABLED: bool = False
    GSC_CREDENTIALS: dict = None
    
    # APPLICATION
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = None
    
    @classmethod
    def from_streamlit(cls, st):
        """Load config from Streamlit secrets"""
        try:
            cls.KEITARO_URL = st.secrets.get("KEITARO_URL")
            cls.KEITARO_API_KEY = st.secrets.get("KEITARO_API_KEY")
            
            cls.GCP_CREDENTIALS = st.secrets.get("gcp", {}).get("credentials")
            cls.SHEETS_SPREADSHEET_ID = st.secrets.get("sheets", {}).get("spreadsheet_id")
            
            cls.DEBUG = st.secrets.get("DEBUG", False)
            cls.LOG_LEVEL = st.secrets.get("LOG_LEVEL", "INFO")
            
            return True
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return False
    
    @classmethod
    def from_env(cls):
        """Load config from environment variables"""
        cls.KEITARO_URL = os.getenv("KEITARO_URL")
        cls.KEITARO_API_KEY = os.getenv("KEITARO_API_KEY")
        
        cls.GCP_CREDENTIALS = os.getenv("GCP_CREDENTIALS")
        cls.SHEETS_SPREADSHEET_ID = os.getenv("SHEETS_SPREADSHEET_ID")
        
        cls.DEBUG = os.getenv("DEBUG", "false").lower() == "true"
        cls.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
        cls.LOG_FILE = os.getenv("LOG_FILE")
        
        return True
    
    @classmethod
    def validate(cls) -> tuple[bool, list[str]]:
        """
        Validate configuration
        
        Returns:
            (is_valid, errors)
        """
        errors = []
        
        if not cls.KEITARO_URL:
            errors.append("KEITARO_URL is required")
        
        if not cls.KEITARO_API_KEY:
            errors.append("KEITARO_API_KEY is required")
        
        if cls.SHEETS_ENABLED and not cls.SHEETS_SPREADSHEET_ID:
            errors.append("SHEETS_SPREADSHEET_ID is required for Sheets")
        
        return len(errors) == 0, errors
    
    @classmethod
    def to_dict(cls, mask_secrets=True):
        """Get config as dict"""
        config = {
            "KEITARO_URL": cls.KEITARO_URL,
            "KEITARO_API_KEY": "***" if mask_secrets else cls.KEITARO_API_KEY,
            "SHEETS_ENABLED": cls.SHEETS_ENABLED,
            "SHEETS_SPREADSHEET_ID": cls.SHEETS_SPREADSHEET_ID,
            "DEBUG": cls.DEBUG,
            "LOG_LEVEL": cls.LOG_LEVEL,
        }
        return config


# ════════════════════════════════════════════════════════════════
# 3. ERROR HANDLING
# ════════════════════════════════════════════════════════════════

class AppError(Exception):
    """Base application error"""
    pass


class ConfigError(AppError):
    """Configuration error"""
    pass


class KeitaroError(AppError):
    """Keitaro API error"""
    pass


class SheetError(AppError):
    """Google Sheets error"""
    pass


def handle_error(error: Exception, context: str = ""):
    """
    Handle application errors
    
    Args:
        error: Exception to handle
        context: Context description
    
    Returns:
        User-friendly error message
    """
    logger = logging.getLogger(__name__)
    
    logger.exception(f"Error in {context}: {error}")
    
    # User-friendly messages
    if isinstance(error, ConfigError):
        return "❌ Configuration error. Check secrets.toml"
    elif isinstance(error, KeitaroError):
        return "❌ Keitaro API error. Check your credentials"
    elif isinstance(error, SheetError):
        return "❌ Google Sheets error. Check your spreadsheet"
    else:
        return f"❌ Unexpected error: {str(error)[:100]}"


# ════════════════════════════════════════════════════════════════
# 4. STREAMLIT SETUP
# ════════════════════════════════════════════════════════════════

def setup_streamlit_app(st, app_name: str = "Site Launcher"):
    """
    Setup Streamlit application
    
    Usage in app.py:
        import streamlit as st
        from config import setup_streamlit_app, Config
        
        setup_streamlit_app(st, "My App")
        Config.from_streamlit(st)
    """
    
    # Page config
    st.set_page_config(
        page_title=app_name,
        page_icon="🚀",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Configuration")
        
        if st.checkbox("Show Config", value=False):
            is_valid, errors = Config.validate()
            
            if is_valid:
                st.success("✅ Configuration valid")
                st.json(Config.to_dict())
            else:
                st.error("❌ Configuration invalid")
                for error in errors:
                    st.write(f"  • {error}")
        
        st.divider()
        st.markdown("### 📚 Help")
        st.write("""
        - Check QUICK_START.md for setup
        - Check DOCUMENTATION.md for details
        - Check examples_and_tests.py for examples
        """)


# ════════════════════════════════════════════════════════════════
# 5. BEST PRACTICES
# ════════════════════════════════════════════════════════════════

"""
🎯 PRODUCTION BEST PRACTICES:

1. SECRETS MANAGEMENT
   ✅ Use st.secrets (Streamlit Cloud) or environment variables
   ❌ Never hardcode secrets
   ❌ Never log API keys
   
   # Good
   api_key = st.secrets["KEITARO_API_KEY"]
   logger.info("Processing domain")  # No key!
   
   # Bad
   api_key = "my-secret-key"  # Hardcoded!
   logger.info(f"Using key: {api_key}")  # Logged!

2. ERROR HANDLING
   ✅ Catch specific exceptions
   ✅ Log errors with context
   ✅ Return user-friendly messages
   
   # Good
   try:
       offer = client.create_offer(domain)
   except KeitaroAPIError as e:
       logger.error(f"Failed to create offer {domain}: {e}")
       st.error("Failed to create offer")
   
   # Bad
   offer = client.create_offer(domain)  # No error handling!

3. CACHING
   ✅ Cache expensive operations (@st.cache_resource)
   ✅ Cache data between reruns (@st.cache_data)
   
   # Good
   @st.cache_resource
   def init_client():
       return KeitaroClient(...)
   
   client = init_client()  # Reused between reruns
   
   # Bad
   def get_client():
       return KeitaroClient(...)  # Created every time!

4. TIMEOUTS
   ✅ Set reasonable timeouts
   ✅ Retry on timeout
   
   # Good
   response = requests.post(..., timeout=30)
   
   # Bad
   response = requests.post(...)  # No timeout!

5. VALIDATION
   ✅ Validate input before processing
   ✅ Validate API responses
   
   # Good
   is_valid, errors = validate_config(config)
   if not is_valid:
       for error in errors:
           st.error(error)
       return
   
   # Bad
   process_config(config)  # What if invalid?

6. LOGGING
   ✅ Log important events
   ✅ Use appropriate levels (DEBUG, INFO, WARNING, ERROR)
   ✅ Log with context
   
   # Good
   logger.info(f"Creating offer for {domain}")
   logger.error(f"Failed to create offer: {e}")
   
   # Bad
   print(f"Creating offer")  # print is bad!
   logger.debug(f"API response: {response.text}")  # Too verbose

7. MONITORING
   ✅ Track success/failure rates
   ✅ Monitor API quotas
   ✅ Alert on errors
   
   # Good
   stats = sheets.get_stats()
   if stats["failed"] > stats["success"]:
       send_alert("More failures than successes!")
   
   # Bad
   # No monitoring at all

8. TESTING
   ✅ Write unit tests
   ✅ Test edge cases
   ✅ Test error scenarios
   
   # Good
   def test_create_offer():
       client = KeitaroClient(...)
       offer = client.create_offer("test.com")
       assert offer["id"] > 0
   
   # Bad
   # No tests, just manual testing

9. DOCUMENTATION
   ✅ Document functions
   ✅ Document configuration
   ✅ Document workflows
   
   # Good
   def create_offer(domain: str) -> Dict:
       \"\"\"
       Create new offer
       
       Args:
           domain: Domain name
       
       Returns:
           Dict with offer data
       \"\"\"
   
   # Bad
   def create_offer(domain):
       # No documentation

10. PERFORMANCE
    ✅ Batch operations when possible
    ✅ Parallelize independent tasks
    ✅ Cache results
    
    # Good
    results = pipeline.launch_batch(sites, zips)  # Batched
    
    # Bad
    for site in sites:
        pipeline.launch_site(site, zip)  # Sequential
"""


# ════════════════════════════════════════════════════════════════
# 6. MONITORING & ALERTS
# ════════════════════════════════════════════════════════════════

class Monitor:
    """Application monitoring"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.metrics = {}
    
    def record_launch(self, success: bool, domain: str, duration: float):
        """Record site launch"""
        self.metrics.setdefault("launches", {})
        self.metrics["launches"][domain] = {
            "success": success,
            "duration": duration,
            "timestamp": str(__import__("datetime").datetime.now())
        }
    
    def get_success_rate(self) -> float:
        """Get launch success rate"""
        launches = self.metrics.get("launches", {})
        
        if not launches:
            return 0.0
        
        success_count = sum(1 for l in launches.values() if l["success"])
        return success_count / len(launches) * 100
    
    def get_avg_duration(self) -> float:
        """Get average launch duration"""
        launches = self.metrics.get("launches", {})
        
        if not launches:
            return 0.0
        
        durations = [l["duration"] for l in launches.values()]
        return sum(durations) / len(durations)
    
    def should_alert(self) -> bool:
        """Check if alert should be sent"""
        success_rate = self.get_success_rate()
        
        # Alert if < 80% success rate
        return success_rate < 80


# ════════════════════════════════════════════════════════════════
# 7. INITIALIZATION
# ════════════════════════════════════════════════════════════════

def init_app(st, config_source: str = "streamlit"):
    """
    Initialize application
    
    Args:
        st: Streamlit module
        config_source: "streamlit" or "env"
    
    Returns:
        (is_valid, error_message)
    """
    
    # Setup Streamlit
    setup_streamlit_app(st)
    
    # Load config
    if config_source == "streamlit":
        Config.from_streamlit(st)
    else:
        Config.from_env()
    
    # Validate
    is_valid, errors = Config.validate()
    
    if not is_valid:
        st.error("❌ Configuration Error")
        for error in errors:
            st.write(f"  • {error}")
        return False, errors[0] if errors else "Unknown error"
    
    # Setup logging
    setup_logging(
        level=getattr(logging, Config.LOG_LEVEL),
        log_file=Config.LOG_FILE
    )
    
    logging.info("✅ Application initialized")
    return True, None


# ════════════════════════════════════════════════════════════════
# 8. EXAMPLE secrets.toml
# ════════════════════════════════════════════════════════════════

"""
# secrets.toml for Streamlit Cloud

[KEITARO]
KEITARO_URL = "https://keitaro.io"
KEITARO_API_KEY = "your-api-key-here"

[gcp]
credentials = \"\"\"
{
  "type": "service_account",
  "project_id": "my-project",
  "private_key_id": "key-id",
  "private_key": "-----BEGIN PRIVATE KEY-----\\n...\\n-----END PRIVATE KEY-----\\n",
  "client_email": "service@project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs"
}
\"\"\"

[sheets]
spreadsheet_id = "1BxiMVs0XRA5nFMKUVfIKewOlMmCgqQlz"

[DEBUG]
DEBUG = false
LOG_LEVEL = "INFO"
LOG_FILE = "app.log"
"""

# ════════════════════════════════════════════════════════════════
# 9. EXAMPLE .env
# ════════════════════════════════════════════════════════════════

"""
# .env for local development

KEITARO_URL=https://keitaro.local
KEITARO_API_KEY=test-key
SHEETS_SPREADSHEET_ID=1BxiMVs0XRA5nFMKUVfIKewOlMmCgqQlz
DEBUG=true
LOG_LEVEL=DEBUG
LOG_FILE=app.log
"""
