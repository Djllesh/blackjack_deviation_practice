import sqlite3


class ResultLogger:
    def __init__(self, conn: sqlite3.Connection):
        self.sql = """INSERT INTO results(
                      hand_total,
                      hand_type,
                      dealer_upcard,
                      action_played,
                      ruleset_id,
                      true_count,
                      true_action,
                      true_action_source)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        self.conn = conn

    def begin_round(self):
        self.conn.execute("BEGIN")

    def log_result(self, row_tuple: tuple):
        self.conn.execute(self.sql, row_tuple)

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()
