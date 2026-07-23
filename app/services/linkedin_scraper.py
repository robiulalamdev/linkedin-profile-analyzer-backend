import httpx
import re


async def scrape_linkedin_profile(url: str) -> dict:
    """
    Extract LinkedIn profile data from a public profile URL.
    Uses httpx to fetch the public page and extract available information.
    """
    normalized_url = _normalize_url(url)

    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15.0) as client:
            response = await client.get(
                normalized_url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml",
                    "Accept-Language": "en-US,en;q=0.9",
                },
            )
            html = response.text
            return _parse_profile(html, normalized_url)
    except Exception:
        return {"url": normalized_url, "rawHtml": "", "error": "Could not fetch profile"}


def _normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith("http"):
        url = "https://" + url
    url = re.sub(r"/$", "", url)
    return url


def _parse_profile(html: str, url: str) -> dict:
    profile = {"url": url}

    # Extract meta tags for basic info
    og_title = re.search(r'<meta\s+property="og:title"\s+content="([^"]*)"', html)
    og_desc = re.search(r'<meta\s+property="og:description"\s+content="([^"]*)"', html)

    if og_title:
        profile["title"] = og_title.group(1)
    if og_desc:
        profile["description"] = og_desc.group(1)

    # Try to extract structured data
    json_ld = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.DOTALL)
    for block in json_ld:
        try:
            import json
            data = json.loads(block)
            if isinstance(data, dict):
                if "name" in data:
                    profile["name"] = data["name"]
                if "jobTitle" in data:
                    profile["headline"] = data["jobTitle"]
                if "description" in data:
                    profile["about"] = data["description"]
                if "worksFor" in data:
                    profile["company"] = data["worksFor"]
                if "alumniOf" in data:
                    profile["education"] = data["alumniOf"]
        except Exception:
            continue

    # Extract headline from page content
    headline_match = re.search(r'<h1[^>]*class="[^"]*text-heading[^"]*"[^>]*>(.*?)</h1>', html, re.DOTALL)
    if headline_match:
        profile["headline"] = _clean_html(headline_match.group(1))

    # Extract about section
    about_match = re.search(r'<section[^>]*id="about"[^>]*>(.*?)</section>', html, re.DOTALL)
    if about_match:
        profile["about"] = _clean_html(about_match.group(1))

    profile["rawHtml"] = html
    return profile


def _clean_html(html: str) -> str:
    text = re.sub(r'<[^>]+>', ' ', html)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()
