import pickle
from pathlib import Path
from collections import defaultdict


def load_pickle(path: Path) -> defaultdict:
    if not path.exists():
        raise FileExistsError(
            f"Basic strategy file not found. Path {str(path)}"
        )
    with open(path, "rb") as handle:
        strategy = pickle.load(handle)
    if not isinstance(strategy, defaultdict):
        raise TypeError(
            "Unexpected type of basic strategy object, expected defaultdict."
        )

    return strategy
