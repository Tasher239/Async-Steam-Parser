import asyncio
import aiohttp


class Worker:
    def __init__(self, delay):
        self.delay = delay
        self.base_url_pattern = (
            "https://store.steampowered.com/search/?term={query}&page={page}&cc=ru"
        )

    async def parse_worker(self, queue, db_processor, parser):
        async with aiohttp.ClientSession() as session:
            while not queue.empty():
                query, page = await queue.get()
                url = self.base_url_pattern.format(query=query, page=page)
                print(f"Fetching: {url}")
                try:
                    games = await parser.fetch_page(session, url)
                    if not games:
                        print(f"Страница {page} по запросу '{query}' пуста. Останавливаем обработку.")
                        queue.task_done()
                        break

                    await db_processor.save_games(games)
                    print(f"Обработано {len(games)} игр со страницы {page} по запросу '{query}'")

                except Exception as e:
                    print(f"Ошибка в {url}: {e}")

                await asyncio.sleep(self.delay)
                queue.task_done()
