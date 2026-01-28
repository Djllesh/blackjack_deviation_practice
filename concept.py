import random
import tkinter as tk
from tkinter import ttk, StringVar

ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
values = {
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10,
}

# TODO:
# Implement the suits
suits = []


def hand_total(cards):
    if "A" in cards:
        # There can only be one soft Ace in the hand
        # Since two soft Aces add to 22 and bust
        n_aces = cards.count("A")
        sum_not_aces = sum([values[card] for card in cards if card != "A"])
        return (n_aces + sum_not_aces, 10 + n_aces + sum_not_aces)

    return sum([values[card] for card in cards])


class Hand:
    def __init__(self):
        self.cards = [random.choice(ranks) for _ in range(2)]
        self.value = hand_total(self.cards)

    def hit(self):
        # Can only hit if not busted
        if "A" in self.cards and self.value[0] >= 21:
            return
        elif self.value >= 21:
            return

        new_card = random.choice(ranks)
        self.cards.append(new_card)
        self.value = hand_total(self.cards)

        player_hand_str.set(f"Player {self.cards}")


class Dealer:
    def __init__(self, rule="H17"):
        self.cards = [random.choice(ranks)]
        self.value = hand_total(self.cards)
        self.rule = rule

    def hit(self):
        new_card = random.choice(ranks)
        self.cards.append(new_card)
        self.value = hand_total(self.cards)

        dealer_hand_str.set(f"Dealer {self.cards}")

    def finish(self):
        self.hit()
        while self.dealer_hitting_condition(dealer_hand, self.rule):
            self.hit()

    def dealer_hitting_condition(self):
        is_ace_in_hand = isinstance(self.cards, tuple)

        if is_ace_in_hand:
            soft_total = self.value[1]
            hard_total = self.value[0]
        else:
            # HACK:
            # If no ace in the hand, there is no soft total
            soft_total = -1
            hard_total = self.value

        if self.rule == "S17":
            return not (
                (soft_total >= 17 and soft_total <= 21) or hard_total >= 17
            )
        if self.rule == "H17":
            return not (
                (soft_total > 17 and soft_total <= 21) or hard_total >= 17
            )


def hit(hand):
    # Can only hit if not busted
    if "A" in hand[0] and hand[1][0] >= 21:
        return hand
    elif hand[1] >= 21:
        return hand

    new_card = random.choice(ranks)
    new_cards = hand[0]
    new_cards.append(new_card)

    new_hand = (new_cards, hand_total(new_cards))
    player_hand_str.set(f"Player {new_cards}")
    return new_hand


def stand():
    pass


def double():
    pass


def split():
    pass


def surrender():
    pass


if __name__ == "__main__":
    root = tk.Tk()

    player_hand = Hand()
    dealer_hand = Dealer()

    player_hand_str = StringVar()
    player_hand_str.set(f"Player {player_hand.cards}")

    dealer_hand_str = StringVar()
    dealer_hand_str.set(f"Dealer {dealer_hand.cards}")

    dealer_label = ttk.Label(root, textvariable=dealer_hand_str).pack()
    player_label = ttk.Label(root, textvariable=player_hand_str).pack()

    # Count the player total, finish the dealer
    stand_button = ttk.Button(root, text="Stand", command=stand).pack()

    hit_button = ttk.Button(root, text="Hit", command=player_hand.hit).pack()

    # Hit one card, count total, finish the dealer
    double_button = ttk.Button(root, text="Double", command=double).pack()

    # Create two hands and keep the play sequential
    split_button = ttk.Button(root, text="Split", command=split).pack()

    # Deal no cards, finish the dealer
    surrender_button = ttk.Button(
        root, text="Surrender", command=surrender
    ).pack()

    root.mainloop()
