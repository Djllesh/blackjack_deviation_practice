import sqlite3


class ResultFetcher:
    def __init__(self, conn: sqlite3.Connection):
        self.sql = "SELECT action_played, true_count, true_action, true_action_source FROM results WHERE hand_total = ? AND hand_type = ? AND dealer_upcard = ? AND ruleset_id = ?"
        self.conn = conn

    def fetch(self, key: tuple):
        return self.conn.execute(self.sql, key)
