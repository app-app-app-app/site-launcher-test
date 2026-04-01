from core.domain_suggest import generate_domain_candidates
from core.domain_check import check_domains_rdap

def get_domain_candidates(brand: str, geo_code: str, geo_data: dict):
ccTLD = None

```
if geo_code and geo_code != "UNKNOWN" and geo_code in geo_data:
    ccTLD = geo_data[geo_code].get("ccTLD")

return generate_domain_candidates(brand, ccTLD)
```

def check_domains(domains: list):
return check_domains_rdap(domains)
