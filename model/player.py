from model.hand import Hand
from model.dealer import DealerHand


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

    def reset(self, hands: list[Hand] = None):
        if hands is None:
            self.hands: list[Hand] = [Hand.deal_initial()]
        else:
            self.hands = hands
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
        if not dealer.finished:
            return None

        for hand in self.hands:
            result = hand.resolve(dealer)
            if result == "w":
                self.wins += 1
            elif result == "p":
                self.pushes += 1
            elif result == "l":
                self.losses += 1
            else:
                raise ValueError(
                    f"Something went wrong when resolving the hand. Result {result}"
                )

    def can_split(self):
        active_hand = self.active_hand()
        if len(active_hand.cards) != 2:
            return False

        are_tens = active_hand.cards[0] in [
            "J",
            "Q",
            "K",
            "10",
        ] and active_hand.cards[1] in ["J", "Q", "K", "10"]

        if not are_tens and active_hand.cards[0] != active_hand.cards[1]:
            # TODO: Let the player know that they can't split
            return False

        return True

    def split(self, cards: list[str] = None):
        if not self.can_split():
            return

        active_hand = self.active_hand()
        card = active_hand.cards[1]
        active_hand.cards.pop(1)
        self.hands.insert(self.active + 1, Hand([card]))
        for i in range(self.active, self.active + 2):
            if cards is None:
                self.hands[i].hit(on_split=True)
            else:
                self.hands[i].hit(card=cards[i], on_split=True)

    def can_finish(self):
        if len(self.hands) == 1 or self.active == len(self.hands) - 1:
            return True
        else:
            return False
