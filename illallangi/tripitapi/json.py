from datetime import date, datetime
from json import JSONEncoder as encoder

from .air import Air
from .aircollection import AirCollection
from .airport import Airport
from .api import API
from .segment import Segment
from .segmentcollection import SegmentCollection
from .trip import Trip
from .tripcollection import TripCollection


class JSONEncoder(encoder):
    def default(self, obj):
        if isinstance(obj, date):
            return obj.isoformat()
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Air):
            return {
                "start": obj.start,
                "segments": obj.segments,
            }
        if isinstance(obj, AirCollection):
            return sorted(obj, key=lambda o: o.start)
        if isinstance(obj, Airport):
            return {
                "iata": obj.iata,
                "latitude": obj.latitude,
                "longitude": obj.longitude,
                "city": obj.city,
                "country": obj.country,
            }
        if isinstance(obj, API):
            return {
                "trips": obj.trips,
            }
        if isinstance(obj, Segment):
            return {
                "start": obj.start,
                "end": obj.end,
                "origin": obj.origin,
                "destination": obj.destination,
                "aircraft": obj.aircraft,
                "flight": obj.flight,
            }
        if isinstance(obj, SegmentCollection):
            return sorted(obj, key=lambda o: o.start)
        if isinstance(obj, Trip):
            return {
                "airs": obj.airs,
                "start": obj.start,
                "display_name": obj.display_name,
            }
        if isinstance(obj, TripCollection):
            return sorted(obj, key=lambda o: o.start)
        return super().default(obj)
