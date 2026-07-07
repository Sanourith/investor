from typing import TypedDict


class PriceResult(TypedDict):
    Name: str
    Price: float | None
    Time: str
    Error: str | None
