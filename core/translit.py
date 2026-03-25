from __future__ import annotations
import re
import unicodedata

# --- ДОДАНО: кастомна нормалізація (ВАЖЛИВО) ---
CUSTOM_MAP = {
    "ł": "l", "Ł": "l",
    "ß": "ss",
    "ø": "o", "Ø": "o",
    "đ": "d", "Đ": "d",
    "ı": "i", "İ": "i",
    "ş": "s", "Ş": "s",
    "ğ": "g", "Ğ": "g",
    "ç": "c", "Ç": "c",
}

# Мінімальні транслітерації (достатньо для доменів)
UA_RU = {
    "а":"a","б":"b","в":"v","г":"h","ґ":"g","д":"d","е":"e","є":"ye","ж":"zh","з":"z","и":"y","і":"i","ї":"yi","й":"y",
    "к":"k","л":"l","м":"m","н":"n","о":"o","п":"p","р":"r","с":"s","т":"t","у":"u","ф":"f","х":"kh","ц":"ts",
    "ч":"ch","ш":"sh","щ":"shch","ю":"yu","я":"ya","ь":"","ъ":"","э":"e","ы":"y","ё":"yo"
}

GR = {
    "α":"a","β":"v","γ":"g","δ":"d","ε":"e","ζ":"z","η":"i","θ":"th","ι":"i","κ":"k","λ":"l","μ":"m","ν":"n",
    "ξ":"x","ο":"o","π":"p","ρ":"r","σ":"s","ς":"s","τ":"t","υ":"y","φ":"f","χ":"ch","ψ":"ps","ω":"o"
}


# --- ДОДАНО: нормалізація бренду ---
def normalize_brand(s: str) -> str:
    if not s:
        return ""

    # 1. кастомні символи (польська, турецька і т.д.)
    for k, v in CUSTOM_MAP.items():
        s = s.replace(k, v)

    # 2. прибираємо акценти (é → e, á → a)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))

    return s


def slugify_brand(s: str) -> str:
    if not s:
        return ""

    s = s.strip()

    # 🔥 ГОЛОВНИЙ ФІКС
    s = normalize_brand(s)

    s = s.lower()

    out = []
    for ch in s:
        if "a" <= ch <= "z" or "0" <= ch <= "9" or ch == "-":
            out.append(ch)
        elif ch in UA_RU:
            out.append(UA_RU[ch])
        elif ch in GR:
            out.append(GR[ch])
        elif ch.isspace() or ch in "_.":
            out.append("-")
        else:
            # інше — пропускаємо
            continue

    res = "".join(out)

    # прибрати подвійні дефіси
    res = re.sub(r"-{2,}", "-", res).strip("-")

    # максимум 63 символи
    return res[:63]
