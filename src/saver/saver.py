import sqlite3


def export_to_markdown(db_path, output_file) -> None:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM games")
    rows = cursor.fetchall()

    cursor.execute("PRAGMA table_info(games)")
    columns = [column[1] for column in cursor.fetchall()]
    conn.close()

    markdown_table = "| " + " | ".join(columns) + " |\n"
    markdown_table += "| " + " | ".join(["---"] * len(columns)) + " |\n"

    for row in rows:
        markdown_table += "| " + " | ".join(str(value) for value in row) + " |\n"

    with open(output_file, "w", encoding="utf-8") as file:
        file.write(markdown_table)

    print(f"Таблица успешно экспортирована в {output_file}")
