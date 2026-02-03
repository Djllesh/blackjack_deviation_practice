import sqlite3
from pathlib import Path

RESULTS_PATH = Path("data/results.db")
needed = {
    "id",
    "hand_total",
    "hand_type",
    "dealer_upcard",
    "action_played",
    "ruleset_id",
    "true_count",
    "true_action",
    "true_action_source",
}


def open_results_db(
    needed: set[str] = needed, table: str = "results"
) -> sqlite3.Connection:
    RESULTS_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(RESULTS_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("""CREATE TABLE IF NOT EXISTS results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    hand_total INTEGER NOT NULL,
                    hand_type text NOT NULL,
                    dealer_upcard INTEGER NOT NULL,
                    action_played text NOT NULL,
                    ruleset_id text NOT NULL,
                    true_count INTEGER NOT NULL,
                    true_action text NOT NULL,
                    true_action_source text NOT NULL)""")
    conn.commit()
    require_columns(conn, table, needed)
    return conn


def require_columns(
    conn: sqlite3.Connection, table: str, needed: set[str]
) -> None:
    rows = conn.execute(f"PRAGMA table_info({table})").fetchall()
    existing = {r[1] for r in rows}  # column name is index 1
    missing = needed - existing
    if missing:
        raise RuntimeError(
            f"DB schema mismatch: table '{table}' missing columns: {sorted(missing)}"
        )
