from app import create_new_event, get_this_weeks_events
from fastapi import FastAPI,Body, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from schemas import Event
from database import SessionLocal, engine
import database
from sqlalchemy.orm import sessionmaker, Session

database.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root(db: Session = Depends(get_db)):
    return get_this_weeks_events(db)

@app.post("/event")
async def create_event(event: Event, db: Session = Depends(get_db)):
    create_new_event(event, db)
