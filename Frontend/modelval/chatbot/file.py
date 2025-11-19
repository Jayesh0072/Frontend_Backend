from typing import NamedTuple


class File(NamedTuple):
    content: object
    type: str
    name: str
