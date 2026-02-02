from model.draw import values

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from dealerhand import Hand


def update_total(cards: list[str]):
    if "A" in cards:
        # There can only be one soft Ace in the hand
        # Since two soft Aces add to 22 and bust
        n_aces = cards.count("A")
        sum_not_aces = sum([values[card] for card in cards if card != "A"])
        return (n_aces + sum_not_aces, 10 + n_aces + sum_not_aces)

    return sum([values[card] for card in cards])


def _get_total(hand: "Hand"):
    if "A" in hand.cards:
        hard_total = hand.value[0]
        soft_total = hand.value[1]
        return hard_total * (soft_total > 21) + soft_total * (soft_total <= 21)
    else:
        return hand.value
