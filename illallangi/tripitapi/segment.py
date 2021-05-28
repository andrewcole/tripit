from datetime import datetime
from functools import cached_property

from loguru import logger

from pytz import timezone

from .airport import Airport


class Segment(object):
    def __init__(self, dictionary, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dictionary = dictionary
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
            "Emissions",
            "EndDateTime",
            "StartDateTime",
            "Status",
            "aircraft",
            "aircraft_display_name",
            "alternate_flights_url",
            "baggage_claim",
            "change_reservation_url",
            "conflict_resolution_url",
            "customer_support_url",
            "distance",
            "duration",
            "end_airport_code",
            "end_airport_latitude",
            "end_airport_longitude",
            "end_city_name",
            "end_country_code",
            "end_gate",
            "end_terminal",
            "entertainment",
            "general_fees_url",
            "id",
            "is_hidden",
            "is_international",
            "marketing_airline",
            "marketing_airline_code",
            "marketing_flight_number",
            "meal",
            "mobile_change_reservation_url",
            "mobile_customer_support_url",
            "mobile_home_url",
            "mobile_refund_info_url",
            "notes",
            "operating_airline",
            "operating_airline_code",
            "operating_flight_number",
            "refund_info_url",
            "seats",
            "service_class",
            "start_airport_code",
            "start_airport_latitude",
            "start_airport_longitude",
            "start_city_name",
            "start_country_code",
            "start_gate",
            "start_terminal",
            "stops",
            "web_home_url",
        ]

    @cached_property
    def start(self):
        return timezone(self._dictionary["StartDateTime"]["timezone"]).localize(
            datetime.fromisoformat(
                f'{self._dictionary["StartDateTime"]["date"]}T{self._dictionary["StartDateTime"]["time"]}'
            )
        )

    @cached_property
    def end(self):
        return timezone(self._dictionary["EndDateTime"]["timezone"]).localize(
            datetime.fromisoformat(
                f'{self._dictionary["EndDateTime"].get("date", self._dictionary["StartDateTime"]["date"])}T{self._dictionary["EndDateTime"]["time"]}'
            )
        )

    @cached_property
    def aircraft(self):
        return self._dictionary.get("aircraft")

    @cached_property
    def origin(self):
        return Airport(
            iata=self._dictionary["start_airport_code"],
            latitude=self._dictionary["start_airport_latitude"],
            longitude=self._dictionary["start_airport_longitude"],
            city=self._dictionary["start_city_name"],
            country=self._dictionary["start_country_code"],
        )

    @cached_property
    def destination(self):
        return Airport(
            iata=self._dictionary["end_airport_code"],
            latitude=self._dictionary["end_airport_latitude"],
            longitude=self._dictionary["end_airport_longitude"],
            city=self._dictionary["end_city_name"],
            country=self._dictionary["end_country_code"],
        )

    @cached_property
    def flight(self):
        return self._dictionary.get(
            "operating_airline_code", self._dictionary.get("marketing_airline_code", "")
        ) + self._dictionary.get(
            "operating_flight_number",
            self._dictionary.get("marketing_flight_number", ""),
        )

    @cached_property
    def relative_url(self):
        return self._dictionary["relative_url"]

    @cached_property
    def url(self):
        return self.api.url_endpoint / self.relative_url.strip("/")

    @property
    def is_valid(self):
        if not all(key in self._dictionary for key in ["StartDateTime"]):
            logger.warning(
                f'Segment {self._dictionary["id"]} is not valid due to missing keys, skipping.'
            )
            return False
        if "time" not in self._dictionary["StartDateTime"]:
            logger.warning(
                f'Segment {self._dictionary["id"]} is not valid due to missing keys in StartDateTime, skipping.'
            )
            return False
        return True
