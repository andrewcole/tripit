from collections.abc import Sequence

from .segment import Segment


class SegmentCollection(Sequence):
    def __init__(self, collection, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._collection = [
            Segment(dictionary)
            for dictionary in (
                collection if isinstance(collection, list) else [collection]
            )
        ]

    def __iter__(self):
        return self._collection.__iter__()

    def __getitem__(self, key):
        return list(self._collection).__getitem__(key)

    def __len__(self):
        return list(self._collection).__len__()
