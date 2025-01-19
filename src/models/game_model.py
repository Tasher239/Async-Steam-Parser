from dataclasses import dataclass


@dataclass
class GameModel:
    title: str
    price: str | None
    rating: int | None
    developer: str | None
    genres: list[int] | None
    release_date: str | None
