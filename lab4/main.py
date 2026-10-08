from itertools import combinations


ITEMS = {
    "r": (3, 25), "p": (2, 15), "a": (2, 15), "m": (2, 20),
    "i": (1, 5), "k": (1, 15), "x": (3, 20), "t": (1, 25),
    "f": (1, 15), "d": (1, 10), "s": (2, 20), "c": (2, 20),
}
START_SCORE = 20


def score(chosen):
    return START_SCORE + sum(value if name in chosen else -value for name, (_, value) in ITEMS.items())


def solutions(capacity):
    names = list(ITEMS)
    result = []
    for count in range(1, len(names) + 1):
        for group in combinations(names, count):
            if "i" not in group or sum(ITEMS[name][0] for name in group) > capacity:
                continue
            points = score(group)
            if points > 0:
                result.append((points, group))
    return sorted(result, key=lambda item: (-item[0], item[1]))


def inventory(group):
    cells = [name for name in group for _ in range(ITEMS[name][0])]
    cells.extend("·" for _ in range(8 - len(cells)))
    for position in range(0, 8, 4):
        print(" ".join(f"[{name}]" for name in cells[position:position + 4]))


def main():
    valid = solutions(8)
    print("Вариант 5: 2×4, астма, стартовые очки 20")
    if valid:
        points, chosen = valid[0]
        print("Лучшее решение:", ", ".join(chosen))
        inventory(chosen)
        print("Итоговые очки выживания:", points)
    print(f"Все допустимые комбинации ({len(valid)}):")
    for points, chosen in valid:
        print(f"{''.join(chosen):12} {points:>3}")
    smaller = solutions(7)
    print(f"Семь ячеек: {len(smaller)} решений с положительным счётом")
    if smaller:
        print("Пример:", "".join(smaller[0][1]), "—", smaller[0][0], "очков")
    else:
        print("Все подмножества проверены; решения нет.")


if __name__ == "__main__":
    main()
