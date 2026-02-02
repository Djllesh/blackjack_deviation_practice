from model.player import Player
from model.dealer import DealerHand
from model.rules import Rules


class AppController:
    def __init__(
        self,
        *,
        rules: Rules = None,
        player: Player = None,
        dealer: DealerHand = None,
    ):
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

        self.state = {
            "dealer_hand_str": f"Dealer {self.dealer.cards}",
            "player_hand_str": f"Player {self.player.show_hands()}",
            "result_str": "",
            "wpl_str": "W/P/L\n0/0/0",
            "round_finished": False,
            "buttons_enabled": True,
        }

    def get_state(self):
        return self.state

    def set_state_stand(self):
        self.state["dealer_hand_str"] = f"Dealer {self.dealer.cards}"
        self.state["result_str"] = f"""
            Previous: Player {self.player.get_totals()} vs Dealer {
            self.dealer.get_total()
        }
            """
        self.state["wpl_str"] = (
            f"W/P/L\n{self.player.wins}/{self.player.pushes}/{self.player.losses}"
        )
        self.state["round_finished"] = True
        self.state["buttons_enabled"] = False

    def set_state_player(self):
        self.state["player_hand_str"] = f"Player {self.player.show_hands()}"

    def stand(self):
        if self.player.can_finish():
            self.dealer.finish()
            self.player.resolve(self.dealer)
            self.set_state_stand()
        else:
            self.player.next()

    def hit(self):
        self.player.active_hand().hit()
        self.set_state_player()
        if self.player.active_hand().is_busted():
            self.stand()

    def double(self):
        self.player.active_hand().hit()
        self.set_state_player()
        self.stand()

    def split(self):
        self.player.split()
        self.set_state_player()

    def surrender(self):
        if self.player.active_hand().is_hit or not self.rules.surrender:
            return
        self.stand()

    def reset(self):
        self.player.reset()
        self.dealer.reset()
        self.state["player_hand_str"] = f"Player {self.player.show_hands()}"
        self.state["dealer_hand_str"] = f"Dealer {self.dealer.cards}"
        self.state["buttons_enabled"] = True
        self.state["round_finished"] = False
