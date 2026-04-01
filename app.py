"""
Complete Streamlit App
======================

Повний готовий Streamlit додаток з усією інтеграцією.
Можеш використати це як template для app.py
"""

import streamlit as st
import logging
from datetime import datetime
import time

# Import our modules
from keitaro_api import KeitaroClient, KeitaroAPIError
from site_launch_pipeline import SiteLaunchPipeline, SiteLaunchConfig, validate_config
from google_sheets import GoogleSheetsManager
from config import Config, init_app, Monitor, handle_error
from keitaro_api import KeitaroClient
from site_launch_pipeline import SiteLaunchPipeline

# Setup logger
logger = logging.getLogger(__name__)


# ════════════════════════════════════════════════════════════════
# INITIALIZATION
# ════════════════════════════════════════════════════════════════

@st.cache_resource
def init_clients():
    """Initialize all clients"""
    try:
        # Keitaro
        client = KeitaroClient(
            base_url=Config.KEITARO_URL,
            api_key=Config.KEITARO_API_KEY
        )
        
        # Google Sheets (optional)
        sheets = None
        if Config.SHEETS_ENABLED and Config.SHEETS_SPREADSHEET_ID:
            try:
                sheets = GoogleSheetsManager(
                    credentials_json=Config.GCP_CREDENTIALS,
                    spreadsheet_id=Config.SHEETS_SPREADSHEET_ID
                )
                sheets.setup_header()
            except Exception as e:
                logger.warning(f"Google Sheets init failed: {e}")
        
        return client, sheets
    
    except Exception as e:
        st.error(f"❌ Failed to init clients: {e}")
        return None, None


# ════════════════════════════════════════════════════════════════
# UI COMPONENTS
# ════════════════════════════════════════════════════════════════

def show_header():
    """Show app header"""
    st.markdown("""
    # 🚀 Site Launcher Pro
    
    Automated site launch pipeline for Keitaro
    """)


def show_config_status():
    """Show configuration status in sidebar"""
    with st.sidebar:
        st.markdown("### ⚙️ Status")
        
        # Check config
        is_valid, errors = Config.validate()
        
        if is_valid:
            st.success("✅ Configuration valid")
        else:
            st.error("❌ Configuration invalid")
            for error in errors:
                st.write(f"  • {error}")
        
        # Check API connection
        if is_valid:
            if st.button("🔗 Test API", use_container_width=True):
                client, _ = init_clients()
                if client:
                    try:
                        offers = client.list_offers()
                        st.success(f"✅ Connected! {len(offers)} offers found")
                    except Exception as e:
                        st.error(f"❌ Connection failed: {e}")


def input_site_config():
    """Input configuration for a single site"""
    
    st.markdown("## 📝 Site Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        brand = st.text_input(
            "Brand Name",
            placeholder="My Brand",
            help="Brand or company name"
        )
        domain = st.text_input(
            "Domain",
            placeholder="example.com",
            help="Domain for the site"
        )
    
    with col2:
        geo_code = st.selectbox(
            "Geographic Code",
            ["UA", "US", "GB", "DE", "FR", "IT", "ES", "PL", "RO"],
            help="Country code"
        )
        lang_code = st.selectbox(
            "Language",
            ["uk", "en", "de", "fr", "it", "es", "pl", "ro"],
            help="Language code"
        )
    
    return brand, domain, geo_code, lang_code


def upload_zip_file():
    """Upload ZIP file"""
    
    st.markdown("## 📦 ZIP Archive")
    
    uploaded_file = st.file_uploader(
        "Upload site ZIP",
        type=["zip"],
        help="ZIP with index.html, css/, js/, etc."
    )
    
    if uploaded_file:
        st.success(f"✅ {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
        return uploaded_file.read()
    
    return None


def launch_single_site():
    """UI for launching a single site"""
    
    tab_config, tab_upload, tab_launch = st.tabs([
        "Configuration",
        "ZIP Upload",
        "Launch"
    ])
    
    with tab_config:
        brand, domain, geo_code, lang_code = input_site_config()
        
        st.session_state["single_config"] = {
            "brand": brand,
            "domain": domain,
            "geo_code": geo_code,
            "lang_code": lang_code
        }
    
    with tab_upload:
        zip_bytes = upload_zip_file()
        st.session_state["single_zip"] = zip_bytes
    
    with tab_launch:
        if st.button("🚀 Launch Site", use_container_width=True, type="primary"):
            # Validate
            config = st.session_state.get("single_config", {})
            zip_bytes = st.session_state.get("single_zip")
            
            if not config.get("domain"):
                st.error("❌ Please fill in domain")
                return
            
            if not zip_bytes:
                st.error("❌ Please upload ZIP")
                return
            
            # Initialize
            client, sheets = init_clients()
            if not client:
                st.error("❌ Failed to initialize clients")
                return
            
            pipeline = SiteLaunchPipeline(
                keitaro_client=client,
                google_sheets_manager=sheets
            )
            
            # Progress UI
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def on_progress(percent, message):
                progress_bar.progress(min(percent / 100, 0.99))
                status_text.info(message)
            
            # Launch
            try:
                on_progress(10, f"🚀 Launching {config['domain']}...")
                
                start_time = time.time()
                
                result = pipeline.launch_site(
                    brand=config["brand"],
                    domain=config["domain"],
                    geo_code=config["geo_code"],
                    lang_code=config["lang_code"],
                    zip_bytes=zip_bytes,
                    template_campaign_id=None,
                    progress_callback=on_progress
                )
                
                duration = time.time() - start_time
                
                progress_bar.progress(1.0)
                
                # Display results
                st.divider()
                
                if result["success"]:
                    st.success(f"✅ Site launched in {duration:.1f}s!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("Offer ID", result["offer_id"])
                    with col2:
                        st.metric("Campaign ID", result["campaign_id"])
                    
                    # Log to sheets
                    if sheets:
                        sheets.add_row(
                            brand=config["brand"],
                            domain=config["domain"],
                            geo_code=config["geo_code"],
                            lang_code=config["lang_code"],
                            status="success",
                            offer_id=result["offer_id"],
                            campaign_id=result["campaign_id"]
                        )
                else:
                    st.error("❌ Launch failed")
                    for error in result["errors"]:
                        st.write(f"  • {error}")
                    
                    # Log failure to sheets
                    if sheets:
                        sheets.add_row(
                            brand=config["brand"],
                            domain=config["domain"],
                            geo_code=config["geo_code"],
                            lang_code=config["lang_code"],
                            status="failed",
                            error_message="; ".join(result["errors"])
                        )
            
            except Exception as e:
                st.error(f"❌ Error: {e}")
                logger.exception("Launch error")


def launch_batch_sites():
    """UI for launching multiple sites"""
    
    st.markdown("## 🌐 Batch Launch")
    
    # Domains input
    col1, col2 = st.columns([4, 1])
    with col1:
        new_domain = st.text_input(
            "Add Domain",
            placeholder="example.com",
            label_visibility="collapsed",
            key="new_domain"
        )
    with col2:
        if st.button("➕ Add", use_container_width=True):
            if new_domain and new_domain not in st.session_state.get("batch_domains", []):
                st.session_state.setdefault("batch_domains", []).append(new_domain)
                st.rerun()
    
    # List domains
    if "batch_domains" in st.session_state and st.session_state["batch_domains"]:
        st.markdown("**Domains to launch:**")
        
        cols = st.columns([3, 1])
        for domain in st.session_state["batch_domains"]:
            with cols[0]:
                st.write(f"  • {domain}")
            with cols[1]:
                if st.button("❌", key=f"remove_{domain}", use_container_width=True):
                    st.session_state["batch_domains"].remove(domain)
                    st.rerun()
    
    st.divider()
    
    # Configuration (same for all)
    col1, col2 = st.columns(2)
    with col1:
        batch_brand = st.text_input("Brand (for all)", placeholder="My Brand")
        batch_geo = st.selectbox("Geo (for all)", ["UA", "US", "GB", "DE", "FR"])
    
    with col2:
        batch_lang = st.selectbox("Language (for all)", ["uk", "en", "de", "fr"])
    
    st.divider()
    
    # ZIP uploads
    uploaded_files = st.file_uploader(
        "Upload ZIP files",
        type=["zip"],
        accept_multiple_files=True
    )
    
    zip_map = {}
    if uploaded_files:
        st.markdown("**Uploaded files:**")
        for f in uploaded_files:
            filename = f.name.replace(".zip", "")
            zip_map[filename] = f.read()
            st.write(f"  ✓ {f.name}")
    
    st.divider()
    
    # Launch button
    if st.button("🚀 Launch All Sites", use_container_width=True, type="primary"):
        domains = st.session_state.get("batch_domains", [])
        
        if not domains:
            st.error("❌ No domains")
            return
        
        if not batch_brand:
            st.error("❌ Brand required")
            return
        
        if not zip_map:
            st.error("❌ Upload ZIPs")
            return
        
        # Initialize
        client, sheets = init_clients()
        if not client:
            st.error("❌ Failed to initialize")
            return
        
        pipeline = SiteLaunchPipeline(
            keitaro_client=client,
            google_sheets_manager=sheets
        )
        
        # Create configs
        configs = [
            SiteLaunchConfig(
                brand=batch_brand,
                domain=d,
                geo_code=batch_geo,
                lang_code=batch_lang
            )
            for d in domains
        ]
        
        # Launch
        progress_bar = st.progress(0)
        status = st.empty()
        
        try:
            results = pipeline.launch_batch(
                sites=configs,
                zip_files=zip_map,
                progress_callback=lambda p, m: (
                    progress_bar.progress(p / 100),
                    status.info(m)
                )
            )
            
            # Results
            st.divider()
            st.markdown("### Results")
            
            success = sum(1 for r in results if r["success"])
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("✅ Success", success)
            with col2:
                st.metric("❌ Failed", len(results) - success)
            
            # Detailed results
            for result in results:
                if result["success"]:
                    with st.expander(f"✅ {result['domain']}", expanded=False):
                        st.json({
                            "Offer": result["offer_id"],
                            "Campaign": result["campaign_id"]
                        })
                else:
                    with st.expander(f"❌ {result['domain']}", expanded=True):
                        for err in result.get("errors", []):
                            st.error(f"  {err}")
        
        except Exception as e:
            st.error(f"❌ Batch launch failed: {e}")
            logger.exception("Batch launch error")


def show_stats():
    """Show statistics from Google Sheets"""
    
    st.markdown("## 📊 Statistics")
    
    _, sheets = init_clients()
    
    if not sheets:
        st.warning("⚠️  Google Sheets not configured")
        return
    
    stats = sheets.get_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📈 Total Launches", stats["total"])
    
    with col2:
        st.metric("✅ Successful", stats["success"])
    
    with col3:
        st.metric("❌ Failed", stats["failed"])
    
    with col4:
        st.metric("⏳ Pending", stats["pending"])
    
    # Recent launches
    with st.expander("📋 Recent Launches", expanded=False):
        rows = sheets.get_all_rows()
        
        if rows:
            import pandas as pd
            
            df = pd.DataFrame(rows[-20:])
            
            # Format display
            df_display = df[[
                "timestamp", "domain", "brand", "status", "offer_id", "campaign_id"
            ]].copy()
            
            st.dataframe(df_display, use_container_width=True)
        else:
            st.info("No data yet")


# ════════════════════════════════════════════════════════════════
# MAIN APP
# ════════════════════════════════════════════════════════════════

def main():
    """Main application"""
    
    # Initialize app
    is_valid, error = init_app(st, config_source="streamlit")
    
    if not is_valid:
        st.error(f"❌ Initialization failed: {error}")
        return
    
    # Header
    show_header()
    show_config_status()
    
    st.divider()
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "🚀 Single Site",
        "🌐 Batch Launch",
        "📊 Statistics"
    ])
    
    with tab1:
        launch_single_site()
    
    with tab2:
        launch_batch_sites()
    
    with tab3:
        show_stats()


if __name__ == "__main__":
    main()
