import tkinter as tk


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
        play_button = tk.Button(
            self, text="Play", command=lambda: self.app.show_frame("PlayFrame")
        )
        table_button = tk.Button(
            self,
            text="Table",
            command=lambda: self.app.show_frame("TableFrame"),
        )
        stats_button = tk.Button(
            self,
            text="Stats",
            command=lambda: self.app.show_frame("StatsFrame"),
        )
        play_button.grid(row=0, column=0, sticky="nsew")
        table_button.grid(row=0, column=1, sticky="nsew")
        stats_button.grid(row=0, column=2, sticky="nsew")
