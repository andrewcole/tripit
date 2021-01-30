from datetime import date
from functools import cached_property

from loguru import logger

from .aircollection import AirCollection


class Trip(object):
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
            "PrimaryLocationAddress",
            "TripInvitees",
            "TripPurposes",
            "TripStatuses",
            "display_name",
            "end_date",
            "id",
            "image_url",
            "is_private",
            "is_trip_owner_inner_circle_sharer",
            "last_modified",
            "primary_location",
            "relative_url",
            "start_date",
        ]

    @cached_property
    def airs(self):
        return AirCollection(self.api, self)

    @cached_property
    def id(self):
        return self._dictionary["id"]

    @cached_property
    def start(self):
        return date.fromisoformat(self._dictionary["start_date"])

    @cached_property
    def display_name(self):
        return self._dictionary["display_name"]
