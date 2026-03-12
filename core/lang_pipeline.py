from __future__ import annotations
import os
import re
import json
import random
from typing import Dict, List, Optional, Callable, Tuple

# OpenAI
try:
    from openai import OpenAI
except Exception:
    OpenAI = None

TEMPLATE_LANG_BASE = "de"
DEFAULT_MODEL = "gpt-5-mini"

SPECIAL_NUMERIC = {"app_price","rating_value","rating_count"}

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
    "page_title_main",
    "page_description_main",
    "site_name"
}

CURRENCY_FALLBACK = {
    "EUR":1.0,"USD":1.08,"GBP":0.85,"CHF":0.95,
    "PLN":4.3,"CZK":25,"SEK":11,"DKK":7.5,
    "TRY":33,"ILS":4,"AED":3.97,
    "CNY":7.8,"JPY":165,
    "CAD":1.47,"AUD":1.65,
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
    "CH":"switzerland.png"
}

# -------------------------
# Utils
# -------------------------

def _round_dynamic(x: float) -> int:

    if x < 400:
        step=50
    elif x < 1500:
        step=100
    elif x < 9000:
        step=500
    else:
        step=1000

    return int(round(x/step)*step)

def _make_price(currency:str)->int:

    rate=CURRENCY_FALLBACK.get(currency,1.0)
    val=250*rate
    return max(50,_round_dynamic(val))

def _infer_cc(target_lang:str,geo_code:Optional[str])->str:

    if geo_code and len(geo_code)==2:
        return geo_code.upper()

    if "-" in target_lang:
        return target_lang.split("-")[-1].upper()

    return "DE"

def _gmail_for_domain(domain:str)->str:

    base=domain.split(".")[0]
    base=re.sub(r"[^a-z0-9\-]","",base.lower())
    return f"support.{base}@gmail.com"

def _escape_php(s:str)->str:
    return s.replace("\\","\\\\").replace('"','\\"')

def _set_php_var(content:str,var:str,value:str,numeric:bool)->str:

    if numeric:
        rhs=value
    else:
        rhs=f"\"{_escape_php(str(value))}\""

    pattern=re.compile(rf"(^\s*\${var}\s*=\s*)(.*?)(;\s*$)",re.MULTILINE)

    if pattern.search(content):
        return pattern.sub(rf"\g<1>{rhs}\g<3>",content,1)

    insert=f"${var} = {rhs};\n"

    if "<?php" in content:
        lines=content.splitlines(True)
        for i,l in enumerate(lines):
            if "<?php" in l:
                lines.insert(i+1,insert)
                return "".join(lines)

    return insert+content

# -------------------------
# OpenAI
# -------------------------

def _get_openai():

    if OpenAI is None:
        raise RuntimeError("openai lib missing")

    key=os.getenv("OPENAI_API_KEY","").strip()

    if not key:
        raise RuntimeError("OPENAI_API_KEY missing")

    return OpenAI(api_key=key)

def _llm_json(client,model,system,payload):

    r=client.chat.completions.create(
        model=model,
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":json.dumps(payload,ensure_ascii=False)}
        ],
        response_format={"type":"json_object"}
    )

    txt=r.choices[0].message.content or "{}"

    try:
        return json.loads(txt)
    except:
        return {}

# -------------------------
# Placeholder protect
# -------------------------

PH_RE=re.compile(r"(\$[A-Za-z_]\w*)")

def _protect(s:str):

    arr=[]

    def repl(m):
        arr.append(m.group(0))
        return f"__PH{len(arr)-1}__"

    t=PH_RE.sub(repl,s)

    mp={f"__PH{i}__":arr[i] for i in range(len(arr))}

    return t,mp

def _restore(s:str,mp:dict):

    for k,v in mp.items():
        s=s.replace(k,v)

    return s

# -------------------------
# Extract strings
# -------------------------

STRING_RE=re.compile(r'("([^"\\]|\\.)*"|\'([^\'\\]|\\.)*\')')

def _extract_strings(content):

    strings=[]
    spans=[]

    for m in STRING_RE.finditer(content):

        literal=m.group(1)
        inner=literal[1:-1]

        if not inner.strip():
            continue

        if inner.startswith("http"):
            continue

        strings.append(inner)

        spans.append((m.start(1)+1,m.end(1)-1))

    return strings,spans

def _apply_strings(content,spans,outs):

    if len(spans)!=len(outs):
        return content

    pairs=list(zip(spans,outs))
    pairs.sort(key=lambda x:x[0][0],reverse=True)

    for (s,e),txt in pairs:
        content=content[:s]+_escape_php(txt)+content[e:]

    return content

# -------------------------
# LLM translate
# -------------------------

def _llm_translate(client,model,strings,target_lang):

    protected=[]
    maps=[]

    for s in strings:
        ps,mp=_protect(s)
        protected.append(ps)
        maps.append(mp)

    system="""
Translate ALL strings into target language.
Return JSON: {"out":[...]}.
Do not modify placeholders __PH0__ etc.
"""

    data=_llm_json(client,model,system,{
        "target_lang":target_lang,
        "in":protected
    })

    out=data.get("out")

    if not isinstance(out,list) or len(out)!=len(protected):
        out=protected

    result=[]

    for s,mp in zip(out,maps):
        result.append(_restore(s,mp))

    return result

# -------------------------
# Template1 LLM specials
# -------------------------

def _generate_specials(client,model,cc,target_lang):

    system="Return JSON with title, description, address and personas."

    payload={"cc":cc,"lang":target_lang}

    return _llm_json(client,model,system,payload)

# -------------------------
# Main generator
# -------------------------

def generate_lang_files(
    template_bytes:bytes,
    geo_code:Optional[str],
    geo_currency:str,
    target_lang:str,
    domains:List[str],
    brand:str,
    template_kind:str="template_1",
    model:str=DEFAULT_MODEL,
    progress_cb:Optional[Callable[[float,str],None]]=None
)->List[Dict[str,str]]:

    client=_get_openai()

    template=template_bytes.decode("utf-8","replace")

    out=[]

    total=len(domains)

    for i,domain in enumerate(domains,1):

        cc=_infer_cc(target_lang,geo_code)
        currency=geo_currency.upper()

        price=_make_price(currency)

        rating_value=round(random.uniform(4.5,5.0),1)
        rating_count=random.randint(300,5000)

        content=template

        # TEMPLATE 1
        if template_kind in ("template_1","t1","1"):

            content=_set_php_var(content,"site_name","$source",False)
            content=_set_php_var(content,"site_url",f"https://{domain}",False)
            content=_set_php_var(content,"app_currency",currency,False)
            content=_set_php_var(content,"app_price",str(price),True)
            content=_set_php_var(content,"rating_value",str(rating_value),True)
            content=_set_php_var(content,"rating_count",str(rating_count),True)
            content=_set_php_var(content,"site_lang",target_lang,False)
            content=_set_php_var(content,"site_gmail",_gmail_for_domain(domain),False)

            gen=_generate_specials(client,model,cc,target_lang)

            for k,v in gen.items():
                content=_set_php_var(content,k,v,False)

        # TEMPLATE 2
        elif template_kind in ("template_2","t2","2"):

            content=_set_php_var(content,"site_name",brand,False)
            content=_set_php_var(content,"site_url",f"https://{domain}",False)
            content=_set_php_var(content,"app_currency",currency,False)
            content=_set_php_var(content,"app_price",str(price),True)
            content=_set_php_var(content,"rating_value",str(rating_value),True)
            content=_set_php_var(content,"rating_count",str(rating_count),True)
            content=_set_php_var(content,"site_lang",target_lang,False)

        # TEMPLATE 3
        elif template_kind in ("template_3","t3","3"):

            content=_set_php_var(content,"site_name","$source",False)
            content=_set_php_var(content,"site_url",f"https://{domain}",False)
            content=_set_php_var(content,"app_currency",currency,False)
            content=_set_php_var(content,"app_price",str(price),True)
            content=_set_php_var(content,"rating_value",str(rating_value),True)
            content=_set_php_var(content,"rating_count",str(rating_count),True)
            content=_set_php_var(content,"site_lang",target_lang,False)
            content=_set_php_var(content,"site_gmail",_gmail_for_domain(domain),False)

            img=f"images/{CRYPTO_IMAGES.get(cc,'crypto_main.png')}"

            content=_set_php_var(content,"crypto_img",img,False)

        strings,spans=_extract_strings(content)

        if strings:
            outs=_llm_translate(client,model,strings,target_lang)
            content=_apply_strings(content,spans,outs)

        if progress_cb:
            progress_cb(i/total,f"done {domain}")

        out.append({
            "domain":domain,
            "content":content
        })

    return out

# -------------------------
# Multi template wrapper
# -------------------------

def generate_lang_files_multi(
    template1_bytes,
    template2_bytes,
    template3_bytes,
    geo_code,
    geo_currency,
    target_lang,
    domains,
    domain_templates,
    brand,
    model=DEFAULT_MODEL,
    progress_cb=None
):

    out=[]

    for d in domains:

        kind=domain_templates.get(d,"template_1")

        if kind in ("template_2","2"):
            tpl=template2_bytes
            tk="template_2"

        elif kind in ("template_3","3"):
            tpl=template3_bytes
            tk="template_3"

        else:
            tpl=template1_bytes
            tk="template_1"

        r=generate_lang_files(
            tpl,
            geo_code,
            geo_currency,
            target_lang,
            [d],
            brand,
            tk,
            model,
            progress_cb
        )

        out.append(r[0])

    return out
