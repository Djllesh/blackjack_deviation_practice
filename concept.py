import random

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


# NOTE:
# we begin with the hand being represented by a tuple: string to show
# and the sum value
def hand():
    """Initialize the hand"""
    cards = [random.choice(ranks) for _ in range(2)]
    value = hand_total(cards)
    return (cards, value)


def hand_total(cards):
    if "A" in cards:
        # There can only be one soft Ace in the hand
        # Since two soft Aces add to 22 and bust
        n_aces = cards.count("A")
        sum_not_aces = sum([values[card] for card in cards if card != "A"])
        return (n_aces + sum_not_aces, 10 + n_aces + sum_not_aces)

    return sum([values[card] for card in cards])


def dealer_upcard():
    card = random.choice(ranks)
    return ([card], hand_total([card]))


def dealer_hitting_condition(dealer_hand, rule):
    is_ace_in_hand = isinstance(dealer_hand[1], tuple)

    if is_ace_in_hand:
        soft_total = dealer_hand[1][1]
        hard_total = dealer_hand[1][0]
    else:
        # HACK:
        # If no ace in the hand, there is no soft total
        soft_total = -1
        hard_total = dealer_hand[1]

    if rule == "S17":
        return not ((soft_total >= 17 and soft_total <= 21) or hard_total >= 17)
    if rule == "H17":
        return not ((soft_total > 17 and soft_total <= 21) or hard_total >= 17)


def finish_dealer(upcard, rule="H17"):
    # Here is where you implement the S17 vs H17 rules
    dealer_hand = hit(upcard)
    while dealer_hitting_condition(dealer_hand, rule):
        dealer_hand = hit(dealer_hand)

    return dealer_hand


def hit(hand):
    new_card = random.choice(ranks)
    new_cards = hand[0]
    new_cards.append(new_card)

    new_hand = (new_cards, hand_total(new_cards))
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
    for _ in range(30):
        print(finish_dealer((["A"], (1, 11)), "S17"))
