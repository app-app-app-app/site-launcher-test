from __future__ import annotations
import re
import unicodedata

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

def _strip_accents(s: str) -> str:
    nfkd = unicodedata.normalize("NFKD", s)
    return "".join([c for c in nfkd if not unicodedata.combining(c)])

def slugify_brand(s: str) -> str:
    if not s:
        return ""

    s = s.strip()
    s = _strip_accents(s)
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
            out.append("")

    res = "".join(out)
    res = re.sub(r"-{2,}", "-", res).strip("-")
    # доменне правило: максимум 63 символи на label
    return res[:63]
