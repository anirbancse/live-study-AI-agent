"""Fetch and cache public AI news so the dashboard can refresh once per day."""

from __future__ import annotations

from datetime import datetime
import json
from pathlib import Path
from urllib.error import URLError
from urllib.request import Request, urlopen
import xml.etree.ElementTree as ET


FEED_URL = (
    "https://export.arxiv.org/api/query?"
    "search_query=all:%22artificial%20intelligence%22&max_results=8"
    "&sortBy=submittedDate&sortOrder=descending"
)


def get_daily_updates(cache_path: str | Path = "live_updates.json") -> dict:
    path = Path(cache_path)
    today = datetime.now().strftime("%Y-%m-%d")
    if path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        if cached.get("date") == today:
            return cached

    try:
        request = Request(FEED_URL, headers={"User-Agent": "AI-Learning-Agent/1.0"})
        with urlopen(request, timeout=8) as response:
            root = ET.fromstring(response.read())
        entries = []
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.findtext("{http://www.w3.org/2005/Atom}title", "").strip()
            link = entry.find("{http://www.w3.org/2005/Atom}link")
            published = entry.findtext("{http://www.w3.org/2005/Atom}published", "").strip()
            if title and link is not None and link.get("href"):
                entries.append({"title": " ".join(title.split()), "url": link.get("href"), "published": published})
        payload = {"date": today, "source": "arXiv", "items": entries, "status": "live"}
    except (OSError, URLError, ET.ParseError, TimeoutError):
        payload = {
            "date": today,
            "source": "arXiv",
            "items": [],
            "status": "unavailable",
            "message": "Live updates could not be refreshed; showing the learning plan.",
        }
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload
