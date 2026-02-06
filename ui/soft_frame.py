import tkinter as tk
from ui.table_canvas import TableCanvas

soft_totals = [
    13,
    14,
    15,
    16,
    17,
    18,
    19,
]


class SoftFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def put_canvas(self, controller):
        self.canvas = TableCanvas(
            parent=self,
            bg="white",
            rows=len(soft_totals) + 1,
            cols=11,
            controller=controller,
            player_totals=soft_totals,
        )
        self.canvas.grid(row=0, column=0, sticky="nsew")
