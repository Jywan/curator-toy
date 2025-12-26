from fastapi import FastAPI, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import select, desc
from contextlib import asynccontextmanager
from typing import Optional, List

from .db import Base, engine, get_db
from .models import Source, Item
from .schemas import SourceCreate, SourceOut, ItemOut
from .services.ingest import run_ingest

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(title= "Curator MVP", lifespan=lifespan)

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/sources", response_model=SourceOut)
def create_source(payload: SourceCreate, db: Session = Depends(get_db)):
    src = Source(**payload.model_dump())
    db.add(src)
    db.commit()
    db.refresh(src)
    return src

@app.get("/sources", response_model=List[SourceOut])
def list_sources(db: Session = Depends(get_db)):
    return db.execute(select(Source).order_by(Source.id)).scalars().all()

@app.get("/items", response_model=List[ItemOut])
def list_items( q: Optional[str] = Query(default=None),
                source_id: Optional[int] = None,
                limit: int = Query(default=50, ge=1, le=200),
                db: Session = Depends(get_db),
                ):
    stmt = select(Item).order_by(desc(Item.published_at), desc(Item.fetched_at))

    if source_id is not None:
        stmt = stmt.where(Item.source_id == source_id)
    if q:
        like = f"%{q}%"
        stmt = stmt.where ((Item.title.ilike(like)) | (Item.snippet.ilike(like)))
    return db.execute(stmt.limit(limit)).scalars().all()

@app.post("/ingest/run")
def ingest_run(db: Session = Depends(get_db)):
    return run_ingest(db)