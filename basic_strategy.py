import pandas as pd
import pickle
from collections import defaultdict
from enum import Enum
from pathlib import Path

basic_strategy_path = "basic_strategy/basic_strategy.csv"
basic_strategy = defaultdict(list)


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


class Action(Enum):
    STAND = "s"
    HIT = "h"
    DOUBLE = "d"
    DOUBLE_STAND = "ds"
    SPLIT = "y"
    SURRENDER = "r"
    SURRENDER_SPLIT = "rp"
    SURRENDER_STAND = "rs"


def convert_df_to_dict(df):
    df["hand_type"] = df["hand_type"].str.lower()
    df["dealer_upcard"] = df["dealer_upcard"].replace({"11": "A"})
    df["action"] = df["action"].str.lower()
    df["deviation"] = df["deviation"].str.lower()

    df["hand_total"] = df["hand_total"].astype(int)
    df["index"] = pd.to_numeric(df["index"], errors="coerce")

    for _, row in df.iterrows():
        key = (
            row["hand_total"],
            row["hand_type"],
            row["dealer_upcard"],
            row["ruleset_id"],
        )

        basic_strategy[key].append(
            {
                "base": Action(row["action"]),
                "index": row["index"],
                "comparison": row["comparison"],
                "deviation": Action(row["deviation"])
                if pd.notna(row["deviation"]) and row["deviation"] != ""
                else None,
            }
        )


if __name__ == "__main__":
    df = pd.read_csv(basic_strategy_path, delimiter=";", dtype=str)

    convert_df_to_dict(df)

    with open("data/basic_strategy.pickle", "wb") as handle:
        pickle.dump(basic_strategy, handle, protocol=pickle.HIGHEST_PROTOCOL)
