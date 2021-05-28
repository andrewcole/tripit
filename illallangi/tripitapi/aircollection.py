from collections.abc import Sequence

from .air import Air


class AirCollection(Sequence):
    def __init__(self, api, trip, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self._collection = []

        for past in ["false", "true"]:
            page_num = 1
            while True:
                result = self.api.get(
                    self.api.endpoint
                    / "list"
                    / "object"
                    / "trip_id"
                    / trip.id
                    / "past"
                    / past
                    / "traveler"
                    / "true"
                    / "type"
                    / "air"
                    % {
                        "format": "json",
                        "page_size": self.api.page_size,
                        "page_num": page_num,
                    },
                )
                if "AirObject" not in result:
                    break

                for o in [
                    air
                    for air in [
                        Air(self.api, dictionary)
                        for dictionary in (
                            [result["AirObject"]]
                            if not isinstance(result["AirObject"], list)
                            else result["AirObject"]
                        )
                    ]
                    if air.is_valid
                ]:
                    self._collection.append(o)
                page_num += 1
                if page_num > int(result["max_page"]):
                    break

    def __iter__(self):
        return self._collection.__iter__()

    def __getitem__(self, key):
        return list(self._collection).__getitem__(key)

    def __len__(self):
        return list(self._collection).__len__()
