import tkinter as tk
from ui.play_frame import PlayFrame
from ui.table_frame import TableFrame
from ui.stats_frame import StatsFrame
from ui.top_frame import TopFrame
from controller.controller import AppController


class App(tk.Tk):
    def __init__(self, controller: AppController):
        super().__init__()
        self.title("Blackjack Deviation Practice")
        self.geometry("800x600")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_rowconfigure(1, weight=100)
        self.container.grid_columnconfigure(0, weight=1)
        top_frame = TopFrame(self.container, self)
        top_frame.grid(row=0, column=0, sticky="nsew")
        top_frame.render_buttons()

        self.frames = {}
        for F in (PlayFrame, TableFrame, StatsFrame):
            frame_name = F.__name__
            frame = F(self.container, controller)
            self.frames[frame_name] = frame
            frame.grid(row=1, column=0, sticky="nsew")
        self.show_frame("PlayFrame")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
