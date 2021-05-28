from functools import cached_property

from loguru import logger

from .segmentcollection import SegmentCollection


class Air(object):
    def __init__(self, api, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary = dictionary
        self.api = api

        for key in self._dictionary.keys():
            if key not in self._keys:
                logger.error(
                    f'Unhandled key in {self.__class__}: {key}: {type(self._dictionary[key])}"{self._dictionary[key]}"'
                )
                continue
            logger.trace(
                f'{key}: {type(self._dictionary[key])}"{self._dictionary[key]}"'
            )

    @property
    def _keys(self):
        return [
            "Agency",
            "Segment",
            "Traveler",
            "booking_date",
            "booking_site_conf_num",
            "booking_site_name",
            "booking_site_phone",
            "booking_site_url",
            "display_name",
            "id",
            "is_client_traveler",
            "is_display_name_auto_generated",
            "is_purchased",
            "is_tripit_booking",
            "last_modified",
            "notes",
            "relative_url",
            "supplier_conf_num",
            "supplier_name",
            "total_cost",
            "trip_id",
        ]

    @cached_property
    def segments(self):
        return SegmentCollection(self._dictionary["Segment"])

    @cached_property
    def id(self):
        return self._dictionary["id"]

    @cached_property
    def trip_id(self):
        return self._dictionary["trip_id"]

    @cached_property
    def start(self):
        return sorted(self.segments, key=lambda o: o.start)[0].start

    @cached_property
    def relative_url(self):
        return self._dictionary["relative_url"]

    @cached_property
    def url(self):
        return self.api.url_endpoint / self.relative_url.strip("/")

    @property
    def is_valid(self):
        if len(self.segments) == 0:
            logger.warning(
                f"Air {self.id} ({self.url}) is not valid as contains no segment objects, skipping."
            )
            return False
        return True
