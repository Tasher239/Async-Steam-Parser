import asyncio
from database.db_processor import DBProcessor
from parsers.game_parser import AsyncParser
from async_workers.parse_worker import Worker
from saver.saver import export_to_markdown

REQUESTS = [
    "strategy",
    "action",
    "rpg",
]

CNT_PAGES = 3
CNT_WORKERS = 7
DELAY = 0.5


async def main():
    db_processor = DBProcessor()
    await db_processor.init_db()
    parser = AsyncParser()
    queue = asyncio.Queue()
    for query in REQUESTS:
        for page in range(1, CNT_PAGES + 1):
            await queue.put((query, page))

    worker = Worker(DELAY)
    workers = [
        asyncio.create_task(worker.parse_worker(queue, db_processor, parser))
        for _ in range(CNT_WORKERS)
    ]
    await queue.join()
    for w in workers:
        w.cancel()


if __name__ == "__main__":
    asyncio.run(main())
    db_path = "database/results.db"
    output_file = "database/games.md"

    export_to_markdown(db_path, output_file)
