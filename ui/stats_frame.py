import tkinter as tk
from tkinter import ttk
from tkinter import StringVar


class StatsFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.selected_hand_str = StringVar()
        self.selected_hand_str.set(self.controller.state["selected_hand"])
        self.selected_hand = tk.Label(
            self, textvariable=self.selected_hand_str, font=("Helvetica", 18)
        )
        self.table_frame = tk.Frame(self)
        self.table = ttk.Treeview(self.table_frame)
        self.table["columns"] = (
            "Action Played",
            "True Count",
            "True Action",
            "True Action Source",
        )

        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.heading("#0", text="", anchor=tk.W)

        for column in self.table["columns"]:
            self.table.column(column, width=150, anchor=tk.W)
            self.table.heading(column, text=column, anchor=tk.W)

        self.table.tag_configure("correct", background="#59a551")
        self.table.tag_configure("incorrect", background="#cc4d3f")

        self.scrollbar = tk.Scrollbar(self.table_frame)
        self.scrollbar.config(command=self.table.yview)

        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.selected_hand.pack()
        self.table.pack()
        self.table_frame.pack()

    def raised(self, plays: list[tuple] = None):
        self.selected_hand_str.set(self.controller.state["selected_hand"])
        self.table.delete(*self.table.get_children())
        if plays is None:
            return
        for play in plays:
            if play[0] == play[2]:
                self.table.insert(
                    parent="", index="end", values=play, tags=("correct")
                )
            else:
                self.table.insert(
                    parent="", index="end", values=play, tags=("incorrect")
                )
