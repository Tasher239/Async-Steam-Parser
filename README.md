# Асинхронный парсер Steam

Проект представляет собой асинхронный веб-парсер, разработанный для извлечения данных из Steam Store.
Парсер выполняет поисковые запросы, переходит по страницам и извлекает подробную информацию об играх,
такую как название, цена, рейтинг, разработчик, жанр и дата выхода. Извлеченные данные сохраняются в
базу данных SQLite (results.db) для дальнейшего использования. Цель проекта — углубить понимание современных методов веб-скрапинга, реализовав собственный парсер с нуля.

## Возможности

- Асинхронный парсинг: Использует `asyncio` для эффективных и параллельных HTTP-запросов.
- Настраиваемые запросы: Позволяет задавать поисковые запросы, количество страниц для парсинга и количество результатов на запрос.
- Извлечение данных: Извлекает следующие данные для каждой игры:
- Название
- Цена
- Текстовый рейтинг (например, "Очень положительные")
- Разработчик
- Жанр(ы)
- Дата выхода
- База данных `SQLite`: Сохраняет извлеченные данные в структурированном формате для удобного доступа и анализа.
- Обработка пагинации: Избегает динамической загрузки контента с помощью query-параметров в URL.


## Алгоритм

Как это работает:
- Поисковые запросы: Парсер выполняет N поисковых запросов (например, "стратегия") в Steam Store.
- Пагинация: Для каждого запроса переходит по первым K страницам (или меньше, если страниц недостаточно).
- Извлечение данных: Извлекает данные об играх с каждой страницы.
- Сохранение в базу данных: Сохраняет извлеченные данные в базу данных SQLite (results.db) в таблицу games.

## Пример полученной базы данных
| id | title | price | rating | developer | genres | release_date |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Dark Strategy | 1417,50 руб | Very Positive | Fictiorama Studios, Jongwoo Kim, Erica Lahaie, FX Bilodeau, Tanya Short, Bobby Two Hands | Indie, Simulation, Strategy | None |
| 2 | Stellaris | 2199 руб | Very Positive | Paradox Development Studio | Simulation, Strategy | 09.05.2016 |
| 3 | Strategy Pack | 1170 руб | Very Positive | None | None | None |
| 4 | Strategy Tribe | 429,75 руб | Very Positive | Space Boat Studios, Baked Games, Creative Storm Entertainment | Casual, Simulation, Indie, RPG, Strategy | None |
| 5 | Strategy Bundle | 5519,46 руб | Very Positive | Core Engage, Mimimi Games, Unfrozen, Yaza Games, Alter Games, Skirmish Mode Games, Spitfire Interactive | Indie, Simulation, Strategy, Early Access, RPG, Action | None |
| 6 | Panzer Strategy | 1351 руб | Mixed | Starni Games | Indie, Strategy | 31.08.2018 |
| 7 | Strategy Bundle | 2307,60 руб | Mostly Positive | None | None | None |
| 8 | Bodycam | 1200 руб | Mostly Positive | Reissad Studio | Action, Indie, Massively Multiplayer, Simulation, Strategy, Early Access | 07.06.2024 |
| 9 | Strategy Bundle | 675,90 руб | Mostly Positive | Bureau Bravin, Grumpy Owl Games, Königsborgs, Hack The Publisher | Indie, Simulation, Strategy, RPG, Casual | None |
| 10 | Strategy Games | 67,67 руб | Mostly Positive | Post Mortem Pixels, Tetabester, Dmitry Kozlov | Indie, Strategy, Casual, Simulation | None |
