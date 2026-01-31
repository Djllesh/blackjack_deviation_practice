import sqlite3
from itertools import compress

from players import DealerHand, Hand, Player
from basic_strategy import Action, load_pickle
from rules import Rules

sql_command = """INSERT INTO results(
                 hand_total,
                 hand_type,
                 dealer_upcard,
                 action_played,
                 ruleset_id,
                 true_count,
                 true_action,
                 result)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""


def commit_to_db(
    conn,
    player: Player,
    action: Action,
    dealer: DealerHand,
    rules: Rules,
    true_count: int,
):
    to_commit = resolve_hand(player, action, dealer, rules, true_count)
    # cursor = conn.cursor()
    # cursor.execute(sql_command, to_commit)
    # conn.commit()


def resolve_hand(
    player: Player,
    action: Action,
    dealer: DealerHand,
    rules: Rules,
    true_count: int,
) -> tuple:
    # TODO: Actually resolve the hand!
    # 1. Check the basic strategy action
    # 1.1. If the action is two-lettered - check the legality
    # 1.2. If the action if associated with deviations - check the threshold
    # 2. Finish the dealer
    # 3. Check the result

    active_hand = player.active_hand()
    bs_key = (
        active_hand.get_total(),
        active_hand.get_hand_type(),
        dealer.get_upcard(),
        rules.ruleset_id(),
    )

    strategy = basic_strategy[bs_key]
    true_action = get_true_action(strategy, true_count)

    print("True action: ", true_action, " vs ", "Action played: ", action)

    return (
        player.active_hand().get_total(),
        player.active_hand().get_hand_type(),
        dealer.get_total(),
        action.value,
        rules.ruleset_id(),
        true_count,
        true_action.value,
        "w",
    )


def get_true_action(strategy: list[dict], true_count: int) -> Action:
    true_deviations = []
    for dev_dict in strategy:
        true_deviations.append(should_deviate(dev_dict, true_count))

    if len(true_deviations) != 0 and True in true_deviations:
        return list(compress(strategy, true_deviations))[0]["deviation"]

    return strategy[0]["base"]


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
    basic_strategy = load_pickle("data/basic_strategy.pickle")
    try:
        with sqlite3.connect("data/results.db") as conn:
            rules = Rules()
            player = Player(init_hand=Hand(cards=["6", "4"]))
            dealer_hand = DealerHand.deal_initial(card="10")
            action = Action.DOUBLE
            true_count = 3

            cursor = conn.cursor()

            cursor.execute("""CREATE TABLE IF NOT EXISTS results (
                              id INTEGER PRIMARY KEY,
                              hand_total INTEGER,
                              hand_type text,
                              dealer_upcard INTEGER,
                              action_played text,
                              ruleset_id text,
                              true_count INTEGER,
                              true_action text,
                              result text
                )""")

            commit_to_db(conn, player, action, dealer_hand, rules, true_count)

    except sqlite3.OperationalError as e:
        print("Falied to open a database: ", e)
