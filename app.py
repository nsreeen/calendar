from datetime import date, datetime, timedelta
import requests
from typing import Dict, List
from database import create_event
import schemas
from sqlalchemy.orm import Session

def get_this_weeks_weekdays() -> List[str]:
    today = date.today()
    monday = today - timedelta(days=today.weekday())
    # todo on weekend look at next week?
    weekdays = [monday + timedelta(days=i) for i in range(0,5)]
    return [date.strftime(date_time, "%Y%m%d") for date_time in weekdays]

def get_events_from_rc_data(rc_data: str, this_weeks_dates: List[str]) -> List[Dict[str, str]]:
    raw_events = [event.replace("\\n\\n", "\r\n").split("\r\n") for event in rc_data.split("BEGIN:VEVENT")]
    event_list = []
    #events_by_day = {0: [],1: [],2: [],3: [],4: []}
    for event in raw_events:
        parsed_event = {}
        status = None
        for line in event:
            if line.startswith("DTSTART"):
                parsed_event["start"] = line.split(":")[1]
            if line.startswith("DTEND"):
                parsed_event["end"] = line.split(":")[1]
            if line.startswith("SUMMARY"):
                parsed_event["summary"] = line.split(":")[1]
            if line.startswith("STATUS"):
                status = line.split(":")[1]
            if line.startswith("URL"):
                parsed_event["url"] = line[4:]

        if not status or status != "CANCELLED":
            if "start" in parsed_event and parsed_event["start"][:8] in this_weeks_dates:
                day_of_week = this_weeks_dates.index(parsed_event["start"][:8])
                parsed_event["day_of_week"] = day_of_week
                event_list.append(parsed_event)
                #events_by_day[this_weeks_dates.index(parsed_event["start"][:8])].append(parsed_event)

    return event_list

# def get_this_weeks_events() -> Dict[int, List[Dict[str, str]]]:
#     this_weeks_dates = get_this_weeks_weekdays()
#     rc_response = requests.get("https://www.recurse.com/calendar/events.ics?token=23d411fdde12626f789c977b90cc995d")
#     rc_data = rc_response.content.decode("utf-8")
#     events_by_day = get_events_from_rc_data(rc_data, this_weeks_dates)
#     return events_by_day

def get_this_weeks_events() -> List[Dict[str, str]]:
    this_weeks_dates = get_this_weeks_weekdays()
    rc_response = requests.get("https://www.recurse.com/calendar/events.ics?token=23d411fdde12626f789c977b90cc995d")
    rc_data = rc_response.content.decode("utf-8")
    this_weeks_events = get_events_from_rc_data(rc_data, this_weeks_dates)
    return this_weeks_events

def create_new_event(event: schemas.Event, db: Session):
    print(event)
    db_event = create_event(event, db)
    print(f"db event: {db_event}")
