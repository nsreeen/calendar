from app import create_new_event, get_this_weeks_events
from fastapi import FastAPI,Body
from fastapi.middleware.cors import CORSMiddleware
from typing import Union
from pydantic import BaseModel

class Event(BaseModel):
    summary: str
    start: str 
    end: str

app = FastAPI() #uvicorn main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)

app.state.event_store = {}
app.state.event_store[1] = "hello"

@app.get("/")
async def root():
    return get_this_weeks_events()

@app.post("/event")
async def create_event(event: Event):
    create_new_event(event)