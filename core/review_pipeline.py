import os
import json
import re
from pathlib import Path
from openai import OpenAI
from core.translit import slugify_brand


def generate_review(
    template_path: str,
    platform_name: str,
    official_website: str,
    availability_country: str,
    currency: str,
    model: str = "gpt-5-mini",
) -> dict:
    """
    Генерує одне review на основі HTML-шаблону.

    Повертає dict:
    {
        "h1": "...",
        "title": "...",
        "description": "...",
        "slug": "...",
        "html": "..."
    }
    """

    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY не знайдено")

    template_file = Path(template_path)
    if not template_file.exists():
        raise FileNotFoundError(f"Не знайдено шаблон review: {template_path}")

    template_html = template_file.read_text(encoding="utf-8").strip()
    if not template_html:
        raise ValueError("Шаблон review порожній")

    website_clean = (official_website or "").strip().replace("https://", "").replace("http://", "").strip("/")
    website_url = f"https://{website_clean}" if website_clean else ""

    # страховка на slug, навіть якщо модель поверне кривий
    expected_slug = f"{slugify_brand(platform_name).lower()}-review-{slugify_brand(availability_country).lower()}"

    prompt = f"""
You are an expert SEO content editor and HTML template rewriter for review pages.

Your task is to rewrite the provided HTML review template for a specific platform.

IMPORTANT RULES:
- Keep the overall HTML structure intact.
- Keep all existing classes exactly the same.
- Keep all technical elements, wrappers, buttons, SVGs, and layout structure intact.
- Rewrite only the textual content and brand-specific visible values.
- Remove all <figure>...</figure> blocks completely if they exist.
- The review must begin with the platform facts block.
- The final HTML must contain exactly 4 "Visit Platform" CTA buttons, naturally distributed through the text.
- Keep the advantages/limitations block in the same structural format as in the template.
- Add exactly 1 quote block using <blockquote>.
- Maintain clear heading hierarchy and logical content flow.
- Use a positive-neutral editorial tone.
- Do not present the platform as suspicious, scammy, fake, or unsafe.
- Do not invent licenses, regulation, awards, company history, user counts, or precise claims that were not provided.
- The review must be written in natural English.
- The output must be substantially rewritten and not feel repetitive or template-spun.

INPUT DATA:
- Platform name: {platform_name}
- Official website: {website_clean}
- Availability country: {availability_country}
- Currency: {currency}
- MINIMUM DEPOSIT RULE:
Generate the minimum deposit yourself.
It should be a plausible rounded amount in the local currency.
Use a value logically close to the equivalent of about 250 EUR.
Prefer rounded values such as 50, 100, 150, 200, 250, 300, 500, or 1000 in the target currency.
Do not use awkward exact values like 237 or 413.
Use the generated value consistently in the facts block and anywhere else relevant.

SEMI-FIXED STRUCTURE TO FOLLOW:
1. facts block
2. intro
3. CTA button #1
4. platform overview / concept
5. registration / access
6. how it works
7. CTA button #2
8. key features
9. advantages and limitations
10. CTA button #3
11. risk awareness / user considerations
12. quote block
13. who might benefit
14. CTA button #4
15. final thoughts / overall perspective

OFFICIAL WEBSITE RULE:
- All visible website references must use: {website_clean}
- All CTA links must point to: {website_url}

FACTS BLOCK RULES:
Use these values in the facts block where relevant:
- Platform name: {platform_name}
- Official website: {website_clean}
- Availability: {availability_country}
- Currency: {currency}
- MINIMUM DEPOSIT RULE:
Generate the minimum deposit yourself.
It should be a plausible rounded amount in the local currency.
Use a value logically close to the equivalent of about 250 EUR.
Prefer rounded values such as 50, 100, 150, 200, 250, 300, 500, or 1000 in the target currency.
Do not use awkward exact values like 237 or 413.
Use the generated value consistently in the facts block and anywhere else relevant.

SLUG RULE:
Return slug in this format:
{expected_slug}

VERY IMPORTANT:
Return ONLY valid JSON with exactly these keys:
{{
  "h1": "...",
  "title": "...",
  "description": "...",
  "slug": "...",
  "html": "..."
}}

Do not wrap JSON in markdown.
Do not add explanations.
Do not add code fences.

HTML TEMPLATE:
{template_html}
""".strip()

    client = OpenAI(api_key=api_key)

    response = client.responses.create(
        model=model,
        input=prompt,
    )

    raw_text = (response.output_text or "").strip()
    if not raw_text:
        raise ValueError("Модель повернула порожню відповідь")

    # якщо модель випадково допише щось до/після JSON
    match = re.search(r"\{.*\}", raw_text, flags=re.DOTALL)
    if not match:
        raise ValueError("Не вдалося знайти JSON у відповіді моделі")

    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError as e:
        raise ValueError(f"Не вдалося розпарсити JSON review: {e}") from e

    required_fields = ["h1", "title", "description", "slug", "html"]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"У відповіді review немає поля: {field}")
        if not str(data[field]).strip():
            raise ValueError(f"Поле review порожнє: {field}")

    html = str(data["html"]).strip()

    # базова валідація
    if "<figure" in html.lower():
        raise ValueError("У review залишилися <figure> блоки")

    if html.count("visit-platform-btn") < 4:
        raise ValueError("У review менше 4 кнопок Visit Platform")

    if "pros-cons-section" not in html:
        raise ValueError("У review відсутній блок pros-cons-section")

    if "<blockquote" not in html.lower():
        raise ValueError("У review відсутній quote block")

    if website_clean and website_clean not in html:
        raise ValueError("У review не підставлено official website")

    # нормалізація slug на випадок кривої відповіді
    data["slug"] = re.sub(r"[^a-z0-9-]+", "-", str(data["slug"]).lower()).strip("-")
    if not data["slug"]:
        data["slug"] = expected_slug

    return {
        "h1": str(data["h1"]).strip(),
        "title": str(data["title"]).strip(),
        "description": str(data["description"]).strip(),
        "slug": str(data["slug"]).strip(),
        "html": html,
    }
