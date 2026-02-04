import tkinter as tk
from tkinter import ttk


class TopFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent)
        self.app = app
        self.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=0, weight=1)
        self.grid_columnconfigure(index=1, weight=1)
        self.grid_columnconfigure(index=2, weight=1)

    def render_buttons(self):
        s = ttk.Style()
        s.configure("my.TButton", font=("Helvetica", 24))
        play_button = ttk.Button(
            self,
            text="Play",
            command=lambda: self.app.show_frame("PlayFrame"),
            style="my.TButton",
        )
        table_button = ttk.Button(
            self,
            text="Table",
            command=lambda: self.app.show_frame("TableFrame"),
            style="my.TButton",
        )
        stats_button = ttk.Button(
            self,
            text="Stats",
            command=lambda: self.app.show_frame("StatsFrame"),
            style="my.TButton",
        )
        play_button.grid(row=0, column=0, sticky="nsew")
        table_button.grid(row=0, column=1, sticky="nsew")
        stats_button.grid(row=0, column=2, sticky="nsew")
