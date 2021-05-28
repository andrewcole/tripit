from datetime import date
from functools import cached_property

from loguru import logger


class Profile(object):
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

    def __eq__(self, other):
        if not isinstance(other, Profile):
            return NotImplemented
        return (
            self.uuid == other.uuid
            and self.public_display_name == other.public_display_name
            and self.screen_name == other.screen_name
        )

    @property
    def _keys(self):
        return [
            "NotificationSettings",
            "public_display_name",
            "screen_name",
            "uuid",
            "@attributes",
            "ProfileEmailAddresses",
            "activity_feed_url",
            "alerts_feed_url",
            "company",
            "date_endian_format",
            "distance",
            "home_city",
            "home_country_code",
            "hour_clock",
            "ical_url",
            "is_cal_detailed",
            "is_cal_localtime",
            "is_client",
            "is_pro",
            "language_tag",
            "photo_url",
            "profile_url",
            "temperature",
        ]

    @cached_property
    def public_display_name(self):
        return self._dictionary["public_display_name"]

    @cached_property
    def screen_name(self):
        return self._dictionary["screen_name"]

    @cached_property
    def uuid(self):
        return self._dictionary["uuid"]

    @cached_property
    def trips(self):
        return [i for i in self.api.trips if i.owner == self]

    @property
    def trip_count(self):
        return len(self.trips)
