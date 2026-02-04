import tkinter as tk
from controller.controller import AppController
from strategy.action import Action


dealer_upcards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11]


def get_hand_type(parent):
    if "Hard" in parent.__class__.__name__:
        return "hard"
    elif "Soft" in parent.__class__.__name__:
        return "soft"
    elif "Pair" in parent.__class__.__name__:
        return "pair"


def action_representation(action: Action):
    if len(action.value) == 1:
        return action.value.upper()

    if action == Action.DOUBLE_STAND:
        return "Ds"
    if action == Action.SURRENDER_STAND:
        return "Rs"
    if action == Action.SURRENDER_SPLIT:
        return "Rp"


def action_to_color(action: Action):
    if action == Action.HIT:
        return "#00b050"
    if action == Action.STAND:
        return "#ff0000"
    if action == Action.DOUBLE:
        return "#ffc000"
    if action == Action.DOUBLE_STAND:
        return "#ffd966"
    if action == Action.SURRENDER:
        return "#ffffff"
    if action == Action.SURRENDER_STAND:
        return "#ffffff"
    if action == Action.SURRENDER_SPLIT:
        return "#ffffff"
    if action == Action.SPLIT:
        return "#0070c0"


def get_base_action(
    basic_strategy,
    *,
    dealer_upcard: int,
    player_total: int,
    hand_type: str,
    ruleset: str,
):
    if hand_type == "pair":
        key = (player_total * 2, hand_type, dealer_upcard, ruleset)
    else:
        key = (player_total, hand_type, dealer_upcard, ruleset)
    strategy_row = basic_strategy[key]
    return strategy_row[0]["base"]


def convert_comp_to_sign(comp: str) -> str:
    if comp == ">=" or comp == ">":
        return "+"
    elif comp == "<=" or comp == "<":
        return "-"
    else:
        raise ValueError(f"Unknown comparison {comp}")


def get_deviations(
    basic_strategy,
    *,
    dealer_upcard: int,
    player_total: int,
    hand_type: str,
    ruleset: str,
) -> tuple:
    if hand_type == "pair":
        key = (player_total * 2, hand_type, dealer_upcard, ruleset)
    else:
        key = (player_total, hand_type, dealer_upcard, ruleset)
    strategy_row = basic_strategy[key]
    if strategy_row[0]["deviation"]:
        deviations = []
        colors = []
        for row in strategy_row:
            deviations.append(
                str(int(row["index"])) + convert_comp_to_sign(row["comparison"])
            )
            colors.append(action_to_color(row["deviation"]))
        return (deviations, colors)

    else:
        return (None, None)


class TableCanvas(tk.Canvas):
    def __init__(
        self,
        *,
        parent,
        controller: AppController,
        bg,
        rows,
        cols,
        player_totals,
    ):
        self.hand_type = get_hand_type(parent)
        self.parent = parent
        self.controller = controller
        self.player_totals = player_totals
        super().__init__(
            parent,
            width=self.parent.winfo_width(),
            height=self.parent.winfo_height(),
            bg=bg,
            bd=0,
        )
        self.rows = rows
        self.cols = cols
        self.make_grid(None)
        self.bind("<Configure>", self.make_grid)

    def make_grid(self, event):
        self.delete("all")
        rectangle_width = self.parent.winfo_width() / self.cols
        rectangle_height = self.parent.winfo_height() / self.rows
        # number of rows is number of hard totals + 1
        for row in range(self.rows):
            # number of cols is number of dealer upcards + 1
            for col in range(self.cols):
                if row == 0 and col >= 1:
                    self.create_text(
                        col * rectangle_width + rectangle_width / 2,
                        rectangle_height / 2,
                        text=str(dealer_upcards[col - 1]),
                        font=("Helvetica", 8),
                    )
                    self.create_rectangle(
                        col * rectangle_width,
                        row * rectangle_height,
                        (col + 1) * rectangle_width,
                        (row + 1) * rectangle_height,
                    )

                if col == 0 and row >= 1:
                    self.create_text(
                        rectangle_width / 2,
                        row * rectangle_height + rectangle_height / 2,
                        text=str(self.player_totals[row - 1]),
                        font=("Helvetica", 8),
                    )
                    self.create_rectangle(
                        col * rectangle_width,
                        row * rectangle_height,
                        (col + 1) * rectangle_width,
                        (row + 1) * rectangle_height,
                    )

                if col >= 1 and row >= 1:
                    hand_type = get_hand_type(self.parent)
                    base_action = get_base_action(
                        self.controller.basic_strategy,
                        dealer_upcard=dealer_upcards[col - 1],
                        player_total=self.player_totals[row - 1],
                        hand_type=hand_type,
                        ruleset=self.controller.rules.ruleset_id(),
                    )
                    action_str = action_representation(base_action)
                    color = action_to_color(base_action)
                    deviations, dev_colors = get_deviations(
                        self.controller.basic_strategy,
                        dealer_upcard=dealer_upcards[col - 1],
                        player_total=self.player_totals[row - 1],
                        hand_type=hand_type,
                        ruleset=self.controller.rules.ruleset_id(),
                    )
                    self.create_rectangle(
                        col * rectangle_width,
                        row * rectangle_height,
                        (col + 1) * rectangle_width,
                        (row + 1) * rectangle_height,
                        fill=color,
                        width=0,
                    )
                    if deviations is not None:
                        for idx, (dev, dev_col) in enumerate(
                            zip(deviations, dev_colors)
                        ):
                            self.create_text(
                                col * rectangle_width
                                + (idx + 1)
                                * rectangle_width
                                / (len(deviations) + 1),
                                row * rectangle_height + rectangle_height / 2,
                                text=dev,
                                font=("Helvetica", 8, "bold"),
                                fill=dev_col,
                            )
                    else:
                        self.create_text(
                            col * rectangle_width + rectangle_width / 2,
                            row * rectangle_height + rectangle_height / 2,
                            text=action_str,
                            font=("Helvetica", 8, "bold"),
                        )
