from __future__ import annotations

import json
import re
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from urllib.parse import quote_plus

import requests
from bs4 import BeautifulSoup


# -----------------------------
# Model
# -----------------------------
@dataclass
class ProbeResult:
    source: str               # "ddg" | "domain"
    input: str                # url tried
    final_url: str            # after redirects
    ok: bool
    status_code: Optional[int]
    error: str                # "" if ok else reason
    lang: Optional[str]       # base lang, e.g. "es"
    geo: Optional[str]        # country code, e.g. "ES"
    signals: List[str]        # signals used (debug)


# -----------------------------
# Normalizers
# -----------------------------
def _norm_lang(lang: str) -> Optional[str]:
    if not lang:
        return None
    lang = lang.strip().replace("_", "-")
    base = lang.split("-")[0].lower()
    if 2 <= len(base) <= 3 and base.isalpha():
        return base
    return None


def _looks_like_country(cc: str) -> bool:
    return isinstance(cc, str) and len(cc) == 2 and cc.isalpha() and cc.upper() == cc


# -----------------------------
# Script extraction (your patterns)
# -----------------------------
def _extract_country_from_scripts(js: str) -> Optional[str]:
    """
    Handles:
      window.userCountry = 'ES';
      userCountry = 'ES';
      COUNTRY = 'AU';
      window.countryCode = 'DE';
      geo = 'IT';
    """
    patterns = [
        r"(?:\bCOUNTRY\b|\bcountry\b)\s*[:=]\s*['\"]([A-Z]{2})['\"]",
        r"(?:\buserCountry\b|\bwindow\.userCountry\b)\s*[:=]\s*['\"]([A-Z]{2})['\"]",
        r"(?:\bcountryCode\b|\bwindow\.countryCode\b)\s*[:=]\s*['\"]([A-Z]{2})['\"]",
        r"(?:\bgeo\b|\bwindow\.geo\b)\s*[:=]\s*['\"]([A-Z]{2})['\"]",
    ]
    for pat in patterns:
        m = re.search(pat, js)
        if m:
            cc = m.group(1)
            if _looks_like_country(cc):
                return cc
    return None


def _extract_lang_from_scripts(js: str) -> Optional[str]:
    """
    Handles:
      window.defaultLang = 'es';
      window.currentLang = 'es';
      DEFAULT_LANG = 'en';
      window.languageList = ["es","en"];
    """
    # single var
    m = re.search(
        r"(?:DEFAULT_LANG|default_lang|defaultLang|currentLang|window\.defaultLang|window\.currentLang)\s*[:=]\s*['\"]([a-z]{2,3})['\"]",
        js,
        re.I,
    )
    if m:
        return _norm_lang(m.group(1))

    # list var
    m2 = re.search(
        r"(?:LANGUAGE_LIST|language_list|languageList|window\.languageList)\s*[:=]\s*(\[[^\]]+\])",
        js,
        re.I,
    )
    if m2:
        arr = m2.group(1)
        m3 = re.search(r"['\"]([a-z]{2,3})['\"]", arr, re.I)
        if m3:
            return _norm_lang(m3.group(1))

    return None


# -----------------------------
# HTML extraction
# -----------------------------
def _extract_from_html(html: str) -> Tuple[Optional[str], Optional[str], List[str]]:
    soup = BeautifulSoup(html, "html.parser")

    signals: List[str] = []
    lang: Optional[str] = None
    geo: Optional[str] = None

    # html lang
    html_tag = soup.find("html")
    if html_tag and html_tag.get("lang"):
        raw = (html_tag.get("lang") or "").strip()
        l = _norm_lang(raw)
        if l:
            lang = lang or l
            signals.append(f"sig:html_lang={raw}")

    # og:locale
    og = soup.find("meta", attrs={"property": "og:locale"})
    if og and og.get("content"):
        raw = (og.get("content") or "").strip()
        parts = raw.replace("-", "_").split("_")
        if len(parts) >= 1:
            l = _norm_lang(parts[0])
            if l:
                lang = lang or l
                signals.append(f"sig:og_locale={raw}")
        if len(parts) >= 2:
            cc = parts[1].upper()
            if _looks_like_country(cc):
                geo = geo or cc
                signals.append(f"sig:og_locale_country={cc}")

    # hreflang
    for tag in soup.find_all("link", attrs={"rel": "alternate", "hreflang": True})[:20]:
        hl = (tag.get("hreflang") or "").strip()
        if not hl or hl.lower() == "x-default":
            continue
        base = _norm_lang(hl)
        if base:
            lang = lang or base
            signals.append(f"sig:hreflang={hl}")
        if "-" in hl:
            cc = hl.split("-")[-1].upper()
            if _looks_like_country(cc):
                geo = geo or cc
                signals.append(f"sig:hreflang_country={cc}")

    # JSON-LD addressCountry
    for sc in soup.find_all("script", attrs={"type": "application/ld+json"})[:30]:
        txt = (sc.get_text() or "").strip()
        if not txt:
            continue
        try:
            data = json.loads(txt)
        except Exception:
            continue

        def walk(obj):
            nonlocal geo
            if isinstance(obj, dict):
                if "addressCountry" in obj:
                    ac = obj["addressCountry"]
                    if isinstance(ac, str):
                        cc = ac.strip().upper()
                        if _looks_like_country(cc):
                            geo = geo or cc
                            signals.append(f"sig:jsonld_addressCountry={cc}")
                    elif isinstance(ac, dict):
                        nm = ac.get("name")
                        if isinstance(nm, str):
                            cc = nm.strip().upper()
                            if _looks_like_country(cc):
                                geo = geo or cc
                                signals.append(f"sig:jsonld_addressCountry_name={cc}")
                for v in obj.values():
                    walk(v)
            elif isinstance(obj, list):
                for v in obj:
                    walk(v)

        walk(data)

    # custom JS patterns (your strongest)
    scripts_text = "\n".join((s.get_text("\n", strip=True) or "") for s in soup.find_all("script"))
    if scripts_text:
        cc = _extract_country_from_scripts(scripts_text)
        if cc:
            geo = geo or cc
            signals.append(f"sig:script_country={cc}")

        l2 = _extract_lang_from_scripts(scripts_text)
        if l2:
            lang = lang or l2
            signals.append(f"sig:script_lang={l2}")

    return lang, geo, signals


# -----------------------------
# Fetch
# -----------------------------
def _fetch(url: str, timeout: float = 10.0) -> Tuple[bool, str, Optional[int], str]:
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9,uk;q=0.8",
    }
    try:
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        status = r.status_code
        text = r.text or ""
        low = text.lower()

        # anti-bot / cloudflare-ish
        if status in (403, 429) or "cloudflare" in low or "attention required" in low:
            return False, r.url, status, "Ймовірно захист (Cloudflare/anti-bot)"
        if status >= 400:
            return False, r.url, status, f"HTTP {status}"

        return True, r.url, status, text

    except requests.RequestException as e:
        return False, url, None, str(e)


# -----------------------------
# Search (no API keys)
# -----------------------------
def _ddg_search(brand: str, limit: int = 10) -> List[str]:
    q = quote_plus(f"\"{brand}\"")
    url = f"https://duckduckgo.com/html/?q={q}"
    ok, final_url, status, body = _fetch(url, timeout=12.0)
    if not ok:
        return []
    soup = BeautifulSoup(body, "html.parser")
    links: List[str] = []
    for a in soup.select("a.result__a")[:limit]:
        href = a.get("href")
        if href and href.startswith("http"):
            links.append(href)
    # de-dup
    out: List[str] = []
    seen = set()
    for u in links:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out[:limit]


# -----------------------------
# Voting logic (important part)
# -----------------------------
def _geo_weight(geo_cc: str, signals: List[str]) -> int:
    """
    Weights:
      script_country -> 8 (strongest)
      jsonld_addressCountry -> 7
      hreflang_country -> 6
      og_locale_country -> 1 (often template)
    Plus anti-pattern:
      US coming ONLY from og:locale=en_US -> weight 0 (ignore)
    """
    sig = " | ".join(signals or [])

    if "sig:script_country=" in sig:
        w = 8
    elif "sig:jsonld_addressCountry=" in sig or "sig:jsonld_addressCountry_name=" in sig:
        w = 7
    elif "sig:hreflang_country=" in sig:
        w = 6
    elif "sig:og_locale_country=" in sig:
        w = 1
    else:
        w = 2

    # Anti-template US: ignore if ONLY og:locale_country=US
    if geo_cc == "US":
        has_og_us = "sig:og_locale_country=US" in sig
        has_strong = ("sig:script_country=" in sig) or ("sig:jsonld_addressCountry" in sig) or ("sig:hreflang_country=" in sig)
        if has_og_us and not has_strong:
            return 0

    return w


def _lang_weight(lang_base: str, signals: List[str]) -> int:
    sig = " | ".join(signals or [])
    if "sig:script_lang=" in sig:
        return 4
    if "sig:hreflang=" in sig:
        return 3
    if "sig:html_lang=" in sig:
        return 2
    if "sig:og_locale=" in sig:
        return 1
    return 1


def infer_geo_from_lang(lang_base: str, geo_defaults: dict, preferred_geo_order: List[str]) -> Optional[str]:
    if not lang_base:
        return None
    candidates = []
    for cc, meta in geo_defaults.items():
        base = (meta.get("lang") or "").split("-")[0].lower()
        if base == lang_base.lower():
            candidates.append(cc)

    if not candidates:
        return None

    # prefer your TOP order if possible
    for cc in preferred_geo_order:
        if cc in candidates:
            return cc
    return candidates[0]


# -----------------------------
# Public API
# -----------------------------
def detect_geo_lang(
    brand: str,
    geo_defaults: dict,
    preferred_geo_order: List[str],
    domain_candidates: List[str],
    search_limit: int = 10,
    probe_limit: int = 12,
) -> Tuple[Optional[str], Optional[str], str, List[ProbeResult]]:
    """
    Returns:
      geo_code (e.g. "HU")
      lang_base (e.g. "hu")
      verdict: "exact" | "lang_only" | "none"
      details: list[ProbeResult]
    """
    brand = (brand or "").strip()
    if not brand:
        return None, None, "none", []

    to_probe: List[Tuple[str, str]] = []

    # 1) Search mention pages
    for u in _ddg_search(brand, limit=search_limit):
        to_probe.append(("ddg", u))

    # 2) Default domains for the brand (your flow)
    for d in domain_candidates[:probe_limit]:
        if d.startswith("http://") or d.startswith("https://"):
            to_probe.append(("domain", d))
        else:
            to_probe.append(("domain", f"https://{d}"))

    results: List[ProbeResult] = []
    geo_votes: Dict[str, int] = {}
    lang_votes: Dict[str, int] = {}

    for source, url in to_probe[: (search_limit + probe_limit)]:
        ok, final_url, status, body_or_err = _fetch(url)
        if not ok:
            results.append(ProbeResult(
                source=source,
                input=url,
                final_url=final_url,
                ok=False,
                status_code=status,
                error=body_or_err,
                lang=None,
                geo=None,
                signals=[],
            ))
            continue

        lang, geo_cc, signals = _extract_from_html(body_or_err)

        if lang:
            lang_votes[lang] = lang_votes.get(lang, 0) + _lang_weight(lang, signals)

        if geo_cc:
            w = _geo_weight(geo_cc, signals)
            if w > 0:
                geo_votes[geo_cc] = geo_votes.get(geo_cc, 0) + w

        results.append(ProbeResult(
            source=source,
            input=url,
            final_url=final_url,
            ok=True,
            status_code=status,
            error="",
            lang=lang,
            geo=geo_cc,
            signals=signals,
        ))

        time.sleep(0.12)

    lang_best = None
    if lang_votes:
        lang_best = sorted(lang_votes.items(), key=lambda x: x[1], reverse=True)[0][0]

    geo_best = None
    if geo_votes:
        geo_best = sorted(geo_votes.items(), key=lambda x: x[1], reverse=True)[0][0]

    # Verdict:
    # - If we found a real geo (and not ignored), it's exact (even if lang missing)
    if geo_best:
        return geo_best, lang_best, "exact", results

    # - If only lang -> guess geo (approx)
    if lang_best:
        guess_geo = infer_geo_from_lang(lang_best, geo_defaults, preferred_geo_order)
        return guess_geo, lang_best, "lang_only", results

    return None, None, "none", results
