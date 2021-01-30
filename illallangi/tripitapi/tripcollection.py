from collections.abc import Sequence

from .trip import Trip


class TripCollection(Sequence):
    def __init__(self, api, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.api = api
        self._collection = []

        for past in ["false", "true"]:
            page_num = 1
            while True:
                result = self.api.get(
                    self.api.endpoint
                    / "list"
                    / "trip"
                    / "traveler"
                    / "true"
                    / "past"
                    / past
                    / "include_objects"
                    / "false"
                    % {
                        "format": "json",
                        "page_size": self.api.page_size,
                        "page_num": page_num,
                    },
                )
                if "Trip" not in result:
                    break

                for o in (
                    [result["Trip"]]
                    if not isinstance(result["Trip"], list)
                    else result["Trip"]
                ):
                    self._collection.append(Trip(self.api, o))
                page_num += 1
                if page_num > int(result["max_page"]):
                    break

    def __iter__(self):
        return self._collection.__iter__()

    def __getitem__(self, key):
        return list(self._collection).__getitem__(key)

    def __len__(self):
        return list(self._collection).__len__()
