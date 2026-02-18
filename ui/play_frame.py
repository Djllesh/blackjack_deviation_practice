import tkinter as tk
import random
from tkinter import ttk, StringVar
from controller.controller import AppController
from collections import defaultdict
from PIL import ImageTk, Image


class PlayFrame(tk.Frame):
    def __init__(
        self,
        parent,
        controller: AppController,
        images: defaultdict[str, list[Image]],
    ):
        super().__init__(parent)
        self.controller = controller
        self.images = images

        self.player_hand_str = StringVar()
        self.dealer_hand_str = StringVar()
        self.result_str = StringVar()
        self.wpl_str = StringVar()
        self.true_count_str = StringVar()
        self.ruleset_str = StringVar()
        self.set_strings()

        s = ttk.Style()
        s.configure("my.TButton", font=("Helvetica", 18))

        self.create_player_dealer_label()
        self.create_dealer_canvas()
        self.update_dealer_canvas()
        self.create_player_canvas()
        self.update_player_canvas()

        self.create_buttons()
        self.create_bottom_labels()

    def raised(self):
        self.set_strings()

    def set_strings(self):
        state = self.controller.get_state()
        self.ruleset_str.set(self.controller.rules.ruleset_id())
        self.player_hand_str.set(state["player_hand_str"])
        self.dealer_hand_str.set(state["dealer_hand_str"])
        self.true_count_str.set(state["true_count_str"])
        self.result_str.set(state["result_str"])
        self.wpl_str.set(state["wpl_str"])

    def create_player_dealer_label(self):
        self.dealer_label = ttk.Label(
            self, textvariable=self.dealer_hand_str, font=("Helvetica", 18)
        )
        self.dealer_label.pack()
        self.player_label = ttk.Label(
            self, textvariable=self.player_hand_str, font=("Helvetica", 18)
        )
        self.player_label.pack()

    def create_dealer_canvas(self):
        default_height = self.images["Back"][0].size[1]
        self.dealer_canvas = tk.Canvas(
            self,
            width=500,
            height=default_height,
            relief="solid",
            background="#f0f0f0",
        )
        self.dealer_canvas.pack()

    def update_dealer_canvas(self):
        self.dealer_canvas.delete("all")
        self.dealer_photos = [
            ImageTk.PhotoImage(random.choice(self.images[card]))
            for card in self.controller.dealer.cards
        ]
        self.back_photo = ImageTk.PhotoImage(self.images["Back"][0])

        for num, photo in enumerate(self.dealer_photos):
            self.dealer_canvas.create_image(
                2 + 50 * num, 2, image=photo, anchor="nw"
            )

        if len(self.dealer_photos) == 1:
            self.dealer_canvas.create_image(
                50, 2, image=self.back_photo, anchor="nw"
            )

    def create_player_canvas(self):
        default_height = self.images["Back"][0].size[1]
        self.player_canvas = tk.Canvas(
            self,
            width=500,
            height=default_height,
            relief="solid",
            background="#f0f0f0",
        )
        self.player_canvas.pack()

    def update_player_canvas(self):
        self.player_canvas.delete("all")
        self.player_photos = [
            [
                ImageTk.PhotoImage(random.choice(self.images[card]))
                for card in hand.cards
            ]
            for hand in self.controller.player.hands
        ]

        number_of_pairs = len(self.player_photos)
        if number_of_pairs == 1:
            number_of_gaps = 1
        else:
            number_of_gaps = number_of_pairs * 2 - 1

        for p_num, pair in enumerate(self.player_photos):
            for idx, card in enumerate(pair):
                self.player_canvas.create_image(
                    p_num * (20 + card.width() + 50) + 50 * idx + 2,
                    2,
                    image=card,
                    anchor="nw",
                )

        self.highlight_active_hand(card.width(), card.height())

    def highlight_active_hand(self, width, height):
        if len(self.controller.player.hands) > 1:
            active_idx = self.controller.player.active
            # HACK: Hardcoded the coordinates of the active hand
            self.player_canvas.create_rectangle(
                active_idx * (20 + width + 50) + 2,
                2,
                width + active_idx * (20 + width + 50),
                2 + height,
                width=3,
            )

    def create_bottom_labels(self):
        self.true_count_label = tk.Label(
            self, textvariable=self.true_count_str, font=("Helvetica", 18)
        )
        self.true_count_label.pack()
        self.result_label = tk.Label(self, textvariable=self.result_str)
        self.result_label.pack()
        self.ruleset_label = tk.Label(self, textvariable=self.ruleset_str)
        self.ruleset_label.pack()
        self.wpl_label = tk.Label(self, textvariable=self.wpl_str)
        self.wpl_label.pack()

    def create_buttons(self):
        self.stand_button = ttk.Button(
            self,
            text="Stand",
            command=self.stand,
            style="my.TButton",
        )
        self.stand_button.pack()
        self.hit_button = ttk.Button(
            self,
            text="Hit",
            command=self.hit,
            style="my.TButton",
        )
        self.hit_button.pack()
        self.double_button = ttk.Button(
            self,
            text="Double",
            command=self.double,
            style="my.TButton",
        )
        self.double_button.pack()
        self.split_button = ttk.Button(
            self,
            text="Split",
            command=self.split,
            style="my.TButton",
        )
        self.split_button.pack()
        self.surrender_button = ttk.Button(
            self,
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
        self.update_dealer_canvas()
        self.disable_all_buttons()
        self.set_strings()
        self.after(2000, self._after_pause)

    def _after_pause(self):
        self.controller.reset()
        self.set_strings()
        self.enable_all_buttons()
        self.update_dealer_canvas()
        self.update_player_canvas()

    def stand(self):
        self.controller.stand()
        # update in case of the split standing
        self.update_player_canvas()
        round_finished = self.controller.round_finished
        if round_finished:
            self.finish_round()

    def hit(self):
        self.controller.hit()
        self.set_strings()
        self.update_player_canvas()
        round_finished = self.controller.round_finished
        if round_finished:
            self.finish_round()

    def double(self):
        self.controller.double()
        self.set_strings()
        self.update_player_canvas()
        round_finished = self.controller.round_finished
        if round_finished:
            self.finish_round()

    def split(self):
        self.controller.split()
        self.update_player_canvas()
        self.set_strings()

    def surrender(self):
        self.controller.surrender()
        round_finished = self.controller.round_finished
        if round_finished:
            self.finish_round()
