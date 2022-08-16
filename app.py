from datetime import date, datetime, timedelta
import requests
from typing import Dict, List
import database
from schemas import Event
from sqlalchemy.orm import Session

def get_this_weeks_weekdays() -> List[str]:
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    # todo on weekend look at next week?
    weekdays = [monday + timedelta(days=i) for i in range(0,5)]
    return [date.strftime(date_time, "%Y%m%d") for date_time in weekdays]

def get_rc_events(this_weeks_dates: List[str]) -> List[Dict[str, str]]:
    rc_response = requests.get("https://www.recurse.com/calendar/events.ics?token=23d411fdde12626f789c977b90cc995d")
    rc_data = rc_response.content.decode("utf-8")
    raw_events = [event.replace("\\n\\n", "\r\n").split("\r\n") for event in rc_data.split("BEGIN:VEVENT")]
    event_list = []
    for event in raw_events:
        start, end, summary, status  = None, None, None, None
        for line in event:
            if line.startswith("DTSTART"):
                start = line.split(":")[1]
            if line.startswith("DTEND"):
                end = line.split(":")[1]
            if line.startswith("SUMMARY"):
                summary = line.split(":")[1]
            if line.startswith("STATUS"):
                status = line.split(":")[1]

        if not status or status != "CANCELLED":
            if start and start[:8] in this_weeks_dates:
                event = Event(summary=summary, start=start, end=end)
                event_list.append(event)

    return event_list

def convert_event_to_dict_and_add_day_of_week(event, this_weeks_dates) -> dict:
    day_of_week = this_weeks_dates.index(event.start[:8])
    return {
        "summary": event.summary,
        "start": event.start,
        "end": event.end,
        "day_of_week": day_of_week,
    }

def get_this_weeks_events(db: Session) -> List[Dict[str, str]]:
    this_weeks_dates = get_this_weeks_weekdays()
    rc_events = get_rc_events(this_weeks_dates)
    app_events = [event for event in database.get_events(db) if event.start[:8] in this_weeks_dates]
    all_events = rc_events + app_events
    return [convert_event_to_dict_and_add_day_of_week(event, this_weeks_dates) for event in all_events]

def create_new_event(event: Event, db: Session):
    print(event)
    db_event = database.create_event(event, db)
    print(f"db event: {db_event}")
