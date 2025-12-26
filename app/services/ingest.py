from typing import Dict, List
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from datetime import datetime, timezone

from ..models import Source, Item
from ..crawlers.rss import fetch_rss_items

def upsert_items(db: Session, source: Source, items: List[Dict]) -> int:
    if not items:
        return 0
    
    rows = []
    for it in items:
        rows.append(
            {
                "source_id": source.id,
                "title": it["title"],
                "url": it["url"],
                "published_at": it.get("published_at"),
                "snippet": it.get("snippet"),
                "fetched_at": datetime.now(timezone.utc),
            }
        )

    stmt = insert(Item).values(rows)
    stmt = stmt.on_conflict_do_nothing(index_elements=["url"])

    result = db.execute(stmt)
    db.commit()

    return result.rowcount or 0


def run_ingest(db: Session) -> Dict:
    sources = db.query(Source).filter(Source.enabled.is_(True)).all()
    
    total_sources = 0
    total_fetched = 0
    total_inserted = 0

    for s in sources:
        total_sources += 1
        if s.type == "rss":
            fetched = fetch_rss_items(s.url, limit=50)
            total_fetched += len(fetched)
            total_inserted += upsert_items(db, s, fetched)
        
    return {
        "sources": total_sources,
        "fetched": total_fetched,
        "inserted": total_inserted,
    }

