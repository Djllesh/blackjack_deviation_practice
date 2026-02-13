from typing import TYPE_CHECKING
from model.draw import draw_random
from model.total import update_total, _get_total

if TYPE_CHECKING:
    from model.dealerhand import DealerHand


class Hand:
    def __init__(self, cards: list[str]):
        self.cards: list[str] = cards
        self.is_hit: bool = False
        self.recompute()

    def recompute(self):
        self.value = update_total(self.cards)
        self.total = _get_total(self)
        self.busted = False

    @classmethod
    def deal_initial(cls):
        cards = draw_random(2)
        return cls(cards)

    def bust_update(self):
        if self.total > 21:
            self.busted = True

    def is_busted(self):
        return self.busted

    def get_total(self):
        return self.total

    def get_hand_type(self):
        if len(self.cards) == 2 and self.cards[0] == self.cards[1]:
            return "pair"

        is_ace_in_hand = isinstance(self.value, tuple)
        if not is_ace_in_hand:
            return "hard"

        soft_total = self.value[1]
        if soft_total <= 21:
            return "soft"
        else:
            return "hard"

    def hit(self, card: str = None, on_split=False):
        if not on_split:
            self.is_hit = True
        # Can only hit if not busted and can only be busted if hit
        if self.busted:
            return

        if card is not None:
            new_card = card
        else:
            new_card = draw_random(1)[0]
        self.cards.append(new_card)
        self.value = update_total(self.cards)
        self.total = _get_total(self)
        self.bust_update()

    def resolve(self, dealer):
        if not dealer.finished:
            return None

        is_win = win(self, dealer)
        is_push = push(self, dealer)
        if is_win:
            return "w"
        elif is_push:
            return "p"
        else:
            return "l"


def win(player_hand: Hand, dealer_hand: "DealerHand"):
    return (
        player_hand.get_total() > dealer_hand.get_total()
        and not player_hand.is_busted()
    ) or (not player_hand.is_busted() and dealer_hand.is_busted())


def push(player_hand: Hand, dealer_hand: "DealerHand"):
    return player_hand.get_total() == dealer_hand.get_total() and (
        not player_hand.is_busted() and not dealer_hand.is_busted()
    )
