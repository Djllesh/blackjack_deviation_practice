import tkinter as tk
from pathlib import Path

from controller.controller import AppController
from stats.open_results import open_results_db
from stats.result_logger import ResultLogger
from stats.fetch_results import ResultFetcher
from strategy.action import Action  # noqa: F401
from strategy.loader import load_pickle
from strategy.basic_strategy import generate_dict
from ui.app import App
from ui.assets.load_images import load_images

from model.player import Player
from model.hand import Hand
from model.dealer import DealerHand
from model.rules import Rules

BASIC_STRATEGY_PATH = Path("data/basic_strategy.pickle")

if __name__ == "__main__":
    # generate_dict()
    player = Player(init_hand=Hand(cards=["8", "8"]))
    dealer = DealerHand.deal_initial(card="K")
    rules = Rules(soft17="H17", das="noDAS")
    player.split(["A", "A"])

    basic_strategy = load_pickle(BASIC_STRATEGY_PATH)
    connection = open_results_db()
    logger = ResultLogger(connection)
    fetcher = ResultFetcher(connection)

    controller = AppController(
        basic_strategy=basic_strategy,
        logger=logger,
        fetcher=fetcher,
        player=player,
        dealer=dealer,
        rules=rules,
        true_count=1,
    )
    app = App(
        controller,
        images=load_images(),
    )
    app.mainloop()
