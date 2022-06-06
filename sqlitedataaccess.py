import sqlite3


class SqliteDataAccess:

    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite')
        self.cursor = self.connection.cursor()

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS scorelist(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER
        );
        """)

        self.connection.commit()

    def save_item(self, name, code, initialization_code, opponent=False):
        self.cursor.execute(
            f"""SELECT COUNT(name) FROM playercode WHERE name = "{name}"; """)
        if self.cursor.fetchone()[0] == 0:
            if opponent:
                player = 0
            else:
                player = 1
            self.cursor.execute(f"""
            INSERT INTO playercode (name, code, initializationcode, player) VALUES(?,?,?,?);
            """, (name, code, initialization_code, player))

            self.connection.commit()
        else:  # update if the row exists
            if opponent:
                player = 0
            else:
                player = 1
            self.cursor.execute(f"""
            UPDATE playercode SET code = "{code}", initializationcode = "{initialization_code}", player={player}
            WHERE name = "{name}";
            """)

            self.connection.commit()

    def get_all_items(self, opponent=False, opponent_type="s"):
        string = """
        SELECT name, id FROM playercode WHERE player = 
        """
        if opponent:
            string += f'0 AND name LIKE "{opponent_type}%"'
        else:
            string += "1"
        self.cursor.execute(string)
        return self.cursor.fetchall()

    def get_item(self, id):
        self.cursor.execute(f"""
        SELECT code, initializationcode FROM playercode WHERE id = {id};
        """)
        return self.cursor.fetchone()

    def save_score(self, score):
        self.cursor.execute(f"""
            INSERT INTO scorelist(score) VALUES({score});
            """)

        self.connection.commit()

    def get_5_best_scores(self):
        self.cursor.execute("""
        SELECT score FROM scorelist 
        ORDER BY score ASC;
        """)
        scores = self.cursor.fetchall()[:5]
        new_scores = []
        for score in scores:
            new_scores.append(*score)
        return new_scores
