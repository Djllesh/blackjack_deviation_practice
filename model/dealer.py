from model.hand import Hand
from model.draw import draw


class DealerHand(Hand):
    def __init__(self, cards, rule):
        super().__init__(cards)
        self.rule = rule
        self.finished = False

    @classmethod
    def deal_initial(cls, card: str = None, rule="H17"):
        if card is not None:
            return cls([card], rule)
        return cls(draw(1), rule)

    def reset(self):
        self.cards = draw(1)
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
        self.finished = True
