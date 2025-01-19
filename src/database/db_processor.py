import aiosqlite
from models.game_model import GameModel


class DBProcessor:
    def __init__(self, db_name="database/results.db"):
        self.db_name = db_name

    async def init_db(self):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
                CREATE TABLE IF NOT EXISTS games (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT,
                    price TEXT,
                    rating TEXT,
                    developer TEXT,
                    genres TEXT,
                    release_date TEXT
                )
            """
            )
            await db.commit()

    async def save_game(self, game: GameModel):
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(
                """
            INSERT INTO games (title, price, rating, developer, genres, release_date)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
                (
                    game.title,
                    game.price,
                    game.rating,
                    game.developer,
                    game.genres,
                    game.release_date,
                ),
            )
            await db.commit()

    async def save_games(self, games: list[GameModel]):
        async with aiosqlite.connect(self.db_name) as db:
            await db.executemany(
                """
                INSERT INTO games (title, price, rating, developer, genres, release_date)
                VALUES (?, ?, ?, ?, ?, ?)
            """,
                [
                    (
                        game.title,
                        game.price,
                        game.rating,
                        game.developer,
                        game.genres,
                        game.release_date,
                    )
                    for game in games
                ],
            )
            await db.commit()
