import requests
import time
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
import pytz

def get_sun_events(current_date):
    # Washington State Coordinates (Seattle)
    sun_times_url = f"https://api.sunrise-sunset.org/json?lat=47.6062&lng=-122.3321&date={current_date}"
    
    response = requests.get(sun_times_url)
    if response.status_code == 200:
        response_json = response.json()
        results = response_json['results']
    else:
        return []

    time_format = "%I:%M:%S %p"
    year, month, day = map(int, current_date.split('-'))
    
    # Convert sunset string to a proper datetime object
    sunset_str = results['sunset']
    sunset_dt = datetime.strptime(sunset_str, time_format).replace(
        tzinfo=pytz.utc, year=year, month=month, day=day
    )

    # Create the single Sunset event
    e_sunset = Event()
    e_sunset.name = "🌇 Sunset"
    e_sunset.begin = sunset_dt
    e_sunset.duration = {'seconds': 15*60}
    
    return [e_sunset]

# 1. Initialize the calendar once
c = Calendar()

# 2. Generate list of dates for the next 90 days
dates = [(datetime.now(timezone.utc) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)]

# 3. Loop through and add every sunset to the calendar object
for date in dates:
    try:
        events = get_sun_events(date)
        for event in events:
            c.events.add(event)
        # Sleep for 1 second to avoid being blocked by the API provider
        time.sleep(1)
    except Exception as e:
        print(f"Error on {date}: {e}")

# 4. SAVE THE FILE (Must be flush left, outside the loop)
with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())
