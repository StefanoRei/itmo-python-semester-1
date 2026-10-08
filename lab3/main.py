import re
import tkinter as tk
from tkinter import ttk


ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def shift(block, distance):
    return "".join(ALPHABET[(ALPHABET.index(char) + distance) % len(ALPHABET)] for char in block)


def make_key(block):
    block = block.strip().upper()
    if not re.fullmatch(r"[A-Z0-9]{5}", block):
        raise ValueError("Введите ровно пять латинских букв или цифр")
    return f"{block}-{shift(block, 3)}-{shift(block, -5)}"


def main():
    window = tk.Tk()
    window.title("Arcade Keygen · вариант 5")
    window.geometry("620x360")
    window.resizable(False, False)
    canvas = tk.Canvas(window, bg="#101426", highlightthickness=0)
    canvas.place(relwidth=1, relheight=1)
    for row in range(9):
        for col in range(14):
            if (row + col * 3) % 7 == 0:
                canvas.create_rectangle(24 + col * 42, 20 + row * 37, 27 + col * 42, 23 + row * 37, fill="#9ceaff", outline="")
    alien = ("  ███  ", " █████ ", "██ █ ██", "███████", "█ ███ █", "█     █")
    for y, line in enumerate(alien):
        for x, char in enumerate(line):
            if char == "█":
                canvas.create_rectangle(410 + x * 20, 114 + y * 20, 428 + x * 20, 132 + y * 20, fill="#73f5a8", outline="")
    panel = ttk.Frame(window, padding=18)
    panel.place(x=28, y=72)
    ttk.Label(panel, text="SPACE ARCADE", font=("TkDefaultFont", 18, "bold")).pack(anchor="w")
    ttk.Label(panel, text="Первый блок (5 символов A–Z, 0–9)").pack(anchor="w", pady=(12, 2))
    first = ttk.Entry(panel, width=28)
    first.pack(anchor="w")
    result = tk.StringVar()
    status = tk.StringVar()

    def generate():
        try:
            result.set(make_key(first.get()))
            status.set("")
        except ValueError as error:
            result.set("")
            status.set(str(error))

    ttk.Button(panel, text="Сгенерировать", command=generate).pack(anchor="w", pady=12)
    ttk.Entry(panel, textvariable=result, state="readonly", width=28).pack(anchor="w")
    ttk.Label(panel, textvariable=status, foreground="#b92338").pack(anchor="w")
    window.mainloop()


if __name__ == "__main__":
    main()
