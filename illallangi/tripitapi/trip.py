from json import dumps
from datetime import date
from functools import cached_property
from more_itertools import one

from loguru import logger

from .aircollection import AirCollection
from .profile import Profile


class Trip(object):
    def __init__(self, api, dictionary, result, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self._dictionary = dictionary
        self._result = result

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
            "description",
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

    @cached_property
    def owner_ref(self):
        return one(
            i
            for i in (
                [self._dictionary["TripInvitees"]["Invitee"]]
                if not isinstance(self._dictionary["TripInvitees"]["Invitee"], list)
                else self._dictionary["TripInvitees"]["Invitee"]
            )
            if i.get("is_owner", False)
        )["@attributes"]["profile_ref"]

    @cached_property
    def owner(self):
        return Profile(
            self.api,
            one(
                i
                for i in (
                    [self._result["Profile"]]
                    if not isinstance(self._result["Profile"], list)
                    else self._result["Profile"]
                )
                if i["@attributes"]["ref"] == self.owner_ref
            ),
        )

    @cached_property
    def relative_url(self):
        return self._dictionary["relative_url"]

    @cached_property
    def url(self):
        return self.api.url_endpoint / self.relative_url.strip("/")

    @property
    def is_valid(self):
        if len(self.airs) == 0:
            logger.warning(
                f"Trip {self.id} ({self.url}) is not valid as contains no air objects, skipping."
            )
            return False
        return True
