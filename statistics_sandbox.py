import numpy as np
import matplotlib.pyplot as plt


def hand_to_idx_hard(hand):
    return hand - 2


def hand_to_idx_soft(hand):
    return hand - 13


def hand_to_idx_pairs(hand):
    return hand - 2


results_hard = []
results_soft = []
results_pairs = []
