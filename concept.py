import random
import tkinter as tk
from tkinter import ttk, StringVar, IntVar
from players import Player, DealerHand, Hand


def stand(player: Player, dealer_hand: DealerHand):
    if player.can_finish():
        dealer_hand.finish()
        dealer_hand_str.set(f"Dealer {dealer_hand.cards}")
        result_str.set(
            f"""
            Previous: Player {player.get_totals()} vs Dealer {
                dealer_hand.get_total()
            }
            """
        )
        player.resolve(dealer_hand)
        wpl_str.set(f"W/P/L\n{player.wins}/{player.pushes}/{player.losses}")
        disable_all()
        root.after(2000, lambda: reset(player, dealer_hand))
    else:
        player.next()


def hit(player: Player, dealer_hand: DealerHand):
    player.active_hand().hit()
    player_hand_str.set(f"Player {player.show_hands()}")
    if player.active_hand().is_busted():
        stand(player, dealer_hand)


def double(player: Player, dealer_hand: DealerHand):
    player.active_hand().hit()
    player_hand_str.set(f"Player {player.show_hands()}")
    stand(player, dealer_hand)


def split(player: Player, dealer_hand: DealerHand):
    player.split()
    player_hand_str.set(f"Player {player.show_hands()}")


def surrender(player: Player, dealer_hand: DealerHand):
    # for now equivalent to standing
    stand(player, dealer_hand)


def reset(player: Player, dealer_hand: DealerHand):
    player.reset()
    dealer_hand.reset()
    player_hand_str.set(f"Player {player.show_hands()}")
    dealer_hand_str.set(f"Dealer {dealer_hand.cards}")
    enable_all()


def disable_all():
    hit_button.config(state=tk.DISABLED)
    stand_button.config(state=tk.DISABLED)
    double_button.config(state=tk.DISABLED)
    surrender_button.config(state=tk.DISABLED)
    split_button.config(state=tk.DISABLED)


def enable_all():
    hit_button.config(state=tk.NORMAL)
    stand_button.config(state=tk.NORMAL)
    double_button.config(state=tk.NORMAL)
    surrender_button.config(state=tk.NORMAL)
    split_button.config(state=tk.NORMAL)


if __name__ == "__main__":
    root = tk.Tk()

    player = Player(init_hand=Hand(["J", "Q"]))
    dealer_hand = DealerHand.deal_initial()

    player_hand_str = StringVar()
    player_hand_str.set(f"Player {player.show_hands()}")

    dealer_hand_str = StringVar()
    dealer_hand_str.set(f"Dealer {dealer_hand.cards}")

    dealer_label = ttk.Label(root, textvariable=dealer_hand_str)
    dealer_label.pack()
    player_label = ttk.Label(root, textvariable=player_hand_str)
    player_label.pack()

    # Count the player total, finish the dealer
    stand_button = ttk.Button(
        root, text="Stand", command=lambda: stand(player, dealer_hand)
    )
    stand_button.pack()

    hit_button = ttk.Button(
        root, text="Hit", command=lambda: hit(player, dealer_hand)
    )
    hit_button.pack()

    # Hit one card, count total, finish the dealer
    double_button = ttk.Button(
        root, text="Double", command=lambda: double(player, dealer_hand)
    )
    double_button.pack()

    # Create two hands and keep the play sequential
    split_button = ttk.Button(
        root, text="Split", command=lambda: split(player, dealer_hand)
    )
    split_button.pack()

    # Deal no cards, finish the dealer
    surrender_button = ttk.Button(
        root, text="Surrender", command=lambda: surrender(player, dealer_hand)
    )
    surrender_button.pack()

    result_str = StringVar()
    result_label = tk.Label(root, textvariable=result_str)
    result_label.pack()

    wpl_str = StringVar()
    wpl_str.set("W/P/L\n0/0/0")
    wpl_label = tk.Label(root, textvariable=wpl_str)
    wpl_label.pack()

    root.mainloop()
