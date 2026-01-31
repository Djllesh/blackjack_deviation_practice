import random
from basic_strategy import Action

# TODO:
# For every move we need to compare it with the strategy chart
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


def update_total(cards):
    if "A" in cards:
        # There can only be one soft Ace in the hand
        # Since two soft Aces add to 22 and bust
        n_aces = cards.count("A")
        sum_not_aces = sum([values[card] for card in cards if card != "A"])
        return (n_aces + sum_not_aces, 10 + n_aces + sum_not_aces)

    return sum([values[card] for card in cards])


def _get_total(hand):
    if "A" in hand.cards:
        hard_total = hand.value[0]
        soft_total = hand.value[1]
        return hard_total * (soft_total > 21) + soft_total * (soft_total <= 21)
    else:
        return hand.value


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
        return cls([random.choice(ranks) for _ in range(2)])

    def bust_update(self):
        if self.total > 21:
            self.busted = True

    def is_busted(self):
        return self.busted

    def get_total(self):
        return self.total

    def get_hand_type(self):
        is_ace_in_hand = isinstance(self.value, tuple)
        if not is_ace_in_hand:
            return "hard"

        soft_total = self.value[1]
        hard_total = self.value[0]
        if soft_total <= 21:
            return "soft"
        else:
            return "hard"

    def hit(self):
        self.is_hit = True
        # Can only hit if not busted and can only be busted if hit
        if self.busted:
            return

        new_card = random.choice(ranks)
        self.cards.append(new_card)
        self.value = update_total(self.cards)
        self.total = _get_total(self)
        self.bust_update()


class DealerHand(Hand):
    def __init__(self, cards, rule):
        super().__init__(cards)
        self.rule = rule

    @classmethod
    def deal_initial(cls, card: str = None, rule="H17"):
        if card is not None:
            return cls([card], rule)
        return cls([random.choice(ranks)], rule)

    def reset(self):
        self.cards = [random.choice(ranks)]
        self.recompute()

    def get_upcard(self):
        return self.cards[0]

    def dealer_hitting_condition(self):
        is_ace_in_hand = isinstance(self.value, tuple)

        if is_ace_in_hand:
            soft_total = self.value[1]
            hard_total = self.value[0]
        else:
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

    def finish(self):
        while self.dealer_hitting_condition():
            self.hit()


class Player:
    def __init__(self, init_hand: Hand = None):
        if init_hand is None:
            self.hands: list[Hand] = [Hand.deal_initial()]
        else:
            self.hands: list[Hand] = [init_hand]

        self.wins = 0
        self.losses = 0
        self.pushes = 0

        self.active = 0

    def reset(self):
        self.hands: list[Hand] = [Hand.deal_initial()]
        self.active = 0

    def show_hands(self):
        if len(self.hands) == 1:
            hands = f"{self.hands[0].cards}"
        else:
            hands = f"{[hand.cards for hand in self.hands]}"
        return hands

    def get_totals(self):
        if len(self.hands) == 1:
            total = self.hands[0].get_total()
        else:
            total = [hand.get_total() for hand in self.hands]
        return total

    def active_hand(self):
        return self.hands[self.active]

    def next(self):
        self.active += 1

    def resolve(self, dealer: DealerHand):
        for hand in self.hands:
            is_win = win(hand, dealer)
            is_push = push(hand, dealer)
            if is_win:
                self.wins += 1
                return "w"
            elif is_push:
                self.pushes += 1
                return "p"
            else:
                self.losses += 1
                return "l"

    def split(self):
        active_hand = self.active_hand()
        if len(active_hand.cards) != 2:
            return

        are_tens = active_hand.cards[0] in [
            "J",
            "Q",
            "K",
            "10",
        ] and active_hand.cards[1] in ["J", "Q", "K", "10"]

        if not are_tens and active_hand.cards[0] != active_hand.cards[1]:
            # TODO: Let the player know that they can't split
            return

        card = active_hand.cards[1]
        active_hand.cards.pop(1)
        self.hands.insert(self.active + 1, Hand([card]))
        for i in range(self.active, self.active + 2):
            self.hands[i].hit()

    def can_finish(self):
        if len(self.hands) == 1 or self.active == len(self.hands) - 1:
            return True
        else:
            return False


def win(player_hand: Hand, dealer_hand: DealerHand):
    return (
        player_hand.get_total() > dealer_hand.get_total()
        and not player_hand.is_busted()
    ) or (not player_hand.is_busted() and dealer_hand.is_busted())


def push(player_hand: Hand, dealer_hand: DealerHand):
    return player_hand.get_total() == dealer_hand.get_total() and (
        not player_hand.is_busted() and not dealer_hand.is_busted()
    )
