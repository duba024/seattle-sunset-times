import requests
import time
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
import pytz
import uuid

def get_sun_events(current_date):
    # Washington State Coordinates
    sun_times_url = f"https://api.sunrise-sunset.org/json?lat=47.6062&lng=-122.3321&date={current_date}"
    
    # Try up to 3 times if the API is busy
    for attempt in range(3):
        try:
            response = requests.get(sun_times_url, timeout=10)
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
                # Create a unique ID so your Mac doesn't see duplicates
                e_sunset.uid = str(uuid.uuid4()) 
                return [e_sunset]
            else:
                time.sleep(2) # Wait and try again
        except:
            time.sleep(2)
    return []

c = Calendar()
# Generate 90 days
dates = [(datetime.now(timezone.utc) + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(90)]

print(f"Starting build for {len(dates)} days...")

for date in dates:
    events = get_sun_events(date)
    for event in events:
        c.events.add(event)
    # Slow down to 1.5 seconds to keep the API happy
    time.sleep(1.5) 

# Save the final file
with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())

print("Done! File saved.")
