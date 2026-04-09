from __future__ import annotations
import os
import re
import json
import random
from typing import Dict, List, Optional, Callable, Tuple
import time



# OpenAI (required)
try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# -----------------------------
# Config
# -----------------------------
TEMPLATE_LANG_BASE = "de"        # шаблон завжди німецький
DEFAULT_MODEL = "gpt-5-mini"     # оптимально по швидкості/ціні (ВАЖЛИВО: без temperature)


# ---- спец-змінні (НЕ перекладати, лише встановлювати значення присвоєнням) ----
SPECIAL_NUMERIC = {"app_price", "rating_value", "rating_count"}
SPECIAL_STRING = {
    "site_url",
    "app_currency",
    "site_lang",
    "adress_name",
    "site_gmail",
    "feedback_strong_1",
    "feedback_strong_2",
    "feedback_strong_3",
    "feedback_strong_4",
    "feedback_strong_5",
    "feedback_strong_6",
    "page_title_main",
    "page_description_main",
    "site_name",
    "crypto_img",
}

CURRENCY_FALLBACK = {
    # Base
    "EUR": 1.0,

    # Major currencies
    "USD": 1.08,
    "GBP": 0.85,
    "CHF": 0.95,
    "JPY": 165.0,
    "AUD": 1.65,
    "CAD": 1.47,
    "NZD": 1.78,

    # Europe
    "PLN": 4.30,
    "CZK": 25.0,
    "HUF": 390.0,
    "RON": 5.0,
    "SEK": 11.0,
    "NOK": 11.0,
    "DKK": 7.5,
    "BGN": 1.96,
    "HRK": 7.53,
    "RSD": 117.0,
    "UAH": 42.0,
    "ISK": 150.0,
    "ALL": 100.0,
    "BAM": 1.96,
    "MDL": 19.0,

    # Middle East
    "TRY": 33.0,
    "ILS": 4.0,
    "AED": 3.97,
    "SAR": 4.05,
    "QAR": 3.95,
    "KWD": 0.33,
    "BHD": 0.41,
    "OMR": 0.42,
    "JOD": 0.77,
    "IRR": 450000.0,

    # Asia
    "CNY": 7.8,
    "HKD": 8.5,
    "SGD": 1.45,
    "KRW": 1450.0,
    "INR": 90.0,
    "THB": 39.0,
    "MYR": 5.1,
    "IDR": 17000.0,
    "PHP": 61.0,
    "VND": 27000.0,
    "TWD": 34.0,
    "PKR": 300.0,
    "BDT": 120.0,
    "LKR": 340.0,

    # Americas
    "MXN": 18.5,
    "BRL": 5.4,
    "ARS": 950.0,
    "CLP": 950.0,
    "COP": 4300.0,
    "PEN": 4.1,
    "UYU": 42.0,
    "BOB": 7.5,
    "PYG": 7900.0,
    "DOP": 64.0,
    "CRC": 550.0,

    # Africa
    "ZAR": 20.0,
    "EGP": 52.0,
    "MAD": 10.8,
    "TND": 3.4,
    "KES": 170.0,
    "GHS": 15.0,
    "NGN": 1700.0,
    "UGX": 4200.0,
    "TZS": 2800.0,
    "XOF": 655.96,
    "XAF": 655.96,

    # Crypto (approx vs EUR)
    "BTC": 0.000018,
    "ETH": 0.00027,
    "USDT": 1.08,
    "USDC": 1.08,
}


CRYPTO_IMAGES = {
    "IT":"italy.png",
    "DE":"germany.png",
    "PL":"poland.png",
    "ES":"spain.png",
    "GB":"united-kingdom.png",
    "CZ":"czech.png",
    "SE":"sweden.png",
    "TR":"turkey.png",
    "PT":"portugal.png",
    "RO":"romania.png",
    "AT":"austria.png",
    "FR":"france.png",
    "CA":"canada.png",
    "CH":"switzerland.png",
    "NZ":"new-zealand.png",
    "FI":"finland.png",
    "AU":"australia.png",
    "NL":"netherlands.png",
    "IE":"ireland.png",
    "BE":"belgium.png",
}

# -----------------------------
# Utils
# -----------------------------
def _round_to_step(x: float, step: int) -> int:
    return int(round(x / step) * step)


def _round_dynamic(x: float) -> int:
    """
    Динамічне округлення:
    - < 400      → до 50
    - 400–1499   → до 100
    - 1500–8999  → до 500
    - 9000+      → до 1000
    """
    if x < 400:
        step = 50
    elif x < 1500:
        step = 100
    elif x < 9000:
        step = 500
    else:
        step = 1000

    return _round_to_step(x, step)


def _make_price(currency: str) -> int:
    """
    Ціна ≈ 250 EUR у валюті країни,
    з динамічним округленням залежно від суми.
    """
    rate = CURRENCY_FALLBACK.get(currency, 1.0)
    price = 250.0 * rate
    return max(50, _round_dynamic(price))



def _escape_php_string_for_quote(s: str, quote: str) -> str:
    """
    Екранування рядка перед вставкою всередину PHP-літерала.
    quote: "'" або '"'
    """
    # завжди екрануємо бекслеш
    s = s.replace("\\", "\\\\")

    if quote == "'":
        # у single quotes потрібно екранувати тільки апостроф
        s = s.replace("'", "\\'")
    else:
        # у double quotes екрануємо тільки подвійні лапки
        # НЕ чіпаємо $, інакше $source стане \$source
        s = s.replace('"', '\\"')

    return s


def _infer_cc_from_target_lang(target_lang: str, geo_code: Optional[str]) -> str:
    # 1) geo_code має пріоритет якщо схожий на ISO2
    if geo_code and isinstance(geo_code, str):
        g = geo_code.strip().upper()
        if len(g) == 2 and g != "UN" and g.isalpha():
            return g

    # 2) пробуємо витягнути з BCP47 (en-US -> US)
    if target_lang and "-" in target_lang:
        tail = target_lang.split("-")[-1].strip().upper()
        if len(tail) == 2 and tail.isalpha():
            return tail

    # 3) fallback
    return "DE"


def _gmail_for_domain(domain: str) -> str:
    base = domain.split(".")[0].lower()
    base = re.sub(r"[^a-z0-9\-]", "", base)
    return f"support.{base}@gmail.com"


def _set_php_var(content: str, var: str, value: str, numeric: bool) -> str:
    """
    Безпечно: змінює ТІЛЬКИ присвоєння $var = ...;
    Не робить глобальний replace $var по всьому файлу.
    """
    if numeric:
        rhs = str(value)
    else:
        rhs = f"\"{_escape_php_string(str(value))}\""

    pattern = re.compile(rf"(^\s*\${re.escape(var)}\s*=\s*)(.*?)(;\s*$)", re.MULTILINE)
    if pattern.search(content):
        # ВАЖЛИВО: \g<1> і \g<3>, щоб числа не ламали group refs
        return pattern.sub(rf"\g<1>{rhs}\g<3>", content, count=1)

    insert_line = f"${var} = {rhs};\n"
    php_open = re.search(r"^\s*<\?php\s*", content)
    if php_open:
        lines = content.splitlines(True)
        for i, ln in enumerate(lines):
            if "<?php" in ln:
                lines.insert(i + 1, insert_line)
                return "".join(lines)
    return insert_line + content


# -----------------------------
# OpenAI helpers
# -----------------------------

def _escape_php_string(s: str) -> str:
    # fallback: безпечне екранування для single-quoted PHP рядків
    return s.replace("\\", "\\\\").replace("'", "\\'")
    
def _get_openai_client() -> OpenAI:
    if OpenAI is None:
        raise RuntimeError("Бібліотека `openai` не встановлена. Додай `openai` у requirements.txt.")
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Не знайдено OPENAI_API_KEY (Streamlit Secrets/Environment).")
    return OpenAI(api_key=api_key)


_JSON_OBJECT_RE = re.compile(r"\{.*\}", re.DOTALL)


def _safe_json_loads(s: str) -> dict:
    """
    Повертає dict, навіть якщо модель підмішала текст.
    """
    s = (s or "").strip()
    if not s:
        return {}
    try:
        return json.loads(s)
    except Exception:
        # пробуємо вирізати перший JSON-об’єкт у відповіді
        m = _JSON_OBJECT_RE.search(s)
        if not m:
            return {}
        try:
            return json.loads(m.group(0))
        except Exception:
            return {}

_JSON_LIKE_RE = re.compile(r"^\s*[\{\[].*[\}\]]\s*$", re.DOTALL)

def _maybe_parse_jsonish(s: str):
    s = (s or "").strip()
    if not s or not _JSON_LIKE_RE.match(s):
        return None
    # пробуємо як JSON
    try:
        return json.loads(s)
    except Exception:
        pass
    # пробуємо як python-dict з одинарними лапками (дуже частий випадок)
    try:
        import ast
        return ast.literal_eval(s)
    except Exception:
        return None

def _format_address_from_obj(obj) -> str:
    """
    Приводить {'street_name':..., 'street_number':..., 'postal_code':..., 'city':..., 'country_name':...}
    у нормальний рядок: "Хрещатик 22, 01001 Київ, Україна"
    """
    if not isinstance(obj, dict):
        return ""
    street = str(obj.get("street_name", "")).strip()
    num = str(obj.get("street_number", "")).strip()
    pc = str(obj.get("postal_code", "")).strip()
    city = str(obj.get("city", "")).strip()
    country = str(obj.get("country_name", "")).strip()

    left = " ".join([x for x in [street, num] if x]).strip()
    mid = " ".join([x for x in [pc, city] if x]).strip()
    right = country

    parts = [p for p in [left, mid, right] if p]
    return ", ".join(parts)


def _llm_json(client: OpenAI, model: str, system: str, payload: dict) -> dict:
    """
    GPT-5* НЕ підтримує temperature — тому тут НІКОЛИ його не передаємо.
    """
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": json.dumps(payload, ensure_ascii=False)},
        ],
        response_format={"type": "json_object"},
    )
    txt = resp.choices[0].message.content or "{}"
    return _safe_json_loads(txt)


# -----------------------------
# Placeholder protection (CRITICAL)
# -----------------------------
PH_RE = re.compile(r"(\$[A-Za-z_]\w*|%(\d+\$)?[sdif])")

def _protect_placeholders(s: str) -> tuple[str, dict]:
    """
    Замінює $placeholders на токени __PH0__ щоб LLM їх не чіпав.
    """
    placeholders: List[str] = []

    def repl(m):
        placeholders.append(m.group(0))
        return f"__PH{len(placeholders) - 1}__"

    protected = PH_RE.sub(repl, s)
    token_map = {f"__PH{i}__": placeholders[i] for i in range(len(placeholders))}
    return protected, token_map


def _restore_placeholders(s: str, token_map: dict) -> str:
    for token, ph in token_map.items():
        s = s.replace(token, ph)
    return s


# -----------------------------
# LLM Specials generation (always new, uses $source)
# -----------------------------
def _generate_specials_via_llm(
    client: OpenAI,
    model: str,
    domain: str,
    cc: str,
    target_lang: str,
) -> Dict[str, str]:

    system = (
        "Ти SEO-копірайтер для AI-trading / trading platform лендингів. "
        "Поверни ТІЛЬКИ JSON. Без пояснень. "
        "Усі тексти мають бути ПОВНІСТЮ мовою target_lang. "
        "Стиль: короткий, рекламний, природний, схожий на native SEO. "
        "Пріоритетні теми: trading platform, AI trading, market analysis, trading signals, algorithms. "
        "Не зловживай словами про investment/returns/profits. "
        "Уникай стилю crypto hype, financial promises, exaggerated claims."
    )

    payload = {
        "target_language": target_lang,
        "country_code": cc,
        "source_placeholder": "$source",
        "requirements": {
            "title": {
                "patterns": [
                    "$source | {phrase}",
                    "$source 2026 | {phrase}",
                    "{phrase} – $source"
                ],
                "length_min": 42,
                "length_max": 68,
                "style": "short, native, SEO-friendly, promotional but clean",
                "prefer_topics": [
                    "AI trading platform",
                    "market analysis",
                    "trading signals",
                    "AI algorithms",
                    "smart trading",
                    "trading hub"
                ],
                "avoid_topics": [
                    "crypto",
                    "cryptocurrency",
                    "autopilot",
                    "passive income",
                    "fast payouts",
                    "capital protection",
                    "guaranteed returns"
                ],
                "examples_style_only": [
                    "$source | Plataforma de trading con IA",
                    "$source 2026 | Trading con IA y análisis de mercados",
                    "$source | Hub de trading con inteligencia artificial",
                    "Trading inteligente con IA – $source"
                ]
            },
            "description": {
                "length_min": 125,
                "length_max": 158,
                "must_start_with_source": True,
                "style": "clean landing page SEO description",
                "preferred_structure": [
                    "$source + 1 emoji + short platform description",
                    "benefit/value",
                    "1 more emoji near benefit or CTA",
                    "soft CTA"
                ],
                "prefer_topics": [
                    "AI trading platform",
                    "market analysis",
                    "signals",
                    "algorithms",
                    "tools for traders",
                    "real-time analysis"
                ],
                "avoid_topics": [
                    "guaranteed profits",
                    "maximize returns",
                    "passive income",
                    "risk-free",
                    "mobile app",
                    "start in minutes",
                    "free trial",
                    "autopilot"
                ],
                "emoji_rules": {
                    "min_count": 2,
                    "max_count": 2,
                    "allowed": ["⭐", "⚡", "🔥", "🚀", "✅", "💰", "➡️"],
                    "placement": [
                        "one emoji right after $source",
                        "one emoji after a benefit phrase",
                        "never cluster emojis together",
                        "never put both emojis at the end"
                    ]
                },
                "examples_style_only": [
                    "$source ⭐ — plataforma de trading con IA y señales en tiempo real ⚡ Descubre herramientas modernas para seguir el mercado con más claridad.",
                    "$source ✅ — hub de trading con inteligencia artificial para análisis de mercado 🔥 Únete a traders que buscan señales y datos en tiempo real.",
                    "$source 🚀 — plataforma de IA para analizar mercados y detectar señales ⭐ Explora una forma más moderna de seguir oportunidades de trading."
                ]
            },
            "address": {
                "type": "realistic full address",
                "must_include": [
                    "street_name",
                    "street_number",
                    "postal_code",
                    "city",
                    "country_name"
                ],
                "must_match_country_code": True
            },
            "personas": {
                "count": 4,
                "format_strict": "STRING ONLY",
                "no_last_names": True,
                "no_json_objects": True,
                "no_dicts": True,
                "age_range": "31-49",
                "output_format": "Name, <age> <localized age word>, City",
                "examples": [
                    "Олександр, 34 роки, Київ",
                    "Марія, 41 рік, Львів",
                    "Leon, 41 Jahre, Stuttgart",
                    "Tommaso, 46 anni, Milano",
                    "Lucía, 37 años, Madrid"
                ]
            }
        }
    }

    data = _llm_json(client, model, system, payload)

    title = str(data.get("title", "")).strip()
    desc = str(data.get("description", "")).strip()
    raw_address = data.get("address", "")
    address = str(raw_address).strip()

    if isinstance(raw_address, dict):
        address = _format_address_from_obj(raw_address) or address
    else:
        parsed = _maybe_parse_jsonish(address)
        if isinstance(parsed, dict):
            address = _format_address_from_obj(parsed) or address

    personas = data.get("personas", [])

    allowed_emoji = "⭐⚡🔥🚀✅💰➡️"

    def _base_lang(lang: str) -> str:
        return (lang or "en").split("-")[0].split("_")[0].lower()

    def _title_fallback(lang: str) -> str:
        base = _base_lang(lang)
        if base == "es":
            return "$source | Plataforma de trading con IA"
        if base == "it":
            return "$source | Piattaforma di trading con AI"
        if base == "fr":
            return "$source | Plateforme de trading avec IA"
        if base == "de":
            return "$source | KI-Trading-Plattform"
        if base == "pt":
            return "$source | Plataforma de trading com IA"
        if base == "pl":
            return "$source | Platforma tradingowa AI"
        if base == "uk":
            return "$source | Платформа AI-трейдингу"
        return "$source | AI Trading Platform"

    def _desc_fallback(lang: str) -> str:
        base = _base_lang(lang)
        if base == "es":
            return "$source ⭐ — plataforma de trading con IA y análisis de mercado en tiempo real ⚡ Descubre señales y herramientas modernas para seguir el mercado."
        if base == "it":
            return "$source ⭐ — piattaforma di trading con AI e analisi di mercato in tempo reale ⚡ Scopri segnali e strumenti moderni per seguire il mercato."
        if base == "fr":
            return "$source ⭐ — plateforme de trading avec IA et analyse de marché en temps réel ⚡ Découvrez des signaux et outils modernes pour suivre le marché."
        if base == "de":
            return "$source ⭐ — KI-Trading-Plattform mit Marktanalyse in Echtzeit ⚡ Entdecke Signale und moderne Tools, um den Markt besser zu verfolgen."
        if base == "pt":
            return "$source ⭐ — plataforma de trading com IA e análise de mercado em tempo real ⚡ Descubra sinais e ferramentas modernas para acompanhar o mercado."
        if base == "pl":
            return "$source ⭐ — platforma tradingowa AI z analizą rynku w czasie rzeczywistym ⚡ Poznaj sygnały i nowoczesne narzędzia do śledzenia rynku."
        if base == "uk":
            return "$source ⭐ — платформа AI-трейдингу з аналізом ринку в реальному часі ⚡ Відкрийте сигнали та сучасні інструменти для роботи з ринком."
        return "$source ⭐ — AI trading platform with real-time market analysis ⚡ Discover signals and modern tools to follow the market more effectively."

    def _clean_spaces(s: str) -> str:
        s = re.sub(r"\s+", " ", s or "").strip()
        s = re.sub(r"\s+([,.;:!?])", r"\1", s)
        return s

    def _normalize_dash_after_source(s: str) -> str:
        s = re.sub(r"^\$source\s*[—–\-:|]\s*", "$source ⭐ — ", s, flags=re.IGNORECASE)
        return s

    def _remove_disallowed_phrases(s: str) -> str:
        bad_patterns = [
            r"\bautopilot\b",
            r"\bcrypto(currency)?\b",
            r"\bsecure payouts?\b",
            r"\bfast payouts?\b",
            r"\bcapital protection\b",
            r"\bguaranteed returns?\b",
            r"\bmaximize (your )?returns?\b",
            r"\bmaximiza (tus )?retornos\b",
            r"\bretornos\b",
            r"\bpassive income\b",
            r"\brisk[- ]?free\b",
            r"\bfree trial\b",
            r"\bprueba gratis\b",
            r"\bstart in minutes\b",
            r"\bempezar en minutos\b",
            r"\bdesde el móvil\b",
            r"\bmobile\b",
            r"\bapp\b",
        ]
        out = s
        for p in bad_patterns:
            out = re.sub(p, "", out, flags=re.IGNORECASE)
        out = re.sub(r"\s{2,}", " ", out)
        out = re.sub(r"\s+([,.;:!?])", r"\1", out)
        return out.strip(" ,;:-")

    def _remove_emoji_clusters(s: str) -> str:
        # ⭐⚡ -> лишаємо першу, другу прибираємо
        s = re.sub(rf"([{allowed_emoji}])\s*([{allowed_emoji}])+", r"\1", s)
        return s

    def _extract_emojis(s: str) -> list[str]:
        return re.findall(rf"[{allowed_emoji}]", s or "")

    def _remove_all_allowed_emojis(s: str) -> str:
        return re.sub(rf"[{allowed_emoji}]", "", s or "")

    def _ensure_title_shape(s: str, lang: str) -> str:
        s = _clean_spaces(s)
        s = _remove_disallowed_phrases(s)

        if "$source" not in s:
            return _title_fallback(lang)

        # прибираємо зайві емодзі з title
        s = _remove_all_allowed_emojis(s)
        s = _clean_spaces(s)

        patterns = [
            r"^\$source\s*\|\s*.+$",
            r"^\$source\s+2026\s*\|\s*.+$",
            r"^.+\s+[–-]\s+\$source$",
        ]
        if not any(re.match(p, s) for p in patterns):
            tail = s.replace("$source", "").strip(" |-–—:;,.")
            if not tail:
                return _title_fallback(lang)
            s = f"$source | {tail}"

        # легке підчищення від investment-style, але без жорсткої заборони
        replace_map = {
            r"\bInversión automática\b": "Trading con IA",
            r"\bInversión con IA\b": "Trading con IA",
            r"\bAutomatic investment\b": "AI Trading",
            r"\bInvestimento automatico\b": "Trading con AI",
        }
        for pat, repl in replace_map.items():
            s = re.sub(pat, repl, s, flags=re.IGNORECASE)

        s = _clean_spaces(s)

        if len(s) < 42:
            return _title_fallback(lang)
        if len(s) > 68:
            s = s[:68].rstrip(" ,;:-|")
            if "$source" not in s:
                return _title_fallback(lang)

        return s

    def _ensure_two_emojis_spread(s: str) -> str:
        s = _remove_emoji_clusters(s)
        emojis = _extract_emojis(s)

        # прибираємо зайві, залишаємо максимум 2
        if len(emojis) > 2:
            kept = 0
            out = []
            for ch in s:
                if re.match(rf"[{allowed_emoji}]", ch):
                    kept += 1
                    if kept > 2:
                        continue
                out.append(ch)
            s = "".join(out)

        emojis = _extract_emojis(s)

        if len(emojis) == 0:
            if "$source" in s:
                s = s.replace("$source", "$source ⭐", 1)
            if "." in s:
                s = s.replace(".", " ⚡.", 1)
            else:
                s += " ⚡"
            return s

        if len(emojis) == 1:
            # якщо є emoji біля $source, другу ставимо ближче до вигоди
            if "." in s:
                first_dot = s.find(".")
                if first_dot != -1:
                    s = s[:first_dot] + " ⚡" + s[first_dot:]
                else:
                    s += " ⚡"
            else:
                s += " ⚡"

        return s

    def _ensure_desc_shape(s: str, lang: str) -> str:
        s = _clean_spaces(s)
        s = _remove_disallowed_phrases(s)

        if "$source" not in s:
            s = _desc_fallback(lang)

        if not s.startswith("$source"):
            s = re.sub(r"^.*?\$source", "$source", s)
            if not s.startswith("$source"):
                s = "$source — " + s.lstrip("—-:| ")

        s = _normalize_dash_after_source(s)
        s = _clean_spaces(s)

        # прибираємо емодзі не з whitelist
        s = re.sub(r"[📈📉💸💵💶💷]", "", s)

        # якщо модель пішла занадто в investment angle, підтягуємо назад до trading/platform
        rewrites = {
            r"\binvertir automáticamente con inteligencia artificial\b": "plataforma de trading con inteligencia artificial",
            r"\binversión automática con inteligencia artificial\b": "trading con inteligencia artificial",
            r"\bautomatic investment with artificial intelligence\b": "AI trading platform",
            r"\binvestimento automatico con intelligenza artificiale\b": "piattaforma di trading con intelligenza artificiale",
        }
        for pat, repl in rewrites.items():
            s = re.sub(pat, repl, s, flags=re.IGNORECASE)

        s = _ensure_two_emojis_spread(s)
        s = _clean_spaces(s)

        # якщо CTA зовсім дивний/агресивний — м'який fallback
        if re.search(r"\b(prueba gratis|free trial|maximiza|retornos|risk-free|guaranteed)\b", s, flags=re.IGNORECASE):
            s = _desc_fallback(lang)

        if len(s) < 125:
            s = _desc_fallback(lang)

        if len(s) > 158:
            s = s[:158].rstrip(" ,;:-")
            # після обрізки якщо загубилась логіка — fallback
            if "$source" not in s or len(_extract_emojis(s)) < 2:
                s = _desc_fallback(lang)

        # фінальна страховка: рівно 2 whitelist-емодзі, без кластерів
        s = _remove_emoji_clusters(s)
        s = _ensure_two_emojis_spread(s)
        s = _clean_spaces(s)

        return s

    def _format_persona(name: str, age: str, city: str, target_lang: str) -> str:
        base = (target_lang.split("-")[0] if target_lang else "en").lower()
        try:
            age_i = int(float(age))
        except Exception:
            age_i = random.randint(31, 49)

        if base == "uk":
            word = "рік" if age_i % 10 == 1 and age_i % 100 != 11 else "роки"
            return f"{name or 'Олександр'}, {age_i} {word}, {city or 'Київ'}"
        if base == "de":
            return f"{name or 'Leon'}, {age_i} Jahre, {city or 'Stuttgart'}"
        if base == "pl":
            return f"{name or 'Jan'}, {age_i} lat, {city or 'Warszawa'}"
        if base == "cs":
            return f"{name or 'Jan'}, {age_i} let, {city or 'Praha'}"
        if base == "es":
            return f"{name or 'Lucía'}, {age_i} años, {city or 'Madrid'}"
        if base == "it":
            return f"{name or 'Tommaso'}, {age_i} anni, {city or 'Milano'}"
        if base == "fr":
            return f"{name or 'Camille'}, {age_i} ans, {city or 'Paris'}"
        return f"{name or 'Alex'}, {age_i} years, {city or 'London'}"

    def _persona_to_text(p, target_lang: str) -> str:
        if isinstance(p, dict):
            name = str(p.get("name", "")).strip()
            age = str(p.get("age", "")).strip()
            city = str(p.get("city", "")).strip()
            if name:
                name = name.split()[0]
            return _format_persona(name, age, city, target_lang)

        s = str(p).strip()
        if not s:
            return ""

        if s.startswith("{") and "name" in s and "city" in s:
            return ""

        # залишаємо тільки ім'я без прізвища
        s = re.sub(r"^([^\s,]+)\s+[^\s,]+", r"\1", s)
        return s

    title = _ensure_title_shape(title, target_lang)
    desc = _ensure_desc_shape(desc, target_lang)
    desc = re.sub(r"\$source([⭐⚡🔥🚀✅💰➡️])", r"$source \1", desc)

    if not isinstance(personas, list):
        personas = []

    clean = []
    for p in personas:
        txt = _persona_to_text(p, target_lang)
        if txt:
            clean.append(txt)

    while len(clean) < 4:
        clean.append(_format_persona("", "", "", target_lang))

    personas = clean[:4]

    if not address:
        address = f"Main Street 10, 10000 Capital City, {cc}"

    return {
        "adress_name": address,
        "feedback_strong_1": personas[0],
        "feedback_strong_2": personas[1],
        "feedback_strong_3": personas[2],
        "feedback_strong_4": personas[3],
        "page_title_main": title,
        "page_description_main": desc,
    }
    

    def _norm_source_dash(s: str) -> str:
        s = (s or "").strip()
        if s.startswith("$source") and not s.startswith("$source —"):
            # прибираємо можливий пробіл/коми після $source
            s = re.sub(r"^\$source\s*[-–—:]?\s*", "$source — ", s)
        return s
    
    def _strip_emoji_inside_words(s: str) -> str:
        # якщо емодзі встромили всередину слова/після коми без пробілу — нормалізуємо пробілами
        s = re.sub(r"([A-Za-zА-Яа-яІЇЄієї0-9])([⭐⚡🔥🚀✅🔒])", r"\1 \2", s)
        s = re.sub(r"([⭐⚡🔥🚀✅🔒])([A-Za-zА-Яа-яІЇЄієї0-9])", r"\1 \2", s)
        return s
    
    def _kill_comma_checklist(desc: str) -> str:
        """
        Якщо модель зробила опис як чекліст через коми — перетворюємо на нормальний текст.
        """
        d = (desc or "").strip()
    
        # дуже грубий сигнал: багато ком + слова-маркери
        if d.count(",") >= 6 and "official" in d.lower() and "trusted" in d.lower():
            # прибираємо "csv" стиль
            d = re.sub(r"\s*,\s*", ", ", d)  # норм пробіли
            # замінюємо перший великий список на фразу
            d = re.sub(
                r"(official,\s*trusted,\s*verified,\s*secure,\s*stable results,\s*fast payouts,\s*capital protection\.?)",
                "official and trusted platform with verified security, stable results, fast payouts and capital protection.",
                d,
                flags=re.IGNORECASE
            )
        return d
    def _ensure_4_emojis_spread(s: str) -> str:
        # гарантуємо 4 емодзі, але ставимо їх після розділових знаків
        allowed = ["⭐", "⚡", "🔥", "🚀", "✅", "🔒"]
        found = re.findall(r"[⭐⚡🔥🚀✅🔒]", s)
        if len(found) >= 4:
            return s
        need = 4 - len(found)
        add = allowed[:need]
    
        # пробуємо вставити після крапок/двокрапок/крапки з комою
        parts = re.split(r"([.!?:])", s)
        if len(parts) >= 3:
            # додаємо емодзі після перших кількох розділових
            out = ""
            ei = 0
            for i in range(0, len(parts), 2):
                chunk = parts[i]
                punct = parts[i+1] if i+1 < len(parts) else ""
                out += chunk + punct
                if punct and ei < len(add):
                    out += " " + add[ei]
                    ei += 1
            s = out
        else:
            s = s + " " + " ".join(add)
    
        return s
    
    def _persona_to_text(p, target_lang: str) -> str:
        # приймає або рядок, або dict, і повертає рядок "Name, age ..., City"
        if isinstance(p, dict):
            name = str(p.get("name", "")).strip()
            age = str(p.get("age", "")).strip()
            city = str(p.get("city", "")).strip()
            # прибрати прізвище якщо є (беремо перше слово)
            if name:
                name = name.split()[0]
            return _format_persona(name, age, city, target_lang)
    
        s = str(p).strip()
        # якщо це строка з dict-подібним виглядом — не приймаємо
        if s.startswith("{") and "name" in s and "city" in s:
            return ""
        # якщо є прізвище — обріжемо до 1 слова
        # формати типу "Олександр Іваненко, 34..." або "Олександр Іваненко"
        s = re.sub(r"^([^\s,]+)\s+[^\s,]+", r"\1", s)
        return s
    
    def _format_persona(name: str, age: str, city: str, target_lang: str) -> str:
        base = (target_lang.split("-")[0] if target_lang else "en").lower()
        try:
            age_i = int(float(age))
        except Exception:
            age_i = random.randint(31, 49)
    
        if base == "uk":
            word = "рік" if age_i % 10 == 1 and age_i % 100 != 11 else "роки"
            return f"{name or 'Олександр'}, {age_i} {word}, {city or 'Київ'}"
        if base == "de":
            return f"{name or 'Leon'}, {age_i} Jahre, {city or 'Stuttgart'}"
        if base == "pl":
            return f"{name or 'Jan'}, {age_i} lat, {city or 'Warszawa'}"
        if base == "cs":
            return f"{name or 'Jan'}, {age_i} let, {city or 'Praha'}"
        if base == "es":
            return f"{name or 'Lucía'}, {age_i} años, {city or 'Madrid'}"
        if base == "it":
            return f"{name or 'Tommaso'}, {age_i} anni, {city or 'Milano'}"
        if base == "fr":
            return f"{name or 'Camille'}, {age_i} ans, {city or 'Paris'}"
        # fallback англ
        return f"{name or 'Alex'}, {age_i} years, {city or 'London'}"
    
    
    # --- нормалізація title/desc ---
    title = _norm_source_dash(title)
    desc = _norm_source_dash(desc)
    desc = _strip_emoji_inside_words(desc)
    desc = _ensure_4_emojis_spread(desc)
    desc = _kill_comma_checklist(desc)
    desc = re.sub(r"\s*([.!?])\s*", r"\1 ", desc).strip()  # акуратна пунктуація
    

    
    # --- нормалізація personas ---
    if not isinstance(personas, list):
        personas = []
    
    clean = []
    for p in personas:
        txt = _persona_to_text(p, target_lang)
        if txt:
            clean.append(txt)
    
    # добиваємо до 4 якщо модель дала фігню
    while len(clean) < 4:
        clean.append(_format_persona("", "", "", target_lang))
    
    personas = clean[:4]


    # -------------------------
    # ЖОРСТКА ВАЛІДАЦІЯ
    # -------------------------

    # TITLE FIX
    if not title.startswith("$source"):
        title = "$source | Official Cryptocurrency Trading Platform"

    if len(title) < 60:
        title += " with Advanced AI System"
    if len(title) > 100:
        title = title[:100]

    # DESCRIPTION FIX
    if not desc.startswith("$source"):
        desc = "$source ⭐ Official AI crypto platform with secure autopilot ⚡ Stable results and fast payouts 🔒 Join today and grow 🚀"

    # Перевірка емодзі
    emojis = re.findall(r"[⭐⚡🔥🚀✅🔒]", desc)
    if len(emojis) < 4:
        desc += " ⭐⚡🚀🔒"

    # Обрізка довжини
    if len(desc) > 160:
        desc = desc[:160]

    # ADDRESS fallback
    if not address:
        address = f"Main Street 10, 10000 Capital City, {cc}"

    # PERSONAS fallback
    if not isinstance(personas, list):
        personas = []

    personas = [str(x).strip() for x in personas if str(x).strip()]
    while len(personas) < 4:
        personas.append("Leon, 41 Jahre, Stuttgart")

    personas = personas[:4]

    return {
        "adress_name": address,
        "feedback_strong_1": personas[0],
        "feedback_strong_2": personas[1],
        "feedback_strong_3": personas[2],
        "feedback_strong_4": personas[3],
        "page_title_main": title,
        "page_description_main": desc,
    }



# -----------------------------
# Batch translate/unique (NO SKIPS)
# -----------------------------
# Covers:
#   $var = "text";
#   $var = 'text';
_ASSIGN_RE = re.compile(
    r"""(^\s*\$(?:[A-Za-z_]\w*|lang\[\s*(?:'[^']+'|"[^"]+")\s*\])\s*=\s*)("([^"\\]|\\.)*"|'([^'\\]|\\.)*')(\s*;\s*$)""",
    re.MULTILINE
)
_STRING_LITERAL_RE = re.compile(
    r"""('([^'\\]|\\.)*'|"([^"\\]|\\.)*")""",
    re.DOTALL
)

def _extract_all_string_literals(template: str):
    items = []
    for m in _STRING_LITERAL_RE.finditer(template):
        literal = m.group(1)  # '...'/"..."
        inner = literal[1:-1] # без лапок (але з escape)
        items.append({
            "full": literal,
            "start": m.start(1),
            "end": m.end(1),
            "text": inner,
        })
    return items

def _var_name_from_prefix(prefix: str) -> Optional[str]:
    m = re.match(r"^\s*\$([A-Za-z_]\w*)\s*=", prefix)
    return m.group(1) if m else None


def _is_string_safe_to_transform(s: str) -> bool:
    low = s.lower()
    if low.startswith("http://") or low.startswith("https://"):
        return False
    # емейли теж краще не трансформувати
    if "@" in s:
        return False
    return True


def _extract_php_array_strings(content):
    pattern = r'\[\s*"([^"]+)"'
    return re.findall(pattern, content)

def _extract_strings(content: str) -> Tuple[List[str], List[Tuple[int, int]]]:
    """
    1) Рядки у присвоєннях: $x = "..."; та $lang['k'] = '...';
    2) Рядки всередині масивів для змінних *_list:
       $foo_list = [
         'a',
         'b',
       ];
    Пропускаємо SPECIAL_* змінні — їх виставляє генератор.
    """
    strings: List[str] = []
    spans: List[Tuple[int, int]] = []

    # --- (A) прості присвоєння з одним літералом ---
    for m in _ASSIGN_RE.finditer(content):
        prefix = m.group(1)
        literal = m.group(2)
        var = _var_name_from_prefix(prefix) or ""

        if var in SPECIAL_NUMERIC or var in SPECIAL_STRING:
            continue

        # strip quotes (тільки для фільтрів)
        if literal.startswith('"'):
            inner = literal[1:-1].replace('\\"', '"').replace("\\\\", "\\")
        else:
            inner = literal[1:-1].replace("\\'", "'").replace("\\\\", "\\")

        if not inner.strip():
            continue
        if not _is_string_safe_to_transform(inner):
            continue

        strings.append(inner)
        start = m.start(2) + 1
        end = m.end(2) - 1
        spans.append((start, end))

    # --- (B) масиви для *_list: перекладаємо кожен рядковий елемент ---
    # знаходимо "$something_list = [" і парсимо до відповідного "];"
    list_start_re = re.compile(r"(^\s*\$([A-Za-z_]\w*_list)\s*=\s*\[)", re.MULTILINE)

    for m in list_start_re.finditer(content):
        var = m.group(2)
        if var in SPECIAL_NUMERIC or var in SPECIAL_STRING:
            continue

        start_idx = m.end(1)  # позиція одразу після "$var_list = ["
        i = start_idx
        depth = 1
        n = len(content)

        # простий сканер дужок [] з урахуванням лапок (щоб не зламатися на тексті)
        in_sq = False
        in_dq = False
        escape = False

        while i < n and depth > 0:
            ch = content[i]

            if escape:
                escape = False
                i += 1
                continue

            if ch == "\\":
                escape = True
                i += 1
                continue

            if not in_dq and ch == "'" :
                in_sq = not in_sq
                i += 1
                continue

            if not in_sq and ch == '"':
                in_dq = not in_dq
                i += 1
                continue

            if not in_sq and not in_dq:
                if ch == "[":
                    depth += 1
                elif ch == "]":
                    depth -= 1

            i += 1

        if depth != 0:
            continue  # незакритий масив — пропускаємо

        block_start = start_idx
        block_end = i - 1  # позиція символа ']'
        block = content[block_start:block_end]

        # тепер всередині блоку знаходимо всі '...' / "..."
        for sm in _STRING_LITERAL_RE.finditer(block):
            literal = sm.group(1)
            inner = literal[1:-1]  # без лапок (escape лишаємо як є)

            if not inner.strip():
                continue
            if not _is_string_safe_to_transform(inner):
                continue

            # глобальні позиції в content: +block_start
            lit_start = block_start + sm.start(1) + 1
            lit_end = block_start + sm.end(1) - 1

            strings.append(inner)
            spans.append((lit_start, lit_end))

    return strings, spans

def _apply_strings(content: str, spans: List[Tuple[int, int]], outs: List[str]) -> str:
    if len(spans) != len(outs):
        return content

    pairs = list(zip(spans, outs))
    pairs.sort(key=lambda x: x[0][0], reverse=True)

    for (start, end), new_text in pairs:
        # визначаємо, які лапки були в оригіналі (символ перед start)
        quote = '"'
        if start - 1 >= 0 and content[start - 1] in {"'", '"'}:
            quote = content[start - 1]

        safe = _escape_php_string_for_quote(new_text, quote)
        content = content[:start] + safe + content[end:]

    return content

    pairs = list(zip(spans, outs))
    pairs.sort(key=lambda x: x[0][0], reverse=True)
    for (start, end), new_text in pairs:
        content = content[:start] + _escape_php_string(new_text) + content[end:]
    return content


gender_map = {
    "feedback_description_1": "female",
    "feedback_description_2": "female",
    "feedback_description_3": "male",
    "feedback_description_4": "female",
    "feedback_description_5": "male",
    "feedback_description_6": "male",
}


def _llm_transform_strings_onepass(
    client: OpenAI,
    model: str,
    strings: List[str],
    target_lang: str,
    geo_code: str,
) -> List[str]:
    """
    1 LLM-запит на весь список рядків.
    Повертає список тієї ж довжини, без зміни плейсхолдерів.
    """
    base = (target_lang.split("-")[0] if target_lang else TEMPLATE_LANG_BASE).lower()
    mode = "unique" if base == TEMPLATE_LANG_BASE else "translate_unique"

    protected_list: List[str] = []
    maps: List[dict] = []
    for s in strings:
        ps, mp = _protect_placeholders(s)
        protected_list.append(ps)
        maps.append(mp)

    
    system = (
        "You are processing a list of website phrases. "
        "Return ONLY strict JSON: {\"out\": [\"...\", \"...\"]}. "
        f"The output language MUST be strictly ISO language code: {target_lang}. "
        "Translate EVERY string to the target language. Even single words like 'Name', 'Contact', 'Email', 'Join'. Do not keep any words from the original language."
        "The website is for users in the specified country. Do not change the country."
        "Do NOT mix languages. "
        "Rules:\n"
        "1) Length of 'out' equals length of 'in'.\n"
        "2) Keep order.\n"
        "3) Do NOT modify tokens like __PH0__, __PH1__.\n"
        "4) Return only plain strings inside JSON.\n"
        "5) No explanations."
        "6) Some strings are user reviews. Gender order:1 female, 2 female, 3 male, 4 female, 5 male, 6 male.  Ensure the translation keeps the correct gender."
        
    )

    task = (
        "Rewrite each string in German with light uniqueness, preserving meaning."
        if mode == "unique"
        else f"Translate each string into ISO language '{target_lang}' with light uniqueness, preserving meaning."
    )

    data = _llm_json(
        client,
        model,
        system,
        {"task": task, "in": protected_list},
    )

    out = data.get("out")
    if not isinstance(out, list) or len(out) != len(protected_list):
        # якщо модель зламалась — повертаємо як є (краще ніж зламати php)
        out = protected_list

    # restore placeholders
    restored = []
    for s, mp in zip(out, maps):
        t = str(s)
        t = str(s).replace("\r", " ").replace("\n", " ").strip()
        restored.append(_restore_placeholders(t, mp))
    
    return restored



def _llm_batch_transform(client: OpenAI, model: str, strings: List[str], target_lang: str) -> List[str]:
    """
    Повертає список тієї ж довжини.
    Якщо щось пішло не так — дробимо батч.
    ВАЖЛИВО: без temperature (GPT-5*).
    """
    base = (target_lang.split("-")[0] if target_lang else TEMPLATE_LANG_BASE).lower()
    mode = "unique" if base == TEMPLATE_LANG_BASE else "translate_unique"

    protected_list: List[str] = []
    maps: List[dict] = []
    for s in strings:
        ps, mp = _protect_placeholders(s)
        protected_list.append(ps)
        maps.append(mp)



    def run_once(batch: List[str]) -> Optional[List[str]]:
        data = _llm_json(
            client,
            model,
            system,
            {"task": task, "out_lang": (TEMPLATE_LANG_BASE if mode == "unique" else target_lang), "in": batch},
        )
        out = data.get("out")
        if isinstance(out, list) and len(out) == len(batch):
            return [str(x) for x in out]
        return None

    out = run_once(protected_list)
    
    # 1 ретрай дрібнішим батчем
    if out is None and len(protected_list) > 1:
        mid = len(protected_list) // 2
        left = run_once(protected_list[:mid])
        right = run_once(protected_list[mid:])
        if left is not None and right is not None:
            out = left + right
    
    # якщо все одно не вийшло — НЕ дробимо до 1 (бо це робить 5 хв),
    # а повертаємо як є (але placeholders збережені)
    if out is None:
        out = protected_list

    restored = []
    for s, mp in zip(out, maps):
        t = str(s).replace("\r", " ").replace("\n", " ").strip()
        restored.append(_restore_placeholders(t, mp))
    return restored



# -----------------------------
# Public API
# -----------------------------
def _llm_transform_whole_php(client: OpenAI, model: str, php_text: str, target_lang: str) -> str:
    base = (target_lang.split("-")[0] if target_lang else TEMPLATE_LANG_BASE).lower()
    mode = "unique" if base == TEMPLATE_LANG_BASE else "translate_unique"

    # захистимо плейсхолдери $... по всьому файлу
    protected, mp = _protect_placeholders(php_text)

    system = (
        "Ти редагуєш PHP-файл з масивом текстів. "
        "Поверни ТІЛЬКИ повний PHP-текст (НЕ JSON). "
        "ВАЖЛИВО: токени виду __PH0__ __PH1__ ... НЕ змінювати, не перекладати, не видаляти. "
        "НЕ змінюй назви змінних ($var), НЕ міняй структуру PHP, не чіпай числа, URL, email. "
        "Змінюй ТІЛЬКИ текст усередині лапок у присвоєннях виду: $var = \"...\"; або $var = '...'; "
        "Плейсхолдери, які були як $something, вже захищені токенами — їх залиш як є."
    )

    task = (
        "Перефразуй (унікалізуй) НІМЕЦЬКИЙ текст у рядках присвоєння. "
        "Зміст той самий, але формулювання інше. Не роби довшим >20%."
        if mode == "unique"
        else f"Переклади на {target_lang} і зроби легку унікалізацію. Не роби довшим >20%."
    )

    user = (
        f"ЗАВДАННЯ: {task}\n\n"
        "ОСОБЛИВО ВАЖЛИВО:\n"
        "- Не чіпай рядки зі спец-змінними: site_url, app_currency, site_lang, adress_name, site_gmail, "
        "feedback_strong_1..4, page_title_main, page_description_main, site_name.\n"
        "- Не змінюй $source, __PH..__.\n"
        "- Не змінюй порядок рядків.\n\n"
        "PHP:\n"
        + protected
    )

    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    )
    out = (resp.choices[0].message.content or "").strip()

    # якщо модель випадково обгорнула в ``` — приберемо
    if out.startswith("```"):
        out = re.sub(r"^```[a-zA-Z]*\n", "", out)
        out = re.sub(r"\n```$", "", out)

    out = _restore_placeholders(out, mp)
    return out





# -----------------------------
# Template 2 manual generation
# -----------------------------
TEMPLATE2_MANUAL_VARS = [
    "site_name","site_url","rating_value","rating_count","app_price","app_currency","site_lang",
    "hero_main_heading","hero_main_highlight",
    "main_title","main_description",
    "test1_name","test2_name","test3_name","test1_profit","test2_profit","test3_profit",
    "test4_name","test5_name","test6_name","test4_profit","test5_profit","test6_profit",
    "single_test1_name","single_test2_name","single_test3_name",
]

def _hero_highlight_amount(currency: str) -> int:
    """Return an amount for hero highlight roughly equivalent to ~$1000/day.
    Requirement: for EUR use 950. For others: convert 1000 USD -> EUR -> currency then round nicely.
    """
    if (currency or "").upper() == "EUR":
        return 950
    # 1000 USD -> EUR (we assume 1 EUR ~= 1.08 USD from our fallback table)
    usd_to_eur = 1.0 / max(0.0001, CURRENCY_FALLBACK.get("USD", 1.08))
    eur_amount = 1000.0 * usd_to_eur
    rate = CURRENCY_FALLBACK.get(currency, 1.0)
    val = eur_amount * rate
    return max(100, _round_dynamic(val))

def _generate_template2_manual_via_llm(
    client: OpenAI,
    model: str,
    cc: str,
    target_lang: str,
    currency: str,
    app_price: int,
    hero_amount: int,
    brand: str,
    profit_amounts: Dict[str, float],
) -> Dict[str, str]:
    """Generate localized strings for template2 MANUAL variables that must be geo/language aware."""
    system = (
        "You are a localization + copywriting engine for PHP landing templates. "
        "Return ONLY valid JSON. Preserve numeric values as-is (do not change digits), "
        "and do not introduce any extra variables or placeholders."
    )

    payload = {
        "task": "Generate localized MANUAL strings for template 2",
        "country_code": cc,
        "target_lang": target_lang,
        "currency": currency,
        "brand": brand,
        "app_price": app_price,
        "hero_amount": hero_amount,
        "profit_amounts": profit_amounts,
        "rules": [
            "hero_main_heading should mean 'Earn over' / 'Make over' in the target language (short).",
            "hero_main_highlight must include the currency symbol/code AND the hero_amount number. Keep it punchy, like '€950 DAILY'.",
            "main_title must follow ONE of these patterns only: '$source | {phrase}', '$source 2026 | {phrase}', or '{phrase} – $source'.",
            "main_title must be 42-68 characters long, localized, natural, and focused on AI trading / trading platform / market analysis / signals / algorithms.",
            "Prefer words equivalent to: trading platform, AI trading, market analysis, signals, smart trading, trading hub.",
            "Avoid words equivalent to: automated investing, modern investors, passive income, guaranteed returns, maximize returns, profitable, crypto, autopilot, fast payouts.",
            "main_description must start with the brand name exactly as provided.",
            "main_description must be 125-158 characters long.",
            "main_description should follow this structure: brand + 1 emoji + short platform description, then benefit/value, then 1 more emoji near the end.",
            "Use exactly 2 emojis максимум, never together, never both at the end.",
            "Allowed emoji style: ⭐, ⚡, 🔥, 🚀, ✅, 💰, ➡️",
            "main_description should sound like a landing-page SEO description for an AI trading platform, not an investing blog or finance app.",
            "Avoid phrases equivalent to: invest automatically, maximize returns, rentable, from your mobile, start in minutes, free trial, passive income.",
            "Names must sound plausible for the specified country/locale. Use fictional people.",
            "For each profit string, format the given numeric amount with the currency and in a natural local style for the target language/locale. Keep numbers unchanged.",
            "!!!Important!!!Gender rules: test1_name male, test2_name female, test3_name male, test4_name male, test5_name male, test6_name female, single_test1_name female, single_test2_name male, single_test3_name male.",
            "Gender constraints: test1_name male, test2_name female, test3_name male, test4_name male, test5_name male, test6_name female, single_test1_name female, single_test2_name male, single_test3_name male. NO double-gender writing: 1. Do NOT use parentheses or slashes to indicate gender alternatives (examples: '(a)', '(e)', '(la)', '(le)', '(а)', '(ла)', 'he/she', 'él/ella', 'il/elle', 'er/sie'). 2. Write each testimonial/comment in a single consistent gender form that matches the person’s gender.",
        ],
        "output_keys": [
            "hero_main_heading","hero_main_highlight","main_title","main_description",
            "test1_name","test2_name","test3_name","test4_name","test5_name","test6_name",
            "single_test1_name","single_test2_name","single_test3_name",
        ]
    }

    out = _llm_json(client, model, system, payload)

    # Ensure keys exist
    for k in payload["output_keys"]:
        if k not in out or not isinstance(out[k], str) or not out[k].strip():
            out[k] = ""
    return out

def generate_lang_files(
    template_bytes: bytes,
    geo_code: Optional[str],
    geo_currency: str,
    target_lang: str,
    domains: List[str],
    brand: str,
    template_kind: str = "template_1",
    model: str = DEFAULT_MODEL,
    country_name: Optional[str] = None,
    progress_cb: Optional[Callable[[float, str], None]] = None,
) -> List[Dict[str, str]]:
    """
    Повертає список: [{"domain": ..., "content": "..."}]
    template_kind: "template_1" або "template_2"
    """
    client = _get_openai_client()
    template = template_bytes.decode("utf-8", errors="replace")
    content = template
    if country_name:
        content = _set_php_var(content, "country_name", country_name, False)
    template_kind = (template_kind or "template_1").strip().lower()

    out_files: List[Dict[str, str]] = []
    total = max(1, len(domains))

    for idx, domain in enumerate(domains, start=1):
        cc = _infer_cc_from_target_lang(target_lang, geo_code)
        content = template

        # -------------------------
        # TEMPLATE 1 (existing flow)
        # -------------------------
        if template_kind == "template_1":
            if progress_cb:
                progress_cb((idx - 1) / total, f"Генерую спец-дані (адреса/персони/SEO) для {domain}…")

            # 1) базові спец-поля (кодом)
            rating_value = round(random.uniform(4.6, 5.0), 1)
            rating_count = random.randint(300, 3000)
            price = _make_price(geo_currency)

            # ВАЖЛИВО: site_name має бути "$source"
            content = _set_php_var(content, "site_name", "$source", numeric=False)

            content = _set_php_var(content, "site_url", f"https://{domain}", numeric=False)
            content = _set_php_var(content, "app_currency", geo_currency, numeric=False)
            content = _set_php_var(content, "app_price", str(price), numeric=True)
            content = _set_php_var(content, "rating_value", str(rating_value), numeric=True)
            content = _set_php_var(content, "rating_count", str(rating_count), numeric=True)
            content = _set_php_var(content, "site_lang", target_lang, numeric=False)
            content = _set_php_var(content, "site_gmail", _gmail_for_domain(domain), numeric=False)

            # 2) LLM спец-генерація (через $source)
            gen = _generate_specials_via_llm(
                client=client,
                model=model,
                domain=domain,
                cc=cc,
                target_lang=target_lang,
            )

            content = _set_php_var(content, "adress_name", gen["adress_name"], numeric=False)
            content = _set_php_var(content, "feedback_strong_1", gen["feedback_strong_1"], numeric=False)
            content = _set_php_var(content, "feedback_strong_2", gen["feedback_strong_2"], numeric=False)
            content = _set_php_var(content, "feedback_strong_3", gen["feedback_strong_3"], numeric=False)
            content = _set_php_var(content, "feedback_strong_4", gen["feedback_strong_4"], numeric=False)
            content = _set_php_var(content, "page_title_main", gen["page_title_main"], numeric=False)
            content = _set_php_var(content, "page_description_main", gen["page_description_main"], numeric=False)

            # 3) Переклад/унікалізація ТІЛЬКИ рядків у присвоєннях, без зміни PHP
            if progress_cb:
                progress_cb((idx - 1) / total + 0.65 / total, f"Один LLM-прохід по файлу для {domain}…")

            strings, spans = _extract_strings(content)
            if strings:
                outs = _llm_transform_strings_onepass(client, model, strings, target_lang, geo_code)
                content = _apply_strings(content, spans, outs)

        
        # -------------------------
        # TEMPLATE 3
        # -------------------------
        elif template_kind == "template_3":

            if progress_cb:
                progress_cb((idx - 1) / total, f"Генерую дані template_3 для {domain}…")
        
            rating_value = round(random.uniform(4.5,5.0),1)
            rating_count = random.randint(300,5000)
            price = _make_price(geo_currency)
        
            # MANUAL
            content = _set_php_var(content,"site_name","$source",numeric=False)
            content = _set_php_var(content,"site_url",f"https://{domain}",numeric=False)
            content = _set_php_var(content,"app_currency",geo_currency,numeric=False)
            content = _set_php_var(content,"app_price",str(price),numeric=True)
            content = _set_php_var(content,"rating_value",str(rating_value),numeric=True)
            content = _set_php_var(content,"rating_count",str(rating_count),numeric=True)
            content = _set_php_var(content,"site_lang",target_lang,numeric=False)
            content = _set_php_var(content,"site_gmail",_gmail_for_domain(domain),numeric=False)
            if country_name:
                content = _set_php_var(content, "country_name", country_name, False)
            
        
            # crypto image
            img = f"images/{CRYPTO_IMAGES.get(cc,'crypto_main.png')}"
            content = _set_php_var(content,"crypto_img",img,numeric=False)
        
            # SEO generation
            gen = _generate_specials_via_llm(
                client=client,
                model=model,
                domain=domain,
                cc=cc,
                target_lang=target_lang,
            )
        
            content = _set_php_var(content,"adress_name",gen["adress_name"],numeric=False)
            content = _set_php_var(content,"page_title_main",gen["page_title_main"],numeric=False)
            content = _set_php_var(content,"page_description_main",gen["page_description_main"],numeric=False)
        
            # names generation with gender control
            system = """
        Return JSON only:
        {"names":["name1","name2","name3","name4","name5","name6"]}

        Generate realistic FIRST NAMES used in the given country.

        Language of names should match the language:
        {language}

        Gender order MUST be:
        1 female
        2 female
        3 male
        4 female
        5 male
        6 male

        Return ONLY first names.
        """
        
            payload = {
                "country": cc,
                "language": target_lang
            }
            
        
            names = _llm_json(client,model,system,payload).get("names",[])
        
            while len(names)<6:
                names.append("Alex")
        
            content = _set_php_var(content,"feedback_strong_1",names[0],numeric=False)
            content = _set_php_var(content,"feedback_strong_2",names[1],numeric=False)
            content = _set_php_var(content,"feedback_strong_3",names[2],numeric=False)
            content = _set_php_var(content,"feedback_strong_4",names[3],numeric=False)
            content = _set_php_var(content,"feedback_strong_5",names[4],numeric=False)
            content = _set_php_var(content,"feedback_strong_6",names[5],numeric=False)
        
            strings,spans=_extract_strings(content)
        
            if strings:
                outs=_llm_transform_strings_onepass(client,model,strings,target_lang,geo_code)
                content=_apply_strings(content,spans,outs)


        # -------------------------
        # TEMPLATE 2 (fixed flow)
        # -------------------------
        elif template_kind == "template_2":
            if progress_cb:
                progress_cb((idx - 1) / total, f"Генерую MANUAL/імена/прибутки для {domain}…")

            # MANUAL scalars
            rating_value = round(random.uniform(4.5, 5.0), 1)
            rating_count = random.randint(350, 5000)
            price = _make_price(geo_currency)
            hero_amount = _hero_highlight_amount(geo_currency)  # для EUR має давати 950 (як у твоїй функції)

            # profits: integer (no cents), "not rounded" means not to 10/100/1000 steps — just int truncation
            def _p(mult: float) -> int:
                return max(1, int(price * mult * random.uniform(0.92, 1.08)))

            profit_amounts = {
                "test1_profit": _p(25),
                "test2_profit": _p(45),
                "test3_profit": _p(110),
                "test4_profit": _p(35),
                "test5_profit": _p(50),
                "test6_profit": _p(135),
            }

            def _fmt_money(amount: int, currency_code: str) -> str:
                # thousands separated by comma, no decimals
                return f"{amount:,} {currency_code}".strip()

            # Ask LLM ONLY for: currency word (localized), names with required gender, headings/title/description
            gen2 = _generate_template2_manual_via_llm(
                client=client,
                model=model,
                cc=cc,
                target_lang=target_lang,
                currency=geo_currency,          # код валюти як контекст
                app_price=price,
                hero_amount=hero_amount,
                brand=brand,
                profit_amounts=profit_amounts,  # як контекст (але форматувати будемо кодом)
            )

            currency_code = geo_currency.strip().upper()

            # 1) Спочатку переклад/унікалізація всіх "звичайних" рядків (потім заоверрайдимо MANUAL)
            if progress_cb:
                progress_cb((idx - 1) / total + 0.55 / total, f"Переклад/унікалізація текстів для {domain}…")

            strings, spans = _extract_strings(content)
            if strings:
                outs = _llm_transform_strings_onepass(client, model, strings, target_lang, geo_code)
                content = _apply_strings(content, spans, outs)

            # 2) Тепер override MANUAL змінних — гарантуємо структуру/плейсхолдери
            content = _set_php_var(content, "site_name", brand, numeric=False)
            content = _set_php_var(content, "site_url", f"https://{domain}", numeric=False)
            content = _set_php_var(content, "rating_value", str(rating_value), numeric=True)
            content = _set_php_var(content, "rating_count", str(rating_count), numeric=True)
            content = _set_php_var(content, "app_price", str(price), numeric=True)
            content = _set_php_var(content, "app_currency", currency_code, numeric=False)
            content = _set_php_var(content, "site_lang", target_lang, numeric=False)

            # Optional small override for UA "Like"
            if target_lang.lower().startswith("uk"):
                content = _set_php_var(content, "single_test1_i", "Подобається", numeric=False)

            # 3) LLM-generated MANUAL texts (names + headings/title/description)
            for k in (
                "hero_main_heading",
                "hero_main_highlight",
                "main_title",
                "main_description",
                "test1_name",
                "test2_name",
                "test3_name",
                "test4_name",
                "test5_name",
                "test6_name",
                "single_test1_name",
                "single_test2_name",
                "single_test3_name",
            ):
                v = (gen2.get(k) or "").strip()
                if v:
                    content = _set_php_var(content, k, v, numeric=False)

            # 4) profits MUST be formatted by code (no cents, comma thousands, localized currency word)
            content = _set_php_var(content, "test1_profit", _fmt_money(profit_amounts["test1_profit"], currency_code), numeric=False)
            content = _set_php_var(content, "test2_profit", _fmt_money(profit_amounts["test2_profit"], currency_code), numeric=False)
            content = _set_php_var(content, "test3_profit", _fmt_money(profit_amounts["test3_profit"], currency_code), numeric=False)
            content = _set_php_var(content, "test4_profit", _fmt_money(profit_amounts["test4_profit"], currency_code), numeric=False)
            content = _set_php_var(content, "test5_profit", _fmt_money(profit_amounts["test5_profit"], currency_code), numeric=False)
            content = _set_php_var(content, "test6_profit", _fmt_money(profit_amounts["test6_profit"], currency_code), numeric=False)

        else:
            raise ValueError(f"Unknown template_kind: {template_kind}")

        if progress_cb:
            progress_cb(idx / total, f"Готово: {domain}")

        out_files.append({"domain": domain, "content": content})

    return out_files


def generate_lang_files_multi(
    template1_bytes: bytes,
    template2_bytes: bytes,
    template3_bytes: bytes,
    geo_code: Optional[str],
    geo_currency: str,
    target_lang: str,
    domains: List[str],
    domain_templates: Dict[str, str],
    brand: str,
    model: str = DEFAULT_MODEL,
    geo_defaults: Optional[Dict] = None,
    progress_cb: Optional[Callable[[float, str], None]] = None,
) -> List[Dict[str, str]]:
    """
    Generate lang.php for multiple templates.
    domain_templates maps domain -> template id
    """

    out: List[Dict[str, str]] = []

    # ---- визначаємо назву країни ----
    country_name = geo_code or ""
    if geo_defaults and geo_code and geo_code in geo_defaults:
        country_name = geo_defaults[geo_code].get("name", geo_code)

    # ---- генерація для кожного домену ----
    for d in domains:

        kind = (domain_templates or {}).get(d, "template_1")

        if kind in ("template_3", "t3", "3", "template3"):
            tpl = template3_bytes
            tk = "template_3"

        elif kind in ("template_2", "t2", "2", "template2"):
            tpl = template2_bytes
            tk = "template_2"

        else:
            tpl = template1_bytes
            tk = "template_1"

        try:
            files = generate_lang_files(
                template_bytes=tpl,
                geo_code=geo_code,
                geo_currency=geo_currency,
                target_lang=target_lang,
                domains=[d],
                brand=brand,
                template_kind=tk,
                model=model,
                country_name=country_name,
                progress_cb=progress_cb,
            )

            if files:
                out.append(files[0])
        except Exception as e:
            print(f"[ERROR] {d}: {e}")
        time.sleep(1.2)  # 🔥 КРИТИЧНО

    return out
