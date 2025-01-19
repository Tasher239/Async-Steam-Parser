from bs4 import BeautifulSoup
from models.game_model import GameModel
import re
from datetime import datetime
import asyncio


class AsyncParser:
    def __init__(self):
        self.soup = None

    async def fetch_page(self, session, url):
        async with session.get(url) as response:
            response.raise_for_status()
            text = await response.text()
            self.soup = BeautifulSoup(text, "lxml")
            return await self.parse_page(session)

    @staticmethod
    async def fetch_game_details(session, game_url):
        async with session.get(game_url) as response:
            response.raise_for_status()
            text = await response.text()
            soup = BeautifulSoup(text, "lxml")

            genres = []
            genre_block = soup.find("b", string=re.compile(r"Genre:"))
            if genre_block:
                genre_links = genre_block.find_next_sibling("span")
                if genre_links:
                    genres = [a.get_text(strip=True) for a in genre_links.find_all("a")]

            developers = []
            developer_block = soup.find("b", string=re.compile(r"Developer:"))
            if developer_block:
                developer_span = developer_block.find_next_sibling("span")
                if developer_span:
                    developers = [
                        a.get_text(strip=True) for a in developer_span.find_all("a")
                    ]

                developer_row = soup.find("div", class_="dev_row")
                if developer_row:
                    developer_links = developer_row.find_all("a")
                    developers = [a.get_text(strip=True) for a in developer_links]

            return genres, developers

    async def parse_page(self, session):
        games = []
        tasks = []

        for game_element in self.soup.select(".search_result_row"):
            title = game_element.select_one(".title").get_text(strip=True)

            price_element = game_element.select_one(".discount_final_price")
            price = price_element.get_text(strip=True) if price_element else None

            rating_element = game_element.select_one(".search_review_summary")
            rating_text_value = None
            if rating_element:
                rating_text = rating_element.get("data-tooltip-html")
                if rating_text:
                    match = re.search(r"^(.*?)<br>", rating_text)
                    rating_text_value = match.group(1).strip() if match else None

            release_date_element = game_element.select_one(".search_released")
            release_date = (
                release_date_element.get_text(strip=True)
                if release_date_element
                else None
            )
            formatted_date = self.format_date(release_date)

            game_url = game_element.get("href")
            tasks.append(self.fetch_game_details(session, game_url))
            games.append(
                {
                    "title": title,
                    "price": price,
                    "rating": rating_text_value,
                    "date": formatted_date,
                }
            )

        details = await asyncio.gather(*tasks)

        for game, (genres, developers) in zip(games, details):
            game["genres"] = genres
            game["developers"] = developers

        game_models = []

        for game in games:
            game_models.append(
                GameModel(
                    game["title"],
                    game["price"],
                    game["rating"],
                    ", ".join(game["developers"]) if game["developers"] else None,
                    ", ".join(game["genres"]) if game["genres"] else None,
                    game["date"],
                ))

        return game_models

    @staticmethod
    def format_date(date_str):
        try:
            return datetime.strptime(date_str, "%d %b, %Y").strftime("%d.%m.%Y")
        except ValueError:
            pass

        try:
            return datetime.strptime(date_str, "%b %d, %Y").strftime("%d.%m.%Y")
        except ValueError:
            pass

        if re.fullmatch(r"\d{4}", date_str):
            return f"01.01.{date_str}"

        quarter_match = re.fullmatch(r"Q([1-4]) (\d{4})", date_str)
        if quarter_match:
            quarter, year = quarter_match.groups()
            quarter_start_month = {"1": "01", "2": "04", "3": "07", "4": "10"}[quarter]
            return f"01.{quarter_start_month}.{year}"

        return None
