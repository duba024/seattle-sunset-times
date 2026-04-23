import requests
import time
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
import pytz

def get_sun_events(current_date):
    sun_times_url = f"https://api.sunrise-sunset.org/json?lat=47.6062&lng=-122.3321&date={current_date}"
    response = requests.get(sun_times_url)
    if response.status_code == 200:
        results = response.json()['results']
        time_format = "%I:%M:%S %p"
        year, month, day = map(int, current_date.split('-'))
        sunset_dt = datetime.strptime(results['sunset'], time_format).replace(
            tzinfo=pytz.utc, year=year, month=month, day=day)
        
        e_sunset = Event()
        e_sunset.name = "🌇 Sunset"
        e_sunset.begin = sunset_dt
        e_sunset.duration = {'seconds': 15*60}
        return [e_sunset]
    return []

# 1. Start the calendar
c = Calendar()

# 2. Get 90 days of dates
dates = [(datetime.now(timezone.utc) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)]

# 3. Add all dates to the calendar object
for date in dates:
    events = get_sun_events(date)
    for event in events:
        c.events.add(event)
    time.sleep(1) # This is indented correctly

# 4. SAVE THE FILE (THIS MUST NOT BE INDENTED)
with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())
