import random
from collections import defaultdict
from model.dealer import DealerHand
from model.player import Player
from model.rules import Rules
from stats.database_handle import resolve_hand
from strategy.action import Action
from stats.result_logger import ResultLogger


class AppController:
    def __init__(
        self,
        basic_strategy: defaultdict,
        logger: ResultLogger,
        *,
        rules: Rules = None,
        player: Player = None,
        dealer: DealerHand = None,
        true_count: int = None,
    ):
        self.logger = logger
        self.basic_strategy = basic_strategy
        self.true_count = true_count
        if rules is not None:
            self.rules = rules
        else:
            self.rules = Rules()

        if player is not None:
            self.player = player
        else:
            self.player = Player()

        if dealer is not None:
            self.dealer = dealer
        else:
            self.dealer = DealerHand.deal_initial(rule=self.rules.soft17)

        self.begin_round()
        self.state = {
            "dealer_hand_str": f"Dealer {self.dealer.cards}",
            "player_hand_str": f"Player {self.player.show_hands()}",
            "result_str": "",
            "wpl_str": "W/P/L\n0/0/0",
            "true_count_str": f"True count: {self.true_count}",
        }

    def get_state(self):
        return self.state

    def update_rules(self, ruleset: str):
        self.rules = Rules.from_ruleset(ruleset)

    def begin_round(self):
        self.logger.begin_round()
        self.round_finished = False
        if self.true_count is None:
            self.true_count = random.randint(-3, 6)

    def attempt_finish_round(self):
        if self.player.can_finish():
            self.dealer.finish()
            self.player.resolve(self.dealer)
            self.set_state_players()
            self.set_state_result()
            self.logger.commit()
            self.round_finished = True
        else:
            self.set_state_players()
            self.player.next()

    def set_state_players(self):
        self.state["dealer_hand_str"] = f"Dealer {self.dealer.cards}"
        self.state["player_hand_str"] = f"Player {self.player.show_hands()}"

    def set_state_result(self):
        self.state["result_str"] = f"""
            Previous: Player {self.player.get_totals()} vs Dealer {
            self.dealer.get_total()
        }
            """
        self.state["wpl_str"] = (
            f"W/P/L\n{self.player.wins}/{self.player.pushes}/{self.player.losses}"
        )

    def stand(self):
        result = self.resolve_hand(Action.STAND)
        print(result)
        self.logger.log_result(result)
        self.attempt_finish_round()

    def resolve_hand(self, action: Action) -> tuple:
        return resolve_hand(
            self.basic_strategy,
            self.player,
            action,
            self.dealer,
            self.rules,
            self.true_count,
        )

    def hit(self):
        result = self.resolve_hand(Action.HIT)
        print(result)
        self.logger.log_result(result)

        can_hit = not self.player.active_hand().is_busted()
        if can_hit:
            self.player.active_hand().hit()
        if self.player.active_hand().is_busted():
            self.attempt_finish_round()
        else:
            self.set_state_players()

    def double(self):
        result = self.resolve_hand(Action.DOUBLE)
        print(result)
        self.logger.log_result(result)

        if self.player.active_hand().is_hit:
            return

        can_hit = not self.player.active_hand().is_busted()
        if can_hit:
            self.player.active_hand().hit()

        self.attempt_finish_round()

    def split(self):
        result = self.resolve_hand(Action.SPLIT)
        print(result)
        self.logger.log_result(result)

        can_split = self.player.can_split()
        if can_split:
            self.player.split()
        self.set_state_players()

    def surrender(self):
        result = self.resolve_hand(Action.SURRENDER)
        print(result)
        self.logger.log_result(result)
        if self.player.active_hand().is_hit or not self.rules.surrender:
            return
        self.attempt_finish_round()

    def reset(self):
        self.player.reset()
        self.dealer.reset()
        self.true_count = random.randint(-3, 6)
        self.state["true_count_str"] = f"True count: {self.true_count}"
        self.set_state_players()
        self.state["buttons_enabled"] = True
        self.begin_round()
