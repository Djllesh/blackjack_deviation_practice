import tkinter as tk
from ui.table_canvas import TableCanvas

pair_totals = [
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
]


class PairFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def put_canvas(self, controller):
        self.canvas = TableCanvas(
            parent=self,
            bg="white",
            rows=11,
            cols=11,
            controller=controller,
            player_totals=pair_totals,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
