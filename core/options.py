from __future__ import annotations
from typing import Dict, List, Tuple

# Топ-країни (показувати першими) — як ти просив
TOP_GEO_ORDER = [
    # --- Core Europe ---
    "ES","IT","PL","CZ","SK","HU","TR","DE","RO","PT","BE","NL","FR",
    "HR","SI","RS","BG","GR",
    "SE","FI","DK","NO","IS",
    "EE","LV","LT",
    "CH","AT",

    # --- UK / Anglosphere ---
    "GB","IE","AU","NZ","CA","US",

    # --- Asia ---
    "JP","KR","TH","VN","ID","MY","HK","SG",

    # --- Middle East ---
    "IL","AE","SA",

    # --- Americas ---
    "CR","MX","BR","AR","CL",

    # --- Africa ---
    "ZA","NG","KE",
]

# Мови (популярні зверху) — можна шукати UA/EN/кодом
LANGS = [
    # --- Global ---
    ("en", "Англійська", "English"),
    ("zh", "Китайська", "Chinese"),
    ("ja", "Японська", "Japanese"),
    ("ko", "Корейська", "Korean"),
    ("ar", "Арабська", "Arabic"),
    ("hi", "Гінді", "Hindi"),

    # --- Europe (Core) ---
    ("de", "Німецька", "German"),
    ("fr", "Французька", "French"),
    ("es", "Іспанська", "Spanish"),
    ("it", "Італійська", "Italian"),
    ("pt", "Португальська", "Portuguese"),
    ("nl", "Нідерландська", "Dutch"),
    ("pl", "Польська", "Polish"),
    ("cs", "Чеська", "Czech"),
    ("sk", "Словацька", "Slovak"),
    ("hu", "Угорська", "Hungarian"),
    ("ro", "Румунська", "Romanian"),
    ("bg", "Болгарська", "Bulgarian"),
    ("hr", "Хорватська", "Croatian"),
    ("sr", "Сербська", "Serbian"),
    ("sl", "Словенська", "Slovenian"),
    ("et", "Естонська", "Estonian"),
    ("lv", "Латвійська", "Latvian"),
    ("lt", "Литовська", "Lithuanian"),
    ("el", "Грецька", "Greek"),
    ("tr", "Турецька", "Turkish"),

    # --- Scandinavia ---
    ("sv", "Шведська", "Swedish"),
    ("fi", "Фінська", "Finnish"),
    ("da", "Данська", "Danish"),
    ("nb", "Норвезька", "Norwegian Bokmål"),
    ("nn", "Норвезька (нюношк)", "Norwegian Nynorsk"),
    ("is", "Ісландська", "Icelandic"),

    # --- CIS / Eastern ---
    ("uk", "Українська", "Ukrainian"),
    ("ru", "Російська", "Russian"),

    # --- Asia ---
    ("th", "Тайська", "Thai"),
    ("vi", "Вʼєтнамська", "Vietnamese"),
    ("id", "Індонезійська", "Indonesian"),
    ("ms", "Малайська", "Malay"),

    # --- Middle East ---
    ("he", "Іврит", "Hebrew"),
    ("fa", "Перська", "Persian"),

    # --- Africa ---
    ("sw", "Суахілі", "Swahili"),
    ("af", "Африкаанс", "Afrikaans"),
]

def flag_emoji(cc: str) -> str:
    """
    'PL' -> 🇵🇱
    """
    cc = (cc or "").upper()
    if len(cc) != 2 or not cc.isalpha():
        return "🏳️"
    return chr(0x1F1E6 + ord(cc[0]) - ord("A")) + chr(0x1F1E6 + ord(cc[1]) - ord("A"))

def build_geo_labels(geo_defaults: dict) -> Tuple[List[str], Dict[str, str]]:
    """
    label: "🇵🇱 Польща / Poland (PL)"
    Пошук працює за UA/EN/кодом, бо все є в одному рядку.
    """
    code_to_label: Dict[str, str] = {}

    for code, meta in geo_defaults.items():
        ua = meta.get("ua_name") or meta.get("name") or code
        en = meta.get("name") or ua or code
        code_to_label[code] = f"{flag_emoji(code)} {ua} / {en} ({code})"

    top = [c for c in TOP_GEO_ORDER if c in code_to_label]
    rest = [c for c in sorted(code_to_label.keys()) if c not in top]
    labels = [code_to_label[c] for c in top] + [code_to_label[c] for c in rest]

    label_to_code = {label: code for code, label in code_to_label.items()}
    return labels, label_to_code

def build_language_labels() -> Tuple[List[str], Dict[str, str]]:
    """
    label: "Англійська / English (en)"
    value: "en"
    """
    labels: List[str] = []
    label_to_code: Dict[str, str] = {}
    for code, ua, en in LANGS:
        label = f"{ua} / {en} ({code})"
        labels.append(label)
        label_to_code[label] = code
    return labels, label_to_code

def bcp47_from(lang_base: str, geo_code: str, use_region: bool) -> str:
    """
    en + PL + use_region=True => en-PL
    en + UNKNOWN => en
    """
    lang_base = (lang_base or "").strip().lower()
    if not lang_base:
        return "unknown"
    if not use_region or geo_code == "UNKNOWN":
        return lang_base
    return f"{lang_base}-{geo_code}"
