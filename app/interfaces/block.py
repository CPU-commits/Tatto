from pydantic import BaseModel
from datetime import datetime

class CalendarBlock(BaseModel):
    day: str
    time_since: str
    time_until: str

    def to_model(self):
        return {
            'day': self.day,
            'time_since': datetime.strptime(self.time_since, '%H:%M:%S'),
            'time_until': datetime.strptime(self.time_until, '%H:%M:%S'),
        }
