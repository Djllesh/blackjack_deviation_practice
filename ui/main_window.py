import tkinter as tk
from tkinter import ttk, StringVar
from controller.controller import AppController


class MainWindow:
    def __init__(self, root, controller: AppController):
        self.root = root
        self.controller = controller
        self.player_hand_str = StringVar()
        self.dealer_hand_str = StringVar()
        self.result_str = StringVar()
        self.wpl_str = StringVar()
        self.set_strings()
        s = ttk.Style()
        s.configure("my.TButton", font=("Helvetica", 18))
        self.create_player_dealer_label()
        self.create_buttons()
        self.create_bottom_labels()

    def set_strings(self):
        state = self.controller.get_state()
        self.player_hand_str.set(state["player_hand_str"])
        self.dealer_hand_str.set(state["dealer_hand_str"])
        self.result_str.set(state["result_str"])
        self.wpl_str.set(state["wpl_str"])

    def create_player_dealer_label(self):
        self.dealer_label = ttk.Label(
            self.root, textvariable=self.dealer_hand_str, font=("Helvetica", 18)
        )
        self.dealer_label.pack()
        self.player_label = ttk.Label(
            self.root, textvariable=self.player_hand_str, font=("Helvetica", 18)
        )
        self.player_label.pack()

    def create_bottom_labels(self):
        self.result_label = tk.Label(self.root, textvariable=self.result_str)
        self.result_label.pack()
        self.wpl_label = tk.Label(self.root, textvariable=self.wpl_str)
        self.wpl_label.pack()

    def create_buttons(self):
        self.stand_button = ttk.Button(
            self.root,
            text="Stand",
            command=self.stand,
            style="my.TButton",
        )
        self.stand_button.pack()
        self.hit_button = ttk.Button(
            self.root,
            text="Hit",
            command=self.hit,
            style="my.TButton",
        )
        self.hit_button.pack()
        self.double_button = ttk.Button(
            self.root,
            text="Double",
            command=self.double,
            style="my.TButton",
        )
        self.double_button.pack()
        self.split_button = ttk.Button(
            self.root,
            text="Split",
            command=self.split,
            style="my.TButton",
        )
        self.split_button.pack()
        self.surrender_button = ttk.Button(
            self.root,
            text="Surrender",
            command=self.surrender,
            style="my.TButton",
        )
        self.surrender_button.pack()

    def disable_all_buttons(self):
        self.hit_button.config(state=tk.DISABLED)
        self.stand_button.config(state=tk.DISABLED)
        self.double_button.config(state=tk.DISABLED)
        self.surrender_button.config(state=tk.DISABLED)
        self.split_button.config(state=tk.DISABLED)

    def enable_all_buttons(self):
        self.hit_button.config(state=tk.NORMAL)
        self.stand_button.config(state=tk.NORMAL)
        self.double_button.config(state=tk.NORMAL)
        self.surrender_button.config(state=tk.NORMAL)
        self.split_button.config(state=tk.NORMAL)

    def finish_round(self):
        self.disable_all_buttons()
        self.set_strings()
        self.root.after(2000, self._after_pause)

    def _after_pause(self):
        self.controller.reset()
        self.set_strings()
        self.enable_all_buttons()

    def stand(self):
        self.controller.stand()
        round_finished = self.controller.get_state()["round_finished"]
        if round_finished:
            self.finish_round()

    def hit(self):
        self.controller.hit()
        self.set_strings()
        round_finished = self.controller.get_state()["round_finished"]
        if round_finished:
            self.finish_round()

    def double(self):
        self.controller.hit()
        self.set_strings()
        self.stand()

    def split(self):
        self.controller.split()
        self.set_strings()

    def surrender(self):
        self.controller.surrender()
        round_finished = self.controller.get_state()["round_finished"]
        if round_finished:
            self.finish_round()
