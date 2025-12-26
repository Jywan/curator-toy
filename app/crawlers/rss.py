import feedparser
from datetime import datetime, timezone
from typing import List, Dict, Optional

def _to_dt(struct_time) -> Optional[datetime]:
    if not struct_time:
        return None
    #feedparser는 time.struct를 준다
    return datetime(*struct_time[:6], tzinfo=timezone.utc)

def fetch_rss_items(feed_url: str, limit: int = 50) -> List[Dict]:
    feed = feedparser.parse(feed_url)
    out: List[Dict] = []

    for e in (feed.entries or [])[:limit]:
        title = (getattr(e, "title", "") or "").strip()
        link = (getattr(e, "link", "") or "").strip()
        if not title or not link:
            continue

        published_at = _to_dt(getattr(e, "published_parsed", None)) or _to_dt(getattr(e, "updated_parsed", None))
        summary = (getattr(e, "summary", None) or getattr(e, "description", None))

        out.append(
            {
                "title": title,
                "url": link,
                "published_at": published_at,
                "snippet": summary[:500] if isinstance(summary, str) and summary else None,
            }
        )

    return out