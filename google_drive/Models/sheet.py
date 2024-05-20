from typing import List
from Models.localized_column import LocalizedColumn


class Sheet:

    def __init__(self, name: str, columns: List[LocalizedColumn]):
        self._name = name
        self._columns = columns

    @property
    def name(self) -> str:
        return self._name

    @property
    def columns(self) -> List[LocalizedColumn]:
        return self._columns
