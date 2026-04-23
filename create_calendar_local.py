import time
from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sun
import uuid

# Define Seattle location locally (no API needed)
city = LocationInfo("Seattle", "USA", "America/Los_Angeles", 47.6062, -122.3321)

c = Calendar()

# Generate 90 days of dates
base = datetime.now(timezone.utc)
dates = [base + timedelta(days=i) for i in range(90)]

print(f"Calculating sunsets for {len(dates)} days...")

for d in dates:
    # Calculate sun times for the specific date
    s = sun(city.observer, date=d)
    
    # Create the event
    e_sunset = Event()
    e_sunset.name = "🌇 Sunset"
    e_sunset.begin = s['sunset']
    e_sunset.duration = {'seconds': 15*60}
    e_sunset.uid = str(uuid.uuid4())
    
    c.events.add(e_sunset)

# Save the final file
with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())

print("Done! 90-day calendar saved.")
