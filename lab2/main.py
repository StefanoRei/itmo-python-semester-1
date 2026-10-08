from pathlib import Path
import argparse
import csv
import xml.etree.ElementTree as ET


ROOT = Path(__file__).parent


def books():
    with (ROOT / "books-en.csv").open(encoding="latin-1", newline="") as source:
        return list(csv.DictReader(source, delimiter=";"))


def bibliography(records):
    lines = [
        f"{number}. {book['Book-Author']}. {book['Book-Title']} - {book['Year-Of-Publication']}"
        for number, book in enumerate(records[:20], 1)
    ]
    (ROOT / "references.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")


def currencies():
    root = ET.parse(ROOT / "currency.xml").getroot()
    codes = []
    values = []
    for currency in root.findall("Valute"):
        codes.append(currency.findtext("CharCode"))
        values.append(float(currency.findtext("Value").replace(",", ".")))
    return codes, values


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--author", default="", help="часть имени автора для поиска")
    args = parser.parse_args()
    records = books()
    print("Названий длиннее 30 символов:", sum(len(book["Book-Title"]) > 30 for book in records))
    matches = [book for book in records if args.author.casefold() in book["Book-Author"].casefold()]
    print(f"Найдено по автору «{args.author}»: {len(matches)}")
    for book in matches[:20]:
        print(f"{book['Book-Author']}: {book['Book-Title']}")
    bibliography(records)
    codes, values = currencies()
    print("CharCode:", codes)
    print("Value:", values)
    publishers = sorted({book["Publisher"] for book in records})
    print(f"Издательства без повторений ({len(publishers)}):", ", ".join(publishers))
    print("20 самых популярных книг:")
    for book in sorted(records, key=lambda item: int(item["Downloads"]), reverse=True)[:20]:
        print(f"{book['Downloads']:>5}  {book['Book-Title']}")


if __name__ == "__main__":
    main()
