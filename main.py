from app import get_this_weeks_events
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI() #uvicorn main:app --reload

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*']
)


@app.get("/")
async def root():
    return get_this_weeks_events()
