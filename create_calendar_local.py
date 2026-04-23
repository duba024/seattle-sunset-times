import requests
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
import pytz

def get_sun_events(current_date):
    # Washington State Coordinates (Seattle)
    sun_times_url = f"https://api.sunrise-sunset.org/json?lat=47.6062&lng=-122.3321&date={current_date}"
    
    response = requests.get(sun_times_url)
    if response.status_code == 200:
        response_json = response.json()
    else:
        return []

    time_format = "%I:%M:%S %p"
    year, month, day = map(int, current_date.split('-'))
    
    # Convert the strings to datetime objects
    datetime_objects = {
        key: datetime.strptime(value, time_format).replace(tzinfo=pytz.utc)
        for key, value in response_json['results'].items()
        if key != 'day_length'
    }

    for key, dt_obj in datetime_objects.items():
        datetime_objects[key] = dt_obj.replace(year=year, month=month, day=day)

    calendar_time_format = "%Y-%m-%d %H:%M:%S"
    events = []

    # Create an event ONLY for today's sunset
    e_sunset = Event()
    e_sunset.name = "🌇 Sunset"
    e_sunset.begin = datetime_objects['sunset'].strftime(calendar_time_format)
    e_sunset.duration = {'seconds': 15*60}
    events.append(e_sunset)

    return events

c = Calendar()
current_date = datetime.now(timezone.utc).strftime('%Y-%m-%d')
dates = [(datetime.now(timezone.utc) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)]

for date in dates:
    for event in get_sun_events(date):
        c.events.add(event)

with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())
