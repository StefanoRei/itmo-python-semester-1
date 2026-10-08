from pathlib import Path
from statistics import mean
import argparse
import sys
import time


DATA = Path(__file__).with_name("sequence.txt")


def flag():
    print("Флаг Литвы")
    for color in (43, 42, 41):
        print(f"\033[{color}m{' ' * 32}\033[0m" * 3)


def pattern():
    print("Узор e")
    for _ in range(2):
        for row in ("╲    ╱", " ╲  ╱ ", "  ╲╱  "):
            print((row + "  ") * 5)


def diagram():
    values = [float(line) for line in DATA.read_text().splitlines() if line.strip()]
    even = mean(abs(value) for value in values[1::2])
    odd = mean(abs(value) for value in values[::2])
    total = even + odd
    print("Среднее |x| по позициям")
    for name, value in (("чётные", even), ("нечётные", odd)):
        share = value / total * 100
        print(f"{name:9} {share:5.1f}% {'█' * round(share / 2)}")


def graph():
    height = 10
    print("Первая четверть графика y = |x| (x ≥ 0, y ≥ 0)")
    sys.stdout.write("\033[s")
    for x in range(height):
        sys.stdout.write(f"\033[{height - x}B\033[{2 * x + 3}C●\033[u")
    sys.stdout.write("\n" * (height + 1))
    sys.stdout.flush()


def animation():
    for position in (0, 5, 10, 15):
        sys.stdout.write("\033[2J\033[H")
        sys.stdout.write("\033[4;1H" + " " * position + "◆ →")
        sys.stdout.flush()
        time.sleep(0.2)
    sys.stdout.write("\033[2J\033[H")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--animate", action="store_true", help="показать анимацию из четырёх кадров")
    args = parser.parse_args()
    if args.animate:
        animation()
    flag()
    pattern()
    diagram()
    if sys.stdout.isatty():
        graph()
