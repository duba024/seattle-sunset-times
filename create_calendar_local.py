from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sun
import uuid

# Seattle Setup
city = LocationInfo("Seattle", "USA", "America/Los_Angeles", 47.6062, -122.3321)
c = Calendar()

# Calculate 90 days of sunsets mathematically
for i in range(90):
    d = datetime.now(timezone.utc) + timedelta(days=i)
    s = sun(city.observer, date=d)
    
    e = Event()
    e.name = "🌇 Sunset"
    e.begin = s['sunset']
    e.duration = {'seconds': 900}
    e.uid = str(uuid.uuid4())
    c.events.add(e)

# Save the full 90-day file
with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())
