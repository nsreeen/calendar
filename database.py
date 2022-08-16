from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String

from schemas import Event


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class DbEvent(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String)
    start = Column(String, index=True)
    end = Column(String, index=True)

def create_event(event: Event, db: Session) -> Event:
    db_event = DbEvent(summary=event.summary, start=event.start, end=event.end)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return Event(summary=db_event.summary, start=db_event.start, end=db_event.end)

def get_events(db: Session):
    return [Event(summary=db_event.summary, start=db_event.start, end=db_event.end) for db_event in db.query(DbEvent)]
