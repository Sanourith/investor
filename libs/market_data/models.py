from typing import TypedDict


class PriceResult(TypedDict):
    Price: float | None
    Time: str
    Error: str | None
