from __future__ import annotations

from typing import List, Dict
from functools import lru_cache
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed


BOOTSTRAP_URL = "https://data.iana.org/rdap/dns.json"

HARDCODED_RDAP = {
    "com": ["https://rdap.verisign.com/com/v1/domain/"],
    "net": ["https://rdap.verisign.com/net/v1/domain/"],
    "org": ["https://rdap.publicinterestregistry.org/rdap/domain/"],
    "info": ["https://rdap.afilias.net/rdap/domain/"],
    "biz": ["https://rdap.nic.biz/domain/"],
}


def _tld(domain: str) -> str:
    parts = domain.lower().strip(".").split(".")
    return parts[-1] if len(parts) >= 2 else ""


@lru_cache(maxsize=1)
def _bootstrap_map() -> Dict[str, List[str]]:
    headers = {"User-Agent": "Mozilla/5.0"}
    r = requests.get(BOOTSTRAP_URL, headers=headers, timeout=10)
    r.raise_for_status()
    data = r.json()

    mapping: Dict[str, List[str]] = {}
    for item in data.get("services", []):
        if not isinstance(item, list) or len(item) != 2:
            continue
        tlds, urls = item
        for t in tlds:
            mapping[t.lower()] = urls

    return mapping


def _rdap_bases_for(domain: str) -> List[str]:
    t = _tld(domain)
    bases: List[str] = []

    # 1. HARDCODED (швидше)
    if t in HARDCODED_RDAP:
        bases.extend(HARDCODED_RDAP[t])

    # 2. IANA bootstrap
    try:
        bm = _bootstrap_map()
        if t in bm:
            for u in bm[t]:
                if u not in bases:
                    bases.append(u)
    except Exception:
        pass

    # 3. fallback
    if "https://rdap.org/domain/" not in bases:
        bases.append("https://rdap.org/domain/")

    return bases


def _probe_one(base: str, domain: str, timeout: float) -> Dict:
    headers = {"User-Agent": "Mozilla/5.0"}
    url = base.rstrip("/") + "/" + domain

    try:
        r = requests.get(url, headers=headers, timeout=timeout)

        if r.status_code == 200:
            return {"status": "taken", "reason": f"RDAP 200 ({base})"}

        if r.status_code == 404:
            return {"status": "free", "reason": f"RDAP 404 ({base})"}

        return {"status": "unknown", "reason": f"HTTP {r.status_code}"}

    except Exception:
        return {"status": "unknown", "reason": "error"}


def _check_one_domain(domain: str, timeout: float) -> Dict:
    bases = _rdap_bases_for(domain)

    for base in bases:
        res = _probe_one(base, domain, timeout)

        if res["status"] in ("free", "taken"):
            return {
                "domain": domain,
                "status": res["status"],
                "reason": res["reason"],
            }

    return {
        "domain": domain,
        "status": "unknown",
        "reason": "no result",
    }


def check_domains_rdap(
    domains: List[str],
    timeout: float = 6.0,
    max_workers: int = 10,
    stop_after_free: int = 5,
    priority_count: int = 10,  # 🔥 нове
) -> List[Dict]:
    """
    🔥 ШВИДКА перевірка доменів

    ✔ паралельна
    ✔ гарантує перевірку топ-доменів (priority)
    ✔ early stop тільки для другорядних

    Args:
        domains: список доменів
        timeout: timeout HTTP
        max_workers: кількість потоків
        stop_after_free: зупинка після N вільних
        priority_count: скільки перших доменів перевірити ОБОВʼЯЗКОВО
    """

    results: List[Dict] = []
    free_count = 0

    clean_domains = [
        d.strip().lower()
        for d in domains
        if d and "." in d
    ]

    if not clean_domains:
        return results

    # 🔥 Розбиваємо
    priority = clean_domains[:priority_count]
    rest = clean_domains[priority_count:]

    # =========================
    # 🔴 PHASE 1: PRIORITY
    # =========================
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(_check_one_domain, d, timeout)
            for d in priority
        ]

        for future in as_completed(futures):
            res = future.result()
            results.append(res)

            if res["status"] == "free":
                free_count += 1

    # =========================
    # 🔴 PHASE 2: REST + EARLY STOP
    # =========================
    if rest:
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(_check_one_domain, d, timeout): d
                for d in rest
            }

            for future in as_completed(futures):
                res = future.result()
                results.append(res)

                if res["status"] == "free":
                    free_count += 1

                if free_count >= stop_after_free:
                    break

    return results
