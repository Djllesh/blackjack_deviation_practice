import sqlite3
from itertools import compress
from pathlib import Path

from model.player import Player
from model.dealer import DealerHand
from model.rules import Rules
from strategy.action import Action
from strategy.loader import load_pickle
from collections import defaultdict

PICKLE_PATH = Path("data/basic_strategy.pickle")


def resolve_hand(
    basic_strategy: defaultdict,
    player: Player,
    action: Action,
    dealer: DealerHand,
    rules: Rules,
    true_count: int,
) -> tuple:
    bs_key = generate_key(player, dealer, rules)

    true_action, action_source = get_true_action(
        basic_strategy[bs_key], true_count
    )

    true_action = get_legal_action(
        true_action,
        rules,
        player.active_hand().is_hit,
    )
    print(f"True action: {true_action}")

    return (
        player.active_hand().get_total(),
        player.active_hand().get_hand_type(),
        dealer.get_total(),
        action.value,
        rules.ruleset_id(),
        true_count,
        true_action.value,
        action_source,
    )


def generate_key(player: Player, dealer: DealerHand, rules: Rules):
    return (
        player.active_hand().get_total(),
        player.active_hand().get_hand_type(),
        dealer.get_total(),
        rules.ruleset_id(),
    )


def get_true_action(strategy: list[dict], true_count: int) -> tuple:
    true_deviations = []
    for dev_dict in strategy:
        true_deviations.append(should_deviate(dev_dict, true_count))

    # If at least one of the deviations passes
    if len(true_deviations) != 0 and True in true_deviations:
        return (
            list(compress(strategy, true_deviations))[0]["deviation"],
            "deviation",
        )

    # Otherwise a base action
    return (strategy[0]["base"], "base")


def get_legal_action(
    true_action: Action, rules: Rules, was_hit: bool
) -> Action:
    """Asserts the legality of the action if it happens to be
    two-lettered or surrendering is not allowed
    """

    if true_action == Action.DOUBLE_STAND and was_hit:
        true_action = Action.STAND
    elif true_action == Action.DOUBLE_STAND and not was_hit:
        true_action = Action.DOUBLE
    elif true_action == Action.DOUBLE and was_hit:
        true_action = Action.HIT
    elif (
        true_action == Action.SURRENDER_STAND
        and not was_hit
        and rules.surrender
    ):
        true_action = Action.SURRENDER
    elif true_action == Action.SURRENDER_STAND and (
        was_hit or not rules.surrender
    ):
        true_action = Action.STAND
    elif true_action == Action.SURRENDER_SPLIT and rules.surrender:
        true_action = Action.SURRENDER
    elif true_action == Action.SURRENDER_SPLIT and not rules.surrender:
        true_action = Action.SPLIT
    elif true_action == Action.SURRENDER and (not rules.surrender or was_hit):
        true_action = Action.HIT
    return true_action


def should_deviate(dev_dict: dict, true_count: int):
    if dev_dict["comparison"] == ">":
        return true_count > dev_dict["index"]
    elif dev_dict["comparison"] == ">=":
        return true_count >= dev_dict["index"]
    elif dev_dict["comparison"] == "<":
        return true_count < dev_dict["index"]
    elif dev_dict["comparison"] == "<=":
        return true_count <= dev_dict["index"]


if __name__ == "__main__":
    basic_strategy = load_pickle(PICKLE_PATH)
    try:
        with sqlite3.connect("data/results.db") as conn:
            pass
            # rules = Rules()
            # player = Player(init_hand=Hand(cards=["J", "6"]))
            # # player.active_hand().hit(card="2")
            # dealer_hand = DealerHand.deal_initial(card="A")
            # action = Action.DOUBLE
            # true_count = 1
            #
            # cursor = conn.cursor()
            #
            # cursor.execute("""CREATE TABLE IF NOT EXISTS results (
            #                   id INTEGER PRIMARY KEY,
            #                   hand_total INTEGER,
            #                   hand_type text,
            #                   dealer_upcard INTEGER,
            #                   action_played text,
            #                   ruleset_id text,
            #                   true_count INTEGER,
            #                   true_action text,
            #                   result text
            #     )""")

    except sqlite3.OperationalError as e:
        print("Falied to open a database: ", e)
