from __future__ import annotations

from typing import List, Dict, Optional
from functools import lru_cache
import requests


BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"

# Fallback endpoints for most common TLDs (навіть якщо bootstrap тимчасово недоступний)
HARDCODED_RDAP = {
    "com": ["https://rdap.verisign.com/com/v1/domain/"],
    "net": ["https://rdap.verisign.com/net/v1/domain/"],
    "org": ["https://rdap.publicinterestregistry.org/rdap/domain/"],
    "info": ["https://rdap.afilias.net/rdap/domain/"],
    "biz": ["https://rdap.nic.biz/domain/"],  # інколи працює, інколи ні — тому буде bootstrap+fallback
}


def _tld(domain: str) -> str:
    parts = domain.lower().strip(".").split(".")
    return parts[-1] if len(parts) >= 2 else ""


@lru_cache(maxsize=1)
def _bootstrap_map() -> Dict[str, List[str]]:
    """
    Returns mapping: tld -> [rdap_base_url1, rdap_base_url2, ...]
    From IANA bootstrap.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(BOOTSTRAP_URL, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    mapping: Dict[str, List[str]] = {}
    services = data.get("services", [])
    # services: [ [ ["com","net"], ["https://rdap.verisign.com/com/v1/"] ], ... ]
    for item in services:
        if not isinstance(item, list) or len(item) != 2:
            continue
        tlds, urls = item
        if not isinstance(tlds, list) or not isinstance(urls, list):
            continue
        for t in tlds:
            if isinstance(t, str):
                mapping[t.lower()] = [u for u in urls if isinstance(u, str)]
    return mapping


def _rdap_bases_for(domain: str) -> List[str]:
    t = _tld(domain)
    bases: List[str] = []

    # 1) hardcoded first (fast & stable for common TLDs)
    if t in HARDCODED_RDAP:
        bases.extend(HARDCODED_RDAP[t])

    # 2) IANA bootstrap
    try:
        bm = _bootstrap_map()
        if t in bm:
            for u in bm[t]:
                if u not in bases:
                    bases.append(u)
    except Exception:
        # bootstrap temporarily unavailable
        pass

    # 3) last resort: rdap.org
    if "https://rdap.org/domain/" not in bases:
        bases.append("https://rdap.org/domain/")

    return bases


def _probe_one(base: str, domain: str, timeout: float) -> Dict:
    """
    Probe a single RDAP base. Returns dict with status.
    """
    headers = {"User-Agent": "Mozilla/5.0"}
    url = base.rstrip("/") + "/" + domain

    try:
        r = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)

        # RDAP common behavior:
        # 200 => exists (taken)
        # 404 => not found (usually free)
        if r.status_code == 200:
            return {"status": "taken", "reason": f"RDAP 200 ({base})", "rdap_url": url}
        if r.status_code == 404:
            return {"status": "free", "reason": f"RDAP 404 ({base})", "rdap_url": url}

        # Some servers use 400 for not found (rare), keep unknown but show
        if r.status_code in (400, 401, 403, 405, 409, 429, 500, 502, 503, 504, 525):
            return {"status": "unknown", "reason": f"RDAP HTTP {r.status_code} ({base})", "rdap_url": url}

        return {"status": "unknown", "reason": f"RDAP HTTP {r.status_code} ({base})", "rdap_url": url}

    except requests.exceptions.SSLError:
        return {"status": "unknown", "reason": f"RDAP SSL error ({base})", "rdap_url": url}
    except requests.exceptions.ConnectionError:
        return {"status": "unknown", "reason": f"RDAP connection error ({base})", "rdap_url": url}
    except requests.exceptions.Timeout:
        return {"status": "unknown", "reason": f"RDAP timeout ({base})", "rdap_url": url}
    except Exception as e:
        return {"status": "unknown", "reason": f"RDAP error: {e} ({base})", "rdap_url": url}


def check_domains_rdap(domains: List[str], timeout: float = 8.0) -> List[Dict]:
    """
    status:
      - free: RDAP 404 (на якомусь сервері)
      - taken: RDAP 200
      - unknown: якщо всі джерела дали помилку/блок/timeout
    """
    out: List[Dict] = []

    for d in domains:
        domain = d.strip().lower()
        if not domain or "." not in domain:
            continue

        bases = _rdap_bases_for(domain)

        best: Optional[Dict] = None
        # Strategy: first definitive wins (taken/free). Otherwise keep last unknown reason.
        for base in bases:
            res = _probe_one(base, domain, timeout=timeout)

            if res["status"] in ("taken", "free"):
                best = res
                break
            best = res  # keep last unknown

        if best is None:
            best = {"status": "unknown", "reason": "RDAP: no result", "rdap_url": ""}

        out.append({
            "domain": domain,
            "status": best["status"],
            "reason": best["reason"],
            "rdap_url": best.get("rdap_url", "")
        })

    return out
