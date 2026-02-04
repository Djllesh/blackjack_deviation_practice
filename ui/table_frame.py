import tkinter as tk
from tkinter import ttk, StringVar
from ui.hard_frame import HardFrame
from ui.soft_frame import SoftFrame
from ui.pair_frame import PairFrame
from controller.controller import AppController


def make_ruleset_from_strings(
    soft17: str, das: str, decks: str, peek: str
) -> str:
    if soft17 == "Dealer hits on soft 17":
        _soft = "H17"
    elif soft17 == "Dealer stands on soft 17":
        _soft = "S17"
    else:
        raise ValueError(f"Unknown value of soft17 string: {soft17}")

    if das == "Double after split allowed":
        _das = "DAS"
    elif das == "Double after split not allowed":
        _das = "noDAS"
    else:
        raise ValueError(f"Unknown value of das string: {das}")

    if decks == "2":
        _decks = 2
    elif decks == "4":
        _decks = 4
    else:
        raise ValueError(f"Unknown value of decks string: {decks}")

    if peek == "Dealer peeks":
        _peek = "peek"
    elif peek == "No peek":
        _peek = "nopeek"
    else:
        raise ValueError(f"Unknown value of peek string: {peek}")

    return f"{_soft}_{decks}_{_das}_{_peek}"


class TableFrame(tk.Frame):
    def __init__(self, parent, controller: AppController):
        super().__init__(parent, padx=60, pady=20)
        self.controller = controller
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.inner_frame = tk.Frame(self)
        self.inner_frame.grid(row=0, column=0, sticky="nsew")
        self.inner_frame.grid_rowconfigure(0, weight=1)
        self.inner_frame.grid_rowconfigure(1, weight=10)
        self.inner_frame.grid_rowconfigure(2, weight=7)
        self.inner_frame.grid_rowconfigure(3, weight=7)
        self.inner_frame.grid_columnconfigure(0, weight=1)

        self.combobox_frame = tk.Frame(self.inner_frame)
        self.combobox_frame.grid(row=0, column=0)
        self.comboboxes()

        self.configure_inner_frame()

    def configure_inner_frame(self):
        self.frames = {}
        for F, idx in zip((HardFrame, SoftFrame, PairFrame), range(3)):
            frame = F(self.inner_frame)
            name = F.__name__
            frame.grid(row=idx + 1, column=0, sticky="nsew")
            self.frames[name] = frame

    def comboboxes(self):
        self.combobox_frame.grid_rowconfigure(0, weight=1)
        self.combobox_frame.grid_columnconfigure(0, weight=1)
        self.combobox_frame.grid_columnconfigure(1, weight=1)
        self.combobox_frame.grid_columnconfigure(2, weight=1)
        self.combobox_frame.grid_columnconfigure(3, weight=1)

        self.soft17_str = StringVar()
        self.soft17_cb = ttk.Combobox(
            self.combobox_frame, textvariable=self.soft17_str
        )
        self.soft17_cb["values"] = [
            "Dealer hits on soft 17",
            "Dealer stands on soft 17",
        ]
        self.soft17_cb.current(0)
        self.soft17_cb.grid(row=0, column=0, sticky="nsew")
        self.soft17_cb.bind("<<ComboboxSelected>>", self.update_rules)

        self.decks_str = StringVar()
        self.decks_cb = ttk.Combobox(
            self.combobox_frame, textvariable=self.decks_str
        )
        self.decks_cb["values"] = [
            "4",
            "2",
        ]
        self.decks_cb.current(0)
        self.decks_cb.grid(row=0, column=1, sticky="nsew")
        self.decks_cb.bind("<<ComboboxSelected>>", self.update_rules)

        self.das_str = StringVar()
        self.das_cb = ttk.Combobox(
            self.combobox_frame, textvariable=self.das_str
        )
        self.das_cb["values"] = [
            "Double after split allowed",
            "Double after split not allowed",
        ]
        self.das_cb.current(0)
        self.das_cb.bind("<<ComboboxSelected>>", self.update_rules)

        self.das_cb.grid(row=0, column=2, sticky="nsew")

        self.peek_str = StringVar()
        self.peek_cb = ttk.Combobox(
            self.combobox_frame, textvariable=self.peek_str
        )
        self.peek_cb["values"] = [
            "Dealer peeks",
            "No peek",
        ]
        self.peek_cb.current(0)
        self.peek_cb.grid(row=0, column=3, sticky="nsew")
        self.peek_cb.bind("<<ComboboxSelected>>", self.update_rules)

    def update_rules(self, event):
        ruleset = make_ruleset_from_strings(
            soft17=self.soft17_str.get(),
            das=self.das_str.get(),
            decks=self.decks_str.get(),
            peek=self.peek_str.get(),
        )
        self.controller.update_rules(ruleset)
        for _, frame in self.frames.items():
            frame.canvas.make_grid(event)

    def raised(self):
        for _, frame in self.frames.items():
            frame.put_canvas(self.controller)
