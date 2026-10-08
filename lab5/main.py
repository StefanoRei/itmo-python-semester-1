from pathlib import Path
import csv
import re


ROOT = Path(__file__).parent
EMAIL = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
URL = r"https?://[A-Za-z0-9.-]+(?:/[A-Za-z0-9._~/%?=&+#-]*)?"
DATE = r"\d{4}[-/.]\d{1,2}[-/.]\d{1,2}|\d{1,2}[-/.]\d{1,2}[-/.]\d{4}"


def first_task():
    source = (ROOT / "task1-ru.txt").read_text(encoding="utf-8")
    numbers = re.findall(r"(?<![\w.,])[-+]?\d+(?:[.,]\d+)?(?![\w.,])", source)
    words = re.findall(r"(?<![А-Яа-яЁё])[А-Яа-яЁё]{6}(?![А-Яа-яЁё])|(?<![А-Яа-яЁё])[А-Яа-яЁё]{8}(?![А-Яа-яЁё])", source)
    print("Задание 1 — числа:", numbers)
    print("Задание 1 — слова на 6 и 8 букв:", words)


def second_task():
    source = (ROOT / "task2.html").read_text(encoding="utf-8", errors="replace")
    contents = re.findall(r"\bcontent\s*=\s*([\"'])(.*?)\1", source, re.I | re.S)
    print("Задание 2 — значения content:", [value for _, value in contents])


def third_task():
    source = (ROOT / "task3.txt").read_text(encoding="ascii")
    tokens = source.split()
    if len(tokens) % 5:
        raise ValueError("Число полей не кратно пяти")
    records = []
    for index in range(0, len(tokens), 5):
        fields = tokens[index:index + 5]
        def pick(pattern):
            found = [token for token in fields if re.fullmatch(pattern, token)]
            if len(found) != 1:
                raise ValueError(f"Неоднозначная запись {index // 5 + 1}: {fields}")
            return found[0]
        records.append((pick(r"\d+"), pick(r"[A-Za-z-]+"), pick(EMAIL), pick(DATE), pick(URL)))
    with (ROOT / "users.csv").open("w", encoding="utf-8", newline="") as destination:
        writer = csv.writer(destination)
        writer.writerow(("ID", "Фамилия", "Почта", "Дата регистрации", "Сайт"))
        writer.writerows(records)
    print(f"Задание 3 — сохранено {len(records)} записей в users.csv")


def extra_task():
    source = (ROOT / "task_add.txt").read_text(encoding="utf-8")
    domain = r"[A-Za-z0-9-]+\.(?:com|ter|now|mas|tee|ru|le|ed|ly)"
    email = r"[A-Za-z0-9._%+-]+@" + domain
    url = r"https?://" + domain
    for label, expression in (("даты", DATE), ("почта", email), ("сайты", url)):
        matches = re.findall(r"(?<=\s)(?:" + expression + r")", source)
        print(f"Дополнительное задание — {label} ({len(matches)}):", matches)


if __name__ == "__main__":
    first_task()
    second_task()
    third_task()
    extra_task()
