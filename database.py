from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy import Column, Integer, String

from schemas import Event as PydanticEvent


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    summary = Column(String)
    start = Column(String, index=True)
    end = Column(String, index=True)

def create_event(event: PydanticEvent, db: Session) -> Event:
    db_event = Event(summary=event.summary, start=event.start, end=event.end)
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event


# def get_events(db: Session):
#     return db.query(models.Event)
