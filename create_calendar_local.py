from ics import Calendar, Event
from datetime import datetime, timezone, timedelta
from astral import LocationInfo
from astral.sun import sun
import uuid

# Seattle Coordinates
city = LocationInfo("Seattle", "USA", "America/Los_Angeles", 47.6062, -122.3321)
c = Calendar()

# Calculate 90 days
for i in range(90):
    d = datetime.now(timezone.utc) + timedelta(days=i)
    s = sun(city.observer, date=d)
    
    e = Event()
    e.name = "🌇 Sunset"
    e.begin = s['sunset']
    e.duration = {'seconds': 900}
    e.uid = str(uuid.uuid4()) # This forces the file to be "new" every time
    c.events.add(e)

# NO SPACES AT THE START OF THESE TWO LINES
with open('sun.ics', 'w') as f:
    f.writelines(c.serialize_iter())
