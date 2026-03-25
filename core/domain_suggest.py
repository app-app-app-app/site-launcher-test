from __future__ import annotations
from typing import List, Optional, Tuple
import re

from core.translit import slugify_brand


def _split_brand_words(brand: str) -> List[str]:
    brand = (brand or "").strip()
    if not brand:
        return []

    # якщо CapvexOne => Capvex + One
    parts = re.findall(r"[A-Z]?[a-z]+|[A-Z]+(?![a-z])|\d+", brand)
    if len(parts) >= 2 and "".join(parts).lower() == brand.lower():
        return [p.lower() for p in parts]

    # якщо є пробіли/дефіси
    brand2 = re.sub(r"[\s_]+", " ", brand)
    raw = re.split(r"[\s\-]+", brand2)
    raw = [r for r in raw if r]
    if len(raw) >= 2:
        return [r.lower() for r in raw]

    return [brand.lower()]


def _forms(words: List[str]) -> Tuple[str, str]:
    if not words:
        return "", ""
    if len(words) == 1:
        w = words[0]
        return w, w
    return "".join(words), "-".join(words)


def generate_domain_candidates(brand: str, ccTLD: Optional[str]) -> List[str]:
    """
    Патерни як ти казав:
    1 слово:
      brand.com, brand.net, brand.org, brand.<ccTLD>, brand-<ccTLD>.com
    2 слова:
      concat/hyphen + ті самі
    + додаткові варіанти з translit/slugify якщо бренд не латинкою
    """
    words = _split_brand_words(brand)
    base_raw_concat, base_raw_hyph = _forms(words)

    base_concat = slugify_brand(base_raw_concat)
    base_hyph = slugify_brand(base_raw_hyph)

    # якщо вийшло пусто — fallback
    if not base_concat:
        base_concat = "brand"
    if not base_hyph:
        base_hyph = base_concat

    tlds = ["com", "net", "org", "io", "pro"]
    out = []

    def add(s: str):
        if s and s not in out:
            out.append(s)

    for b in [base_concat, base_hyph]:
        for t in tlds:
            add(f"{b}.{t}")

    # --- official варіанти ---
    for b in [base_concat, base_hyph]:
        add(f"{b}-official.com")

    if ccTLD:
        add(f"{base_concat}.{ccTLD}")
        add(f"{base_hyph}.{ccTLD}")
        # geo in sld
        add(f"{base_concat}-{ccTLD}.com")
        add(f"{base_hyph}-{ccTLD}.com")

    # трішки бонусних загальних
    for t in ["info", "site", "app"]:
        add(f"{base_concat}.{t}")

    return out
