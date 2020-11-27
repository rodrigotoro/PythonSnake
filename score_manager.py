import sqlite3
import datetime


class ScoreManager:

    def __init__(self, database_name="scores.db"):
        self.database_name = database_name

    def connect(self):
        self.connection = sqlite3.connect(self.database_name)
        self.cursor = self.connection.cursor()
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS scores (
        timestamp TEXT,
        name TEXT,
        score INTEGER
        );""")
        self.connection.commit()

    def add_score(self, name, score):
        self.cursor.execute("""INSERT INTO scores (timestamp, name, score)
        VALUES (?, ?, ?)""",
        str(datetime.datetime.timestamp(datetime.datetime.now())),
        name,
        score)
        self.connection.commit()

    def get_scores(self):
        self.cursor.execute("SELECT * FROM scores ORDER DESC score")
        return self.cursor.fetchall()


if __name__ == "__main__":
    pass
