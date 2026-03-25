import os
import json
import urllib.parse
import streamlit as st
import textwrap
import time
import re
import streamlit.components.v1 as components
from core.translit import slugify_brand
import io
import zipfile
from pathlib import Path
from typing import Optional
from core.review_pipeline import generate_review




from core.options import build_geo_labels, build_language_labels, bcp47_from, TOP_GEO_ORDER
from core.geo_detect import detect_geo_lang
from core.domain_suggest import generate_domain_candidates
from core.domain_check import check_domains_rdap
from core.lang_pipeline import generate_lang_files_multi


# ---- Page config (must be before any st.* calls) ----

def _get_favicon():
    # Page icon in the browser tab (cheap status indicator).
    step = int(st.session_state.get("step", 1))
    domains_checked = bool(st.session_state.get("domains_checked_done"))
    archives_ready = bool(st.session_state.get("archives_ready"))
    has_files = bool(st.session_state.get("generated_files"))

    # Step 2: show planet ONLY after all domains were checked
    if step == 2:
        return "🌐" if domains_checked else "🔎"

    # Step 3: show check ONLY after archives were built
    if step == 3:
        if archives_ready:
            return "✅"
        if has_files:
            return "📦"
        return "⚙️"

    return "🚀"


_brand_for_title = (st.session_state.get("brand") or "").strip()
_page_title = f"{_brand_for_title}" if _brand_for_title else "Site Launcher"

st.set_page_config(
    page_title=_page_title,
    page_icon=_get_favicon(),
    layout="wide",
)

GEO_PATH = "core/geo_defaults.json"
UNKNOWN_GEO_LABEL = "🏳️ Невідомо / Unknown"
TOTAL_STEPS = 3
TEMPLATES = {
    "template_1": {
        "label": "Шаблон 1",
        "dir": "templates/template_1-1",
        "favicon": "templates/template_1-1/favicon.svg",
        "lang": "templates/template_1-1/lang.php",
    },
    "template_2": {
        "label": "Шаблон 2",
        "dir": "templates/template_2",
        "favicon": "templates/template_2/favicon.svg",
        "lang": "templates/template_2/lang.php",
    },
        "template_3": {
        "label": "Шаблон 3",
        "dir": "templates/template_3",
        "favicon": "templates/template_3/favicon.svg",
        "lang": "templates/template_3/lang.php",
    },
}
# Default template for Streamlit page icon (does not affect per-domain selection)
DEFAULT_PAGE_TEMPLATE = "template_1"

# Постав сюди модель, яка у тебе реально доступна.
# Якщо gpt-5-mini не доступна — заміни на "gpt-4.1-mini" або "gpt-4o-mini".
DEFAULT_MODEL = "gpt-5-mini"



st.markdown("""
<style>

/* Прибрати верхню панель Streamlit (Share/...) */
header[data-testid="stHeader"] { display: none !important; }

/* Стиснути загальний top padding */
.block-container { padding-top: 0.6rem !important; }

/* ====== ХЕДЕР: тільки container(border=True), де є якір ======
   Streamlit робить окремий wrapper: stVerticalBlockBorderWrapper
*/
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor) {
  background: linear-gradient(180deg, rgba(15,23,42,0.95) 0%, rgba(2,6,23,0.75) 100%) !important;
  border: 1px solid rgba(148,163,184,0.20) !important;
  border-radius: 14px !important;
  padding: 10px 14px !important;
  margin-bottom: 12px !important;
  box-shadow: 0 10px 26px rgba(0,0,0,0.28) !important;
}

/* прибрати внутрішні зайві відступи самого контейнера */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor) > div {
  padding: 0 !important;
}

/* Заголовок — компактний і по центру */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor) h1 {
  text-align: center !important;
  font-size: 24px !important;
  margin: 2px 0 8px 0 !important;
  line-height: 1.1 !important;
}

/* Прогрес — тонкий */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor)
div[data-testid="stProgress"] > div {
  height: 6px !important;
  border-radius: 999px !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor)
div[data-testid="stProgress"] > div > div {
  border-radius: 999px !important;
}

/* Caption — компактніше */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor) .stCaption {
  margin: 2px 0 8px 0 !important;
  opacity: 0.85;
}

/* Кнопки кроків — низькі */
div[data-testid="stVerticalBlockBorderWrapper"]:has(div.sitehdr-anchor) button {
  padding: 0.28rem 0.75rem !important;
  border-radius: 10px !important;
}

/* Заголовок кожного кроку — менший і по центру */
h2 {
  font-size: 22px !important;
  margin: 10px 0 12px 0 !important;
  text-align: center !important;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* ТІЛЬКИ layout wrapper, який містить якір хедера */
div[data-testid="stLayoutWrapper"]:has(.sitehdr-anchor) {
    background-color: #9168bd !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    margin-bottom: 16px !important;
}

</style>
""", unsafe_allow_html=True)



def _mtime(path: str) -> float:
    try:
        return os.path.getmtime(path)
    except OSError:
        return 0.0


@st.cache_data
def load_geo(_file_mtime: float):
    with open(GEO_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


geo = load_geo(_mtime(GEO_PATH))
geo_labels, geo_label_to_code = build_geo_labels(geo)
lang_labels, lang_label_to_code = build_language_labels()


# ---------------------------
# State
# ---------------------------
def init_state():
    st.session_state.setdefault("step", 1)
    st.session_state.setdefault("step1_done", False)
    st.session_state.setdefault("step2_done", False)

    st.session_state.setdefault("brand", "")

    # controlled widget keys
    st.session_state.setdefault("geo_choice_label", UNKNOWN_GEO_LABEL)
    st.session_state.setdefault("lang_choice_label", lang_labels[0])  # English у списку
    st.session_state.setdefault("use_region", True)

    # derived
    st.session_state.setdefault("geo_code", "UNKNOWN")
    st.session_state.setdefault("target_lang", "unknown")

    # step1 confirmation
    st.session_state.setdefault("serp_checked", False)
    st.session_state.setdefault("decision", None)  # go|no

    # detect results
    st.session_state.setdefault("detect_status", "idle")   # idle|running|done
    st.session_state.setdefault("detect_verdict", None)    # exact|lang_only|none
    st.session_state.setdefault("detect_geo", None)
    st.session_state.setdefault("detect_lang", None)
    st.session_state.setdefault("detect_details", [])

    # step2 domains
    st.session_state.setdefault("sites_count", 1)
    st.session_state.setdefault("domain_candidates", [])
    st.session_state.setdefault("manual_domains", [])
    # UI status flags (favicons / steps)
    st.session_state.setdefault("domains_checked_done", False)  # all domains checked on Step 2
    st.session_state.setdefault("archives_ready", False)        # zips built on Step 3
    st.session_state.setdefault("manual_domain_input", "")
    st.session_state.setdefault("domain_checks", [])   # list of dicts {domain, status, reason, rdap_found}
    st.session_state.setdefault("chosen_domains", [])  # list[str]
    st.session_state.setdefault("domain_templates", {})  # dict[domain]->template_id
    st.session_state.setdefault("_copy_buf", "")

    # Task fields (простий набір)
    st.session_state.setdefault("task_buy_tg", "—")
    st.session_state.setdefault("task_buy_zone", "")
    st.session_state.setdefault("task_buy_keitaro", "")
    st.session_state.setdefault("task_buy_index", "ДА")  # ДА/НІ

    # step3 generated files
    st.session_state.setdefault("generated_files", [])

    st.session_state.setdefault("step2_autocheck_done", False)
    st.session_state.setdefault("step3_autogen_done", False)


    # rerun
    st.session_state.setdefault("needs_rerun", False)

    st.session_state.setdefault("generate_review", False)
    st.session_state.setdefault("generated_review", None)
    st.session_state.setdefault("step3_review_autogen_done", False)
    st.session_state.setdefault("review_generation_error", None)
    

    st.session_state.setdefault("auto_download_done", False)


def reset_all():
    # ВАЖЛИВО: кнопка reset натискається після того, як віджети сайдбару вже створені.
    # Тому не можна "м'яко" присвоювати значення widget-key'ам в цьому ж ререндері.
    # Робимо повне очищення і НЕ продовжуємо поточний ререндер — одразу rerun.
    st.session_state.clear()




init_state()


# ---------------------------
# Helpers
# ---------------------------

TEXT_EXTS = {".txt", ".xml", ".html", ".htm", ".php", ".css", ".js", ".json", ".md"}

def clipboard_button(text: str, label: str, key: str):
    js_text = json.dumps(text)  # безпечний JS string
    components.html(
        f"""
        <button
            onclick="navigator.clipboard.writeText({js_text}).then(() => {{
                const b = document.getElementById('{key}');
                const old = b.innerText;
                b.innerText = '✅ Скопійовано';
                setTimeout(() => b.innerText = old, 900);
            }});"
            id="{key}"
            style="width:100%; padding:0.25rem 0.5rem; border:1px solid #d0d0d0;
                   border-radius:8px; background:#f7f7f7; cursor:pointer;">
            {label}
        </button>
        """,
        height=44,
    )

def _render_placeholders(text: str, domain: str, target_lang: str) -> str:
    # {{DOMAIN}}, {{SITE_URL}}, {{LANG}}
    return (
        text.replace("{{DOMAIN}}", domain)
            .replace("{{SITE_URL}}", f"https://{domain}")
            .replace("{{LANG}}", target_lang)
    )

def extract_lang_vars(lang_php: str) -> dict:
    """
    Дістає значення змінних з lang.php:
      $app_price = '250';
      $app_currency = 'EUR';
    """
    def _get(name: str):
        m = re.search(rf"\${name}\s*=\s*(?:'([^']*)'|\"([^\"]*)\"|([^;\n\r]+))\s*;", lang_php)
        if not m:
            return None
        return (m.group(1) or m.group(2) or m.group(3) or "").strip()

    return {
        "app_price": _get("app_price"),
        "app_currency": _get("app_currency"),
    }

def patch_offer_seo(content: str, brand: str, geo_code: str, target_lang: str,
                   app_price: Optional[str], app_currency: Optional[str]) -> str:
    # $source
    content = re.sub(r'\$source\s*=\s*".*?";', f'$source = "{brand}";', content)

    # $currency = '250EUR'  <- з lang.php ($app_price + $app_currency)
    if app_price and app_currency:
        content = re.sub(r"\$currency\s*=\s*'.*?';", f"$currency = '{app_price}{app_currency}';", content)

    # $form_country / $form_phone_country
    geo_lower = (geo_code or "").lower()

    content = re.sub(
        r"\$form_country\s*=\s*'.*?';",
        f"$form_country = '{geo_lower}';",
        content
    )

    content = re.sub(
        r"\$form_phone_country\s*=\s*'.*?';",
        f"$form_phone_country = '{geo_lower}';",
        content
    )

    # $form_language
    base_lang = (target_lang or "").split("-")[0].split("_")[0]
    content = re.sub(
        r"\$form_language\s*=\s*'.*?';",
        f"$form_language = '{base_lang}';",
        content,
    )

    # $form_only_countries
    content = re.sub(
        r"\$form_only_countries\s*=\s*json_encode\(\[.*?\]\);",
        f'$form_only_countries = json_encode(["{geo_lower}"]);',
        content
    )

    # $form_is_autologin не чіпаємо
    return content

def build_domain_site_zip(
    domain: str,
    site_template_dir: str,
    lang_php_content: str,
    target_lang: str,
    geo_code: str,
    brand: str,
) -> bytes:
    root = Path(site_template_dir)
    if not root.exists() or not root.is_dir():
        raise FileNotFoundError(f"Не знайдено папку шаблону сайту: {site_template_dir}")

    # витягнемо app_price/app_currency зі згенерованого lang.php
    lang_vars = extract_lang_vars(lang_php_content)
    app_price = lang_vars.get("app_price")
    app_currency = lang_vars.get("app_currency")

    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for p in root.rglob("*"):
            if p.is_dir():
                continue

            rel = p.relative_to(root).as_posix()

            # 1) lang.php підміняємо згенерованим
            if rel.replace("\\", "/").endswith("lang.php"):
                out_bytes = lang_php_content.encode("utf-8")

            else:
                raw_bytes = p.read_bytes()

                # 2) offer_seo.php — патчимо конкретні змінні
                geo_code = (geo_code or "").lower()
                if p.name.lower() == "offer_seo.php":
                    raw_text = raw_bytes.decode("utf-8", errors="replace")
                    patched = patch_offer_seo(
                        content=raw_text,
                        brand=brand,
                        geo_code=geo_code,
                        target_lang=target_lang,
                        app_price=app_price,
                        app_currency=app_currency,
                    )
                    out_bytes = patched.encode("utf-8")

                # 3) robots.txt / sitemap.xml (та інші текстові) — плейсхолдери домену/мови
                elif p.suffix.lower() in TEXT_EXTS:
                    raw_text = raw_bytes.decode("utf-8", errors="replace")
                    rendered = _render_placeholders(raw_text, domain=domain, target_lang=target_lang)
                    out_bytes = rendered.encode("utf-8")

                else:
                    out_bytes = raw_bytes

            z.writestr(f"{domain}/{rel}", out_bytes)

    buf.seek(0)
    return buf.getvalue()

def build_all_sites_zip(
    site_template_dir: str,
    domain_to_langphp: dict,
    target_lang: str,
    geo_code: str,
    brand: str,
) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        root = Path(site_template_dir)

        for domain, lang_php_content in domain_to_langphp.items():
            # витягнемо app_price/app_currency
            lang_vars = extract_lang_vars(lang_php_content)
            app_price = lang_vars.get("app_price")
            app_currency = lang_vars.get("app_currency")

            for p in root.rglob("*"):
                if p.is_dir():
                    continue

                rel = p.relative_to(root).as_posix()

                if rel.replace("\\", "/").endswith("lang.php"):
                    out_bytes = lang_php_content.encode("utf-8")

                else:
                    raw_bytes = p.read_bytes()
                    
                    if p.name.lower() == "offer_seo.php":
                        raw_text = raw_bytes.decode("utf-8", errors="replace")
                        patched = patch_offer_seo(
                            content=raw_text,
                            brand=brand,
                            geo_code=geo_code,
                            target_lang=target_lang,
                            app_price=app_price,
                            app_currency=app_currency,
                        )
                        out_bytes = patched.encode("utf-8")

                    elif p.suffix.lower() in TEXT_EXTS:
                        raw_text = raw_bytes.decode("utf-8", errors="replace")
                        rendered = _render_placeholders(raw_text, domain=domain, target_lang=target_lang)
                        out_bytes = rendered.encode("utf-8")

                    else:
                        out_bytes = raw_bytes

                z.writestr(f"{domain}/{rel}", out_bytes)

    buf.seek(0)
    return buf.getvalue()

    



def build_all_sites_zip_multi(
    domain_to_template_dir: dict,
    domain_to_langphp: dict,
    target_lang: str,
    geo_code: str,
    brand: str,
) -> bytes:
    """
    Один ZIP з усіма доменами, але кожен домен може мати свій шаблон.
    domain_to_template_dir: {domain: "templates/.."}
    domain_to_langphp: {domain: "<php>"}
    """
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for domain, lang_php_content in domain_to_langphp.items():
            site_template_dir = domain_to_template_dir.get(domain)
            if not site_template_dir:
                continue
            root = Path(site_template_dir)
            if not root.exists() or not root.is_dir():
                continue

            lang_vars = extract_lang_vars(lang_php_content)
            app_price = lang_vars.get("app_price")
            app_currency = lang_vars.get("app_currency")

            for p in root.rglob("*"):
                if p.is_dir():
                    continue
                rel = p.relative_to(root).as_posix()

                if rel.replace("\\", "/").endswith("lang.php"):
                    out_bytes = lang_php_content.encode("utf-8")
                else:
                    raw_bytes = p.read_bytes()

                    if p.name.lower() == "offer_seo.php":
                        raw_text = raw_bytes.decode("utf-8", errors="replace")
                        patched = patch_offer_seo(
                            content=raw_text,
                            brand=brand,
                            geo_code=(geo_code or "").lower(),
                            target_lang=target_lang,
                            app_price=app_price,
                            app_currency=app_currency,
                        )
                        out_bytes = patched.encode("utf-8")
                    elif p.suffix.lower() in TEXT_EXTS:
                        raw_text = raw_bytes.decode("utf-8", errors="replace")
                        rendered = _render_placeholders(raw_text, domain=domain, target_lang=target_lang)
                        out_bytes = rendered.encode("utf-8")
                    else:
                        out_bytes = raw_bytes

                z.writestr(f"{domain}/{rel}", out_bytes)

    buf.seek(0)
    return buf.getvalue()

def _build_buy_task_text(brand: str, domains: list[str]) -> str:
    brand = (brand or "").strip()
    doms = ", ".join(domains or [])
    return (
        f"Задача: купити домен(и) для бренду {brand}\n\n"
        f"Домени:\n{doms}\n\n"
        f"Дія:\n- Перевірити доступність у реєстратора\n- Купити домен(и)\n"
    )

def _build_launch_task_text(brand: str, domains: list[str]) -> str:
    brand = (brand or "").strip()
    doms = ", ".join(domains or [])
    return (
        f"Задача: завести сайт під бренд {brand}\n\n"
        f"Домени:\n{doms}\n\n"
        f"Дія:\n- Додати домен у панель\n- Налаштувати DNS\n- Розгорнути сайт/лонч\n"
    )
def copy_button(text: str, label: str, key: str):
    # json.dumps правильно екранує перенос рядків/лапки/табуляції
    payload = json.dumps(text or "")
    components.html(
        f"""
        <div style="display:flex; gap:8px; align-items:center;">
          <button id="{key}" style="padding:6px 10px; border-radius:8px; border:1px solid #ccc; cursor:pointer;">
            {label}
          </button>
          <span id="{key}_msg" style="font-size:12px; opacity:0.7;"></span>
        </div>
        <script>
          const btn = document.getElementById("{key}");
          const msg = document.getElementById("{key}_msg");
          btn.onclick = async () => {{
            try {{
              await navigator.clipboard.writeText({payload});
              msg.textContent = "Скопійовано ✅";
              setTimeout(() => msg.textContent = "", 1200);
            }} catch(e) {{
              msg.textContent = "Не вдалось скопіювати";
            }}
          }};
        </script>
        """,
        height=42,
    )



def _lang_name_ua(lang_code: str) -> str:
    if not lang_code:
        return "невідомо"

    base = lang_code.split("-")[0].lower()

    mapping = {
        "en": "англійська",
        "it": "італійська",
        "es": "іспанська",
        "de": "німецька",
        "fr": "французька",
        "pt": "португальська",
        "pl": "польська",
        "hu": "угорська",
        "ro": "румунська",
        "nl": "нідерландська",
        "no": "норвезька",
        "sv": "шведська",
        "da": "данська",
        "fi": "фінська",
        "cs": "чеська",
        "sk": "словацька",
        "el": "грецька",
        "tr": "турецька",
    }

    return mapping.get(base, base)

def _build_tsv_row(brand: str, geo_code: str, lang_code: str, domains: list[str]) -> str:
    """TSV rows for copy-paste into Sheets/Excel.

    Brand<TAB>Geo<TAB>Lang<TAB>Domain<TAB>Template<TAB>Review
    """

    brand = (brand or "").strip()
    geo_name = _geo_name_ua(geo_code or "UNKNOWN")
    lang = _lang_name_ua(lang_code)

    ds = [d.strip() for d in (domains or []) if d and d.strip()]

    # чи генерується ревʼю
    review_flag = "Так" if st.session_state.get("generate_review") else "Ні"

    # шаблони для доменів
    domain_templates = st.session_state.get("domain_templates", {})

    if not ds:
        return f"{brand}\t{geo_name}\t{lang}\t-\t-\t{review_flag}"

    rows = []

    for d in ds:
        tpl_id = domain_templates.get(d, "template_1")
        tpl_label = TEMPLATES.get(tpl_id, {}).get("label", tpl_id)

        rows.append(
            f"{brand}\t{geo_name}\t{lang}\t{d}\t{tpl_label}\t{review_flag}"
        )

    return "\n".join(rows)

def _set_geo_widget_to_code(cc: str | None):
    if not cc:
        st.session_state.geo_choice_label = UNKNOWN_GEO_LABEL
        return
    for lbl, code in geo_label_to_code.items():
        if code == cc:
            st.session_state.geo_choice_label = lbl
            return


def _set_lang_widget_to_base(lang_base: str | None):
    if not lang_base:
        st.session_state.lang_choice_label = lang_labels[0]
        return
    for lbl, code in lang_label_to_code.items():
        if code == lang_base:
            st.session_state.lang_choice_label = lbl
            return


def _compute_target_lang():
    geo_label = st.session_state.geo_choice_label
    lang_label = st.session_state.lang_choice_label
    use_region = st.session_state.use_region

    if geo_label == UNKNOWN_GEO_LABEL:
        geo_code = "UNKNOWN"
    else:
        geo_code = geo_label_to_code.get(geo_label, "UNKNOWN")
    st.session_state.geo_code = geo_code

    chosen_base = lang_label_to_code.get(lang_label, "en")

    if geo_code == "UNKNOWN":
        st.session_state.target_lang = chosen_base
        return

    default_bcp47 = geo[geo_code]["lang"]
    default_base = default_bcp47.split("-")[0]

    if chosen_base == default_base:
        st.session_state.target_lang = default_bcp47
    else:
        st.session_state.target_lang = bcp47_from(chosen_base, geo_code, use_region)


def _can_go_step2() -> bool:
    return st.session_state.step1_done is True


def _can_go_step3() -> bool:
    return st.session_state.step2_done is True


def _set_step(n: int):
    if n == 1:
        st.session_state.step = 1
    elif n == 2:
        if _can_go_step2():
            st.session_state.step = 2
        else:
            st.toast("Спочатку пройди Крок 1.", icon="⚠️")
    elif n == 3:
        if _can_go_step3():
            st.session_state.step = 3
        else:
            st.toast("Спочатку пройди Крок 2.", icon="⚠️")
    st.session_state.needs_rerun = True


def _geo_name_ua(geo_code: str) -> str:
    if not geo_code or geo_code == "UNKNOWN":
        return "Невідомо"
    return geo.get(geo_code, {}).get("ua_name", geo_code)


def _build_buy_task_text(brand: str, domains: list[str]) -> str:
    # ПРОСТИЙ ШАБЛОН. Нічого не “вигадуємо”.
    if len(domains) <= 1:
        title_line = f'Купити домен'
    else:
        title_line = f'Купити {len(domains)} домени під "{brand}"'

    zone_value = (st.session_state.get("task_buy_zone") or "").strip()
    tg = st.session_state.get("task_buy_tg") or "—"
    keitaro = st.session_state.get("task_buy_keitaro") or ""
    indexation = st.session_state.get("task_buy_index") or "ДА"

    domains_block = "\n".join([f"{d}" for d in domains]) if domains else "(ще не обрано домени)"

    txt = textwrap.dedent(f"""\
{title_line}

Обязательные поля:
1. Telegram - 
2. Доменная зона - 
3. Список доменов (если без списка, то купим любые):

{domains_block}

4. Добавить на SEO сервер (Да - 5,6,7 пункт пропускаем/Нет) - ДА
5. Номер кейтаро - 
6. Группа в которую закинуть домены - TNA
7. Включить индексацию(Да/Нет) - 
""").strip()
    return txt


def _build_launch_tasks(brand, domains, geo_label, target_lang):
    brand = (brand or "").strip() or "—"
    geo_label = (geo_label or "").strip() or "—"
    target_lang = (target_lang or "").strip() or "—"

    domains = [d.strip() for d in (domains or []) if str(d).strip()]

    if len(domains) <= 1:
        d = domains[0] if domains else "—"
        return f"""Завести розширений офер під {brand}
Бренднейм — {brand}

Домен — {d}

Гео — {geo_label}
Мова — {target_lang}

Готовий архів сайту — прикріпляю

- SEO-інтеграція під TNA
- Обмежувати вибір мови в формі по гео
"""
    else:
        n = len(domains)
        domains_block = "\n".join(domains)
        return f"""Завести {n} розширених офери під {brand}
Бренднейм — {brand}

Домени:

{domains_block}

Гео — {geo_label}
Мова — {target_lang}

Готові архіви сайту — прикріпляю

- SEO-інтеграція під TNA
- Обмежувати вибір мови в формі по гео
"""

# ---------------------------
# Callbacks
# ---------------------------
def on_geo_change():
    geo_label = st.session_state.geo_choice_label

    if geo_label == UNKNOWN_GEO_LABEL:
        st.session_state.geo_code = "UNKNOWN"
        _compute_target_lang()
        return

    geo_code = geo_label_to_code.get(geo_label, "UNKNOWN")
    st.session_state.geo_code = geo_code

    if geo_code == "UNKNOWN":
        _compute_target_lang()
        return

    # Автоматично підтягнути дефолтну мову країни
    default_bcp47 = geo[geo_code]["lang"]
    default_base = default_bcp47.split("-")[0]
    _set_lang_widget_to_base(default_base)
    st.session_state.target_lang = default_bcp47


def on_lang_or_region_change():
    _compute_target_lang()


def run_detect():
    brand = (st.session_state.brand or "").strip()
    if not brand:
        st.session_state.detect_status = "done"
        st.session_state.detect_verdict = "none"
        st.session_state.detect_geo = None
        st.session_state.detect_lang = None
        st.session_state.detect_details = []
        st.session_state.needs_rerun = True
        return

    st.session_state.detect_status = "running"
    st.session_state.detect_verdict = None
    st.session_state.detect_geo = None
    st.session_state.detect_lang = None
    st.session_state.detect_details = []
    st.session_state.needs_rerun = True

    domain_candidates = generate_domain_candidates(brand, None)

    geo_guess, lang_guess, verdict, details = detect_geo_lang(
        brand=brand,
        geo_defaults=geo,
        preferred_geo_order=TOP_GEO_ORDER,
        domain_candidates=domain_candidates,
        search_limit=10,
        probe_limit=12
    )

    st.session_state.detect_status = "done"
    st.session_state.detect_verdict = verdict
    st.session_state.detect_geo = geo_guess
    st.session_state.detect_lang = lang_guess
    st.session_state.detect_details = details
    st.session_state.needs_rerun = True


def apply_detect():
    cc = st.session_state.detect_geo
    lang = st.session_state.detect_lang

    # Є geo + мова -> застосовуємо ОБИДВА значення
    if cc and cc in geo:
        _set_geo_widget_to_code(cc)
        st.session_state.geo_code = cc

        if lang:
            _set_lang_widget_to_base(lang)
            st.session_state.target_lang = bcp47_from(
                lang,
                cc,
                st.session_state.use_region
            )
        else:
            # fallback: дефолтна мова країни, якщо мову не визначили
            default_bcp47 = geo[cc]["lang"]
            default_base = default_bcp47.split("-")[0]
            _set_lang_widget_to_base(default_base)
            st.session_state.target_lang = default_bcp47

    # Є лише мова, але нема geo
    elif lang:
        _set_geo_widget_to_code(None)
        _set_lang_widget_to_base(lang)
        st.session_state.geo_code = "UNKNOWN"
        st.session_state.target_lang = lang

    st.session_state.needs_rerun = True

def mark_serp_checked():
    st.session_state.serp_checked = True
    st.toast("SERP перевірено ✅")


def decision_go():
    st.session_state.decision = "go"
    st.session_state.step1_done = True
    st.session_state.step = 2
    st.session_state.needs_rerun = True
    st.session_state.step2_autocheck_done = False
    st.session_state.step3_autogen_done = False
    st.session_state.generated_files = []
    st.session_state["generated_site_zips"] = {}
    st.session_state.pop("last_generation_time", None)



def decision_no():
    st.session_state.decision = "no"
    reset_all()


def step2_generate_candidates():
    brand = (st.session_state.brand or "").strip()
    if not brand:
        st.toast("Введи бренднейм.", icon="⚠️")
        return

    geo_code = st.session_state.geo_code if st.session_state.geo_code != "UNKNOWN" else None
    ccTLD = None
    if geo_code and geo_code in geo:
        ccTLD = geo[geo_code].get("ccTLD")

    candidates = generate_domain_candidates(brand, ccTLD)
    st.session_state.domain_candidates = candidates
    st.session_state.domain_checks = []
    st.session_state.chosen_domains = []
    st.session_state.domains_checked_done = False
    st.toast("Кандидати доменів згенеровано ✅")
    st.session_state.needs_rerun = True

def add_manual_domain():
    d = _normalize_domain(st.session_state.get("manual_domain_input", ""))

    if not d or "." not in d:
        st.warning("Впиши домен у форматі `example.com`")
        return

    # зберігаємо, щоб не губився
    manual = list(st.session_state.get("manual_domains") or [])
    if d not in manual:
        manual.append(d)
        st.session_state.manual_domains = manual

    # додаємо/оновлюємо у domain_checks як manual
    checks = list(st.session_state.get("domain_checks") or [])
    checks = [x for x in checks if (x.get("domain") or "").lower() != d]
    checks.append({"domain": d, "status": "manual", "reason": "додано вручну"})

    # пересортувати (використовуємо твою функцію сортування)
    st.session_state.domain_checks = _sort_domain_checks(
        checks=checks,
        brand=st.session_state.get("brand") or "",
        geo_code=st.session_state.get("geo_code") or "UNKNOWN",
    )

    st.session_state.manual_domain_input = ""
    st.success(f"Додано вручну: {d}")
    # ✅ Авто-обрати вручну доданий домен
    chosen = list(st.session_state.get("chosen_domains") or [])
    limit = int(st.session_state.get("sites_count") or 1)
    
    if d not in chosen:
        if len(chosen) >= limit:
            # якщо вже обрано максимум — замінимо останній (або просто попередимо)
            st.warning(f"Можна обрати лише {limit}. Спочатку зніми вибір з іншого домену.")
        else:
            chosen.append(d)
            st.session_state.chosen_domains = chosen

    st.rerun()


def step2_check_domains():
    if not st.session_state.domain_candidates:
        step2_generate_candidates()

    checks = check_domains_rdap(st.session_state.domain_candidates[:80])

    # сортуємо: free першими
    checks_sorted = _sort_domain_checks(
        checks=checks,
        brand=st.session_state.get("brand") or "",
        geo_code=st.session_state.get("geo_code") or "UNKNOWN",
    )
    st.session_state.domain_checks = checks_sorted
    st.session_state.domains_checked_done = True

    st.toast("Перевірку завершено ✅")
    st.session_state.needs_rerun = True

def _domain_sort_key(domain: str, brand: str, cc_tld: str | None) -> tuple:
    """
    Стабільне сортування доменів під твій бізнес-порядок.
    Працює з:
      - акцентами (Á -> a)
      - CamelCase (QuanterioItalica -> quanterio-italica)
      - 3-4 словами
      - цифрами (Brand24Pro -> brand-24-pro)
    """
    d = (domain or "").strip().lower()
    host = d.split(".")[0] if "." in d else d
    tld = d.split(".")[-1] if "." in d else ""
    cc = (cc_tld or "").strip().lower()

    # ---------- brand normalization ----------
    raw = (brand or "").strip()

    # 1) "plain" slug (як є)
    slug_plain = slugify_brand(raw)

    # 2) "spaced" slug: розбиваємо CamelCase та межі цифр/літер
    #    QuanterioItalica -> Quanterio Italica
    #    Brand24Pro -> Brand 24 Pro
    spaced = re.sub(r"([a-z])([A-Z])", r"\1 \2", raw)
    spaced = re.sub(r"([A-Za-z])(\d)", r"\1 \2", spaced)
    spaced = re.sub(r"(\d)([A-Za-z])", r"\1 \2", spaced)
    slug_spaced = slugify_brand(spaced)

    # Визначаємо "hyphen base" та "concat base"
    # hyphen: якщо є дефіси (зазвичай slug_spaced), але не завжди
    base_h_candidates = []
    if slug_spaced:
        base_h_candidates.append(slug_spaced)
    if slug_plain and slug_plain != slug_spaced:
        base_h_candidates.append(slug_plain)

    # concat базу беремо з "найбільш дефісної" форми (щоб Brand 24 Pro -> brand24pro)
    base_h_primary = next((x for x in base_h_candidates if "-" in x), base_h_candidates[0] if base_h_candidates else "")
    base_c = (base_h_primary or slug_plain or "").replace("-", "")

    # інколи slug_plain уже без дефісів, але це якраз concat
    # якщо він дає іншу concat-базу — додаємо як запасний варіант
    alt_c = (slug_plain or "").replace("-", "")
    concat_candidates = [base_c]
    if alt_c and alt_c != base_c:
        concat_candidates.append(alt_c)

    # для hyphen теж беремо максимум 2 варіанти (primary -> secondary)
    hyphen_candidates = []
    if base_h_primary:
        hyphen_candidates.append(base_h_primary)
    for x in base_h_candidates:
        if x and x not in hyphen_candidates and "-" in x:
            hyphen_candidates.append(x)
    # якщо взагалі дефісів нема (1 слово), дозволимо hyphen_candidates бути порожнім
    # але slug_spaced може містити дефіс навіть при 1 слові з CamelCase (це нам і потрібно)

    # ---------- helper: match rank inside hyphen/concat variants ----------
    def hyphen_variant_rank(h: str) -> int:
        if not h:
            return 99
        try:
            return hyphen_candidates.index(h)
        except ValueError:
            return 99

    def concat_variant_rank(c: str) -> int:
        if not c:
            return 99
        try:
            return concat_candidates.index(c)
        except ValueError:
            return 99

    # ---------- define preferred patterns (rank map) ----------
    # Порядок як ти хочеш (і як ми вже підкручували):
    # 0) H.com
    # 1) C.com
    # 2) H.org
    # 3) H.net
    # 4) C.org
    # 5) C.net
    # 6) H.cc
    # 7) C.cc
    # 8) H-cc.com
    # 9) C-cc.com
    # 20) base on other tlds (io/pro/app/info/site/...)
    # 30) хвости типу "-pt" на інших tlds
    #
    # Далі — усе інше
    def match_pattern_rank() -> tuple[int, int]:
        # return (pattern_rank, variant_rank)
        # exact hyphen matches
        for h in hyphen_candidates:
            if h and host == h and tld == "com":
                return (0, hyphen_variant_rank(h))
            if h and host == h and tld == "org":
                return (2, hyphen_variant_rank(h))
            if h and host == h and tld == "net":
                return (3, hyphen_variant_rank(h))
            if h and host == f"{h}-official" and tld == "com":
                return (3.5, hyphen_variant_rank(h))
            if cc and h and host == h and tld == cc:
                return (6, hyphen_variant_rank(h))
            if cc and h and host == f"{h}-{cc}" and tld == "com":
                return (8, hyphen_variant_rank(h))

        # exact concat matches
        for c in concat_candidates:
            if c and host == c and tld == "com":
                return (1, concat_variant_rank(c))
            if c and host == c and tld == "org":
                return (4, concat_variant_rank(c))
            if c and host == c and tld == "net":
                return (5, concat_variant_rank(c))
            if cc and c and host == c and tld == cc:
                return (7, concat_variant_rank(c))
            if cc and c and host == f"{c}-{cc}" and tld == "com":
                return (9, concat_variant_rank(c))

        # base hosts on "other" TLDs (io/pro/app/info/site etc) — нижче
        for h in hyphen_candidates:
            if h and host == h:
                return (20, hyphen_variant_rank(h))
        for c in concat_candidates:
            if c and host == c:
                return (20, concat_variant_rank(c))

        # hosts starting with base + "-" (geo/other suffix) — ще нижче
        for h in hyphen_candidates:
            if h and host.startswith(h + "-"):
                return (30, hyphen_variant_rank(h))
        for c in concat_candidates:
            if c and host.startswith(c + "-"):
                return (30, concat_variant_rank(c))

        return (99, 99)

    pr, vr = match_pattern_rank()
    return (pr, vr, d)
def _sort_domain_checks(checks: list[dict], brand: str, geo_code: str) -> list[dict]:
    # ccTLD з geo_defaults
    cc_tld = None
    if geo_code and geo_code != "UNKNOWN" and geo_code in geo:
        cc_tld = geo[geo_code].get("ccTLD")

    # статусний порядок: free -> taken -> unknown
    def status_rank(x: dict) -> int:
        s = (x.get("status") or "unknown").lower()
        if s == "free":
            return 0
        if s == "manual":
            return 1
        if s == "taken":
            return 2
        return 3

    return sorted(
        checks,
        key=lambda x: (
            status_rank(x),
            _domain_sort_key(x.get("domain", ""), brand, cc_tld),
        )
    )


def add_domain(domain: str):
    k = int(st.session_state.sites_count)
    chosen = list(st.session_state.chosen_domains)

    if domain in chosen:
        return
    if len(chosen) >= k:
        return

    chosen.append(domain)
    st.session_state.chosen_domains = chosen

    # default template assignment: 1st -> template_1, 2nd -> template_2, 3rd -> template_1 ...
    dt = st.session_state.get("domain_templates") or {}
    if domain not in dt:
        idx = len(chosen) - 1
        dt[domain] = "template_1" if (idx % 2 == 0) else "template_2"
    st.session_state["domain_templates"] = dt

    st.session_state.needs_rerun = True


def remove_domain(domain: str):
    chosen = [d for d in st.session_state.chosen_domains if d != domain]
    st.session_state.chosen_domains = chosen

    dt = st.session_state.get("domain_templates") or {}
    dt.pop(domain, None)
    st.session_state["domain_templates"] = dt

    st.session_state.needs_rerun = True


def clear_domains():
    st.session_state.chosen_domains = []
    st.session_state["domain_templates"] = {}
    st.session_state.needs_rerun = True


def step2_continue():
    k = int(st.session_state.sites_count)
    if len(st.session_state.chosen_domains) != k:
        st.toast(f"Потрібно обрати рівно {k} домен(и).", icon="⚠️")
        return

    st.session_state.step2_done = True
    st.session_state.step = 3
    st.session_state.needs_rerun = True

    # скидаємо генерацію lang.php
    st.session_state["step3_autogen_done"] = False
    st.session_state["generated_files"] = []
    st.session_state["last_generation_time"] = None
    st.session_state["archives_ready"] = False
    st.session_state["generated_site_zips"] = {}

    # скидаємо ревʼю
    st.session_state["generated_review"] = None
    st.session_state["step3_review_autogen_done"] = False
    st.session_state["review_generation_error"] = None

    st.rerun()


def copy_domain(domain: str):
    st.session_state._copy_buf = domain
    st.toast(f"Скопіюй домен: {domain}", icon="📋")
    st.session_state.needs_rerun = True


# ---------------------------
# Top progress / step bar
# ---------------------------
st.markdown('<div class="sitehdr">', unsafe_allow_html=True)
with st.container(border=True):
    st.markdown('<div class="sitehdr-anchor"></div>', unsafe_allow_html=True)


    progress = (st.session_state.step - 1) / (TOTAL_STEPS - 1)
    st.progress(progress)
    st.caption(f"Крок {st.session_state.step} з {TOTAL_STEPS}")

    nav_cols = st.columns(3)
    with nav_cols[0]:
        st.button("Бренд / Гео / SERP", on_click=lambda: _set_step(1), use_container_width=True)
    with nav_cols[1]:
        st.button("Домени", on_click=lambda: _set_step(2), use_container_width=True, disabled=not _can_go_step2())
    with nav_cols[2]:
        st.button("lang.php", on_click=lambda: _set_step(3), use_container_width=True, disabled=not _can_go_step3())

# divider після хедера НЕ треба — він робить зайву висоту
# st.divider()


# divider після хедера прибираємо — він додає висоту
# st.divider()


# ВАЖЛИВО: divider після хедера можна прибрати або лишити
# st.divider()



# ---------------------------
# Sidebar (global)
# ---------------------------
with st.sidebar:
    st.header("Параметри")

    st.text_input("Бренднейм", key="brand", placeholder="CapvexOne / capvex one / πλάτων")

    if st.session_state.geo_choice_label == UNKNOWN_GEO_LABEL:
        st.button("🧭 Визначити гео", type="primary", on_click=run_detect, use_container_width=True)

    st.selectbox(
        "Гео (країна) — шукай за 🇺🇦/🇬🇧/кодом",
        options=[UNKNOWN_GEO_LABEL] + geo_labels,
        key="geo_choice_label",
        on_change=on_geo_change
    )

    if st.session_state.geo_code != "UNKNOWN":
        st.caption(f"Валюта: **{geo[st.session_state.geo_code]['currency']}**")
        st.caption(f"Дефолтна мова країни: **{geo[st.session_state.geo_code]['lang']}**")
    else:
        st.caption("Валюта: **unknown**")
        st.caption("Дефолтна мова країни: **unknown**")

    st.subheader("Мова")
    st.selectbox("Вибери мову", options=lang_labels, key="lang_choice_label", on_change=on_lang_or_region_change)
    st.checkbox("Додати регіон до мови (en-PL, de-DE…)", key="use_region", on_change=on_lang_or_region_change)

    if st.session_state.target_lang == "unknown":
        _compute_target_lang()

    st.success(f"Цільова мова: {st.session_state.target_lang}")

    # --- TSV ---
    st.markdown("### 📋 TSV")
    
    brand = (st.session_state.get("brand") or "").strip()
    geo_code = st.session_state.get("geo_code") or "UNKNOWN"
    lang_code = st.session_state.get("target_lang") or "en"
    
    domains = st.session_state.get("chosen_domains") or []
    tsv = _build_tsv_row(brand, geo_code, lang_code, domains)
    
    st.sidebar.text_area(
        " ",
        value=tsv,
        height=90,
        label_visibility="collapsed",
    )
    
    copy_button(tsv, "📋 Скопіювати TSV", key="copy_tsv_btn")
    
    st.sidebar.caption("TSV = поля розділені табуляцією. Встав у Sheets/Excel — розіб’ється на колонки.")
    
    st.divider()
       
    st.sidebar.divider()
    st.sidebar.markdown("### ✅ Обрані домени")
    
    chosen = list(st.session_state.get("chosen_domains") or [])
    
    if not chosen:
        st.sidebar.caption("Ще нічого не обрано.")
    else:
        domains_txt = "\n".join(chosen)
    
        st.sidebar.text_area(
            " ",
            value=domains_txt,
            height=80 if len(chosen) <= 2 else 110,
            label_visibility="collapsed",
        )
    
        copy_button(domains_txt, "📋 Скопіювати домени", key="copy_domains_btn")
    
    
    
    if st.button("🔄 Скинути все", use_container_width=True):
        reset_all()


def _normalize_domain(s: str) -> str:
    s = (s or "").strip().lower()
    s = s.replace("https://", "").replace("http://", "")
    s = s.split("/")[0].strip()
    # прибрати випадкові пробіли
    s = s.replace(" ", "")
    return s
# ---------------------------
# STEP 1
# ---------------------------
if st.session_state.step == 1:
    st.subheader("Крок 1 — Визначення гео/мови + ручна перевірка SERP")

    if st.session_state.detect_status == "running":
        st.info("Визначаю гео/мову…")

    if st.session_state.detect_status == "done" and st.session_state.detect_verdict is not None:
        verdict = st.session_state.detect_verdict
        cc = st.session_state.detect_geo
        lg = st.session_state.detect_lang

        if verdict == "exact" and cc:
            st.success(f"✅ Визначено гео: **{cc}**, мова: **{lg or 'unknown'}**")
            st.button("✅ Застосувати", type="primary", on_click=apply_detect, use_container_width=True)

        elif verdict == "lang_only" and lg:
            st.warning(f"⚠️ Визначено мову: **{lg}**. Ймовірне гео: **{cc or 'невідомо'}** (орієнтовно)")
            st.button("✅ Застосувати (орієнтовно)", type="primary", on_click=apply_detect, use_container_width=True)
        else:
            st.error("❌ Не вдалося визначити гео/мову автоматично.")

        with st.expander("Деталі перевірок"):
            details = st.session_state.detect_details or []
            for r in details:
                if getattr(r, "ok", False):
                    st.markdown(f"- [{r.source}] {r.input} → **OK {r.status_code}** | lang={r.lang} | geo={r.geo}")
                    if getattr(r, "signals", None):
                        st.caption("Сигнали: " + ", ".join(r.signals[:8]))
                else:
                    st.markdown(f"- [{getattr(r,'source','?')}] {getattr(r,'input','?')} → **FAIL** | {getattr(r,'error','')}")

    st.divider()
    st.subheader("SERP (ручний крок)")

    if st.session_state.brand and st.session_state.geo_code != "UNKNOWN" and st.session_state.target_lang != "unknown":
        hl = st.session_state.target_lang.split("-")[0]
        q = urllib.parse.quote_plus(st.session_state.brand.strip())
        serp_url = f"https://www.google.com/search?q={q}&gl={geo[st.session_state.geo_code]['gl']}&hl={hl}"
        st.link_button("Відкрити Google SERP", serp_url, use_container_width=True)
        st.code(serp_url, language="text")
    else:
        st.info("Введи бренд + визнач/вибери гео, щоб з’явився SERP-лінк.")

    st.divider()
    cols = st.columns([1, 1, 2])
    with cols[0]:
        st.button("✅ Я перевірив SERP", on_click=mark_serp_checked, use_container_width=True)
    with cols[1]:
        st.button("✅ Запускаємось", type="primary", on_click=decision_go, disabled=not st.session_state.serp_checked, use_container_width=True)
    with cols[2]:
        st.button("⛔ Не заходимо (очистити все)", on_click=decision_no, use_container_width=True)

    if not st.session_state.serp_checked:
        st.caption("Щоб перейти на Крок 2, спочатку натисни “Я перевірив SERP”.")

    st.divider()

# ---------------------------
# STEP 2
# ---------------------------


elif st.session_state.step == 2:
    st.subheader("Крок 2 — Домени: генерація → перевірка → вибір + таска на покупку")
    # --- AUTO: одразу перевіряємо домени при заході на крок 2 (1 раз) ---
    if not st.session_state.get("step2_autocheck_done"):
        st.session_state.step2_autocheck_done = True
        with st.spinner("🔎 Автоматично перевіряю домени…"):
            step2_check_domains()
        st.rerun()


    st.session_state.sites_count = st.radio(
        "Скільки сайтів запускаємо?",
        [1, 2, 3, 4, 5],
        index=[1, 2, 3, 4, 5].index(int(st.session_state.sites_count)),
        horizontal=True
    )

    left, right = st.columns([2, 3])

    
    
    with left:
        st.markdown("### 2.1 Перевірка доступності доменів")
        st.button("🔁 Перевірити ще раз", on_click=step2_check_domains, use_container_width=True)

        st.divider()
        st.markdown("### 2.2 Вибір доменів")
        k = int(st.session_state.sites_count)
        chosen = st.session_state.chosen_domains

        st.write(f"Обери **{k}** домен(и). Обрано: **{len(chosen)}/{k}**")

        

    
        # --- Template selection lives HERE (Step 2) ---
        dt = st.session_state.get("domain_templates") or {}
        # ensure defaults exist for already chosen domains (alternating 1,2,1...)
        for i_d, d in enumerate(chosen):
            if d not in dt:
                dt[d] = "template_1" if (i_d % 2 == 0) else "template_2"
        st.session_state["domain_templates"] = dt

        if chosen:
            for d in chosen:
                tpl = dt.get(d, "template_1")
                favicon_path = TEMPLATES.get(tpl, TEMPLATES["template_1"]).get("favicon")

                c_fav, c_dom, c_tpl, c_rm = st.columns([0.6, 3.2, 2.4, 0.8], gap="small")
                with c_fav:
                    if os.path.exists(favicon_path):
                        st.image(favicon_path, width=22)
                    else:
                        st.write("🧩")
                with c_dom:
                    st.code(d, language="text")
                with c_tpl:
                    # quick per-domain selector
                    new_tpl = st.selectbox(
                        " ",
                        options=list(TEMPLATES.keys()),
                        index=list(TEMPLATES.keys()).index(tpl) if tpl in TEMPLATES else 0,
                        format_func=lambda x: f"{TEMPLATES[x]['label']}",
                        key=f"tpl_{d}",
                        label_visibility="collapsed",
                    )
                    if new_tpl != tpl:
                        dt[d] = new_tpl
                        st.session_state["domain_templates"] = dt
                with c_rm:
                    st.button("🗑️", key=f"rm_{d}", on_click=lambda dd=d: remove_domain(dd), help="Прибрати домен")
        else:
            st.info("Поки нічого не обрано.")

        st.button("🧹 Очистити вибір", on_click=clear_domains, use_container_width=True)
        st.divider()
        st.checkbox("Сформувати ревʼю", key="generate_review")

        st.button(
            "➡️ Далі до Кроку 3",
            type="primary",
            disabled=(len(st.session_state.chosen_domains) != int(st.session_state.sites_count)),
            use_container_width=True,
            on_click=step2_continue,
        )


    with right:
        st.markdown("### Список доменів")
        st.markdown("### ➕ Додати домен вручну")
        
        c1, c2 = st.columns([3, 1])
        with c1:
            st.text_input(
                " ",
                key="manual_domain_input",
                placeholder="example.com",
                label_visibility="collapsed",
            )
        with c2:
            st.button("Додати", on_click=add_manual_domain, use_container_width=True)
        
        st.divider()

        st.caption(f"Кандидатів: {len(st.session_state.domain_candidates)} | Перевірено: {len(st.session_state.domain_checks)}")

        # 1) якщо є checks — показуємо checks (free зверху, зелені)
        if st.session_state.domain_checks:
            # ⭐ Знаходимо рекомендований домен: перший "free" у відсортованому списку
            recommended = None
            for r in st.session_state.domain_checks:
                if (r.get("status") or "").lower() == "free":
                    recommended = r.get("domain", "")
                    break

            for row in st.session_state.domain_checks[:120]:
                domain = row.get("domain", "")
                status = row.get("status", "unknown")  # free|taken|unknown
                reason = row.get("reason", "")

                is_chosen = domain in st.session_state.chosen_domains
                k = int(st.session_state.sites_count)
                is_full = len(st.session_state.chosen_domains) >= k

                if status == "free":
                    badge = "🟩 Вільний"
                elif status == "manual":
                    badge = "🟦 Вручну"
                elif status == "taken":
                    badge = "🟥 Зайнятий"
                else:
                    badge = "🟨 Невідомо"


                box = st.container(border=True)
                with box:
                    top = st.columns([3, 1, 1, 1])
                    with top[0]:
                        star = " ⭐ Рекомендую" if (recommended and domain == recommended) else ""
                        st.markdown(f"**{badge}** — `{domain}`{star}")
                        if recommended and domain == recommended:
                            st.caption("⭐ Рекомендований варіант (найкращий з доступних)")

                        if reason:
                            st.caption(reason)

                    with top[1]:
                        st.markdown('<div class="hide-code-text">', unsafe_allow_html=True)
                        st.code(domain, language="text")
                        st.markdown('</div>', unsafe_allow_html=True)
                    with top[2]:
                        st.link_button("🔗 Відкрити", f"https://{domain}")
                    with top[3]:
                        disabled_pick = is_chosen or (is_full and not is_chosen)
                        label = "✅ Обрано" if is_chosen else "➕ Обрати"
                        st.button(label, key=f"pick_{domain}", disabled=disabled_pick, on_click=lambda d=domain: add_domain(d))

        # 2) якщо checks ще нема, але кандидати є — показуємо список кандидатів (без статусу)
        elif st.session_state.domain_candidates:
            st.info("Домени згенеровані. Натисни “Перевірити домени”, щоб побачити статус (вільний/зайнятий).")
            st.code("\n".join(st.session_state.domain_candidates[:80]), language="text")

        else:
            st.info("Натисни “Перевірити домени”.")


# ---------------------------
# STEP 3
# ---------------------------
elif st.session_state.step == 3:
    st.subheader("Крок 3 — Генерація `lang.php` + таски")
    
    _missing_lang = [t["lang"] for t in TEMPLATES.values() if not os.path.exists(t["lang"])]
    if _missing_lang:
        st.error("Не знайдено файл(и) шаблону lang.php: " + ", ".join(_missing_lang))
    else:
        brand = (st.session_state.get("brand") or "").strip()
        domains = list(st.session_state.get("chosen_domains") or [])
        geo_code = st.session_state.get("geo_code") or "UNKNOWN"
        target_lang = st.session_state.get("target_lang") or "en"

        geo_currency = "EUR"
        if geo_code != "UNKNOWN" and geo_code in geo:
            geo_currency = geo[geo_code].get("currency", "EUR")

        if not domains:
            st.error("Немає обраних доменів. Повернись на Крок 2.")
        else:
            st.markdown("## 🧾 Таски")

            buy_txt = _build_buy_task_text(brand, domains)
            launch_txt = _build_launch_tasks(brand, domains, geo_code, target_lang)

            c1, c2 = st.columns(2)
            with c1:
                st.text_area("ТЗ купівля", buy_txt, height=300)
                copy_button(buy_txt, "📋 Скопіювати", "copy_buy")

            with c2:
                st.text_area("ТЗ запуск", launch_txt, height=300)
                copy_button(launch_txt, "📋 Скопіювати", "copy_launch")

            st.divider()

            # --- генерація ---
            progress = st.progress(0)
            status = st.empty()

            def progress_cb(p, msg):
                progress.progress(p)
                status.info(msg)

            MODEL = "gpt-5-mini"

            should_autogen = (
                (not st.session_state.get("generated_files"))
                and (not st.session_state.get("step3_autogen_done"))
            )

            if should_autogen or st.button("🚀 Згенерувати / Перегенерувати"):
                st.session_state["step3_autogen_done"] = True
                try:
                    files = generate_lang_files_multi(
                        template1_bytes=open(TEMPLATES["template_1"]["lang"], "rb").read(),
                        template2_bytes=open(TEMPLATES["template_2"]["lang"], "rb").read(),
                        template3_bytes=open(TEMPLATES["template_3"]["lang"], "rb").read(),
                        domain_templates=st.session_state.get("domain_templates", {}),
                        geo_code=geo_code,
                        geo_currency=geo_currency,
                        target_lang=target_lang,
                        domains=domains,
                        brand=brand,
                        model=MODEL,
                        progress_cb=progress_cb,
                        geo_defaults=geo,
                    )

                    st.session_state["generated_files"] = files
                    status.success("Готово ✅")
                    progress.progress(1.0)
                    st.session_state["auto_download_done"] = False

                except Exception as e:
                    st.error(f"Помилка: {e}")

            files = st.session_state.get("generated_files") or []
            if not files:
                st.error("❌ Нічого не згенерилось (можливо LLM помилка або rate limit)")
                st.caption("Можливі причини: timeout, rate limit, помилка LLM")

            if files:
                st.divider()
                st.markdown("### 📥 Завантаження")


                # --- сайти ---
                st.markdown("#### ZIP сайти")

                TEMPLATE_DIRS = {
                    "template_1": "templates/template_1-1",
                    "template_2": "templates/template_2",
                    "template_3": "templates/template_3",
                }

                dt = st.session_state.get("domain_templates", {})

                if "generated_site_zips" not in st.session_state:
                    st.session_state["generated_site_zips"] = {}

                for i, item in enumerate(files):
                    domain = item["domain"]

                    try:
                        if domain not in st.session_state["generated_site_zips"]:
                            tpl_id = dt.get(domain, "template_1")
                            tpl_dir = TEMPLATE_DIRS.get(tpl_id, TEMPLATE_DIRS["template_1"])

                            st.session_state["generated_site_zips"][domain] = build_domain_site_zip(
                                domain=domain,
                                site_template_dir=tpl_dir,
                                lang_php_content=item["content"],
                                target_lang=target_lang,
                                geo_code=geo_code.lower(),
                                brand=brand,
                            )

                        st.download_button(
                            f"⬇️ {domain}.zip",
                            data=st.session_state["generated_site_zips"][domain],
                            file_name=f"{domain}.zip",
                            key=f"zip_{i}"
                        )

                    except Exception as e:
                        st.warning(f"{domain}: {e}")

                st.session_state["archives_ready"] = True

            # --- REVIEW GENERATION ---
            should_autogen_review = (
                st.session_state.get("generate_review")
                and bool(files)
                and not st.session_state.get("generated_review")
                and not st.session_state.get("step3_review_autogen_done")
            )
            
            if should_autogen_review:
                review_box = st.empty()
            
                try:
                    review_box.info("⏳ Генерую ревʼю...")
            
                    main_domain = domains[0] if domains else ""
                    country_name_en = (
                        geo.get(geo_code, {}).get("name")
                        or geo.get(geo_code, {}).get("en_name")
                        or geo_code
                    ) if geo_code != "UNKNOWN" else "Unknown"
            
                    with st.spinner("Генерую ревʼю..."):
                        review = generate_review(
                            template_path="templates/template_for_review",
                            platform_name=brand,
                            official_website=main_domain,
                            availability_country=country_name_en,
                            currency=geo_currency,
                            model=MODEL,
                        )
            
                    if not isinstance(review, dict):
                        raise ValueError("generate_review повернув некоректний результат")
            
                    st.session_state["generated_review"] = review
                    st.session_state["review_generation_error"] = None
                    st.session_state["step3_review_autogen_done"] = True
            
                    review_box.empty()
                    st.success("Ревʼю згенеровано ✅")
            
                except Exception as e:
                    st.session_state["generated_review"] = None
                    st.session_state["review_generation_error"] = str(e)
                    st.session_state["step3_review_autogen_done"] = False
                    review_box.error(f"Помилка генерації ревʼю: {e}")
            
            # --- REVIEW UI ---
            review = st.session_state.get("generated_review")
            review_error = st.session_state.get("review_generation_error")
            
            if (
                st.session_state.get("generate_review")
                or review
                or review_error
            ):
                st.divider()
                st.markdown("### 📝 Ревʼю")
            
                if review_error:
                    st.error(review_error)
            
                elif isinstance(review, dict):
                    st.text_input("H1", value=review.get("h1", ""), key="review_h1_view")
                    copy_button(review.get("h1", ""), "📋 Скопіювати H1", key="copy_review_h1")
            
                    st.text_input("Title", value=review.get("title", ""), key="review_title_view")
                    copy_button(review.get("title", ""), "📋 Скопіювати Title", key="copy_review_title")
            
                    st.text_area("Description", value=review.get("description", ""), height=100, key="review_desc_view")
                    copy_button(review.get("description", ""), "📋 Скопіювати Description", key="copy_review_desc")
            
                    st.text_input("Slug", value=review.get("slug", ""), key="review_slug_view")
                    copy_button(review.get("slug", ""), "📋 Скопіювати Slug", key="copy_review_slug")
            
                    st.text_area("HTML", value=review.get("html", ""), height=650, key="review_html_view")
                    copy_button(review.get("html", ""), "📋 Скопіювати HTML", key="copy_review_html")
            
                else:
                    st.info("Ревʼю ще не згенеровано або генерація не завершилась.")
            
                if st.button("🔁 Перегенерувати ревʼю", use_container_width=True):
                    st.session_state["generated_review"] = None
                    st.session_state["step3_review_autogen_done"] = False
                    st.session_state["review_generation_error"] = None
                    st.rerun()


# ---------------------------
# Safe rerun
# ---------------------------
if st.session_state.get("needs_rerun"):
    st.session_state.needs_rerun = False
    st.rerun()
