import sqlite3
class SqliteDataAccess:

    def __init__(self):
        self.connection = sqlite3.connect('db.sqlite')
        self.cursor = self.connection.cursor()
        
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS playercode(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(20),
            code TEXT,
            initializationcode TEXT,
            player INTEGER DEFAULT 0
        );
        """)#mache DEFAULT später auf 1

        self.connection.commit()

    def save_item(self, name, code, initialization_code):
        self.cursor.execute(f"""SELECT COUNT(name) FROM playercode WHERE name = "{name}"; """)
        if self.cursor.fetchone()[0] == 0:
            self.cursor.execute(f"""
            INSERT INTO playercode (name, code, initializationcode) VALUES(?,?,?);
            """, (name, code, initialization_code))
            
            self.connection.commit()
        else:#update if the row exists
            self.cursor.execute(f"""
            UPDATE playercode SET code = "{code}", initializationcode = "{initialization_code}"
            WHERE name = "{name}";
            """)
            
            self.connection.commit()

    def get_all_items(self):
        self.cursor.execute("""
        SELECT name, id FROM playercode;
        """)
        return self.cursor.fetchall()

    def get_item(self, id):
        self.cursor.execute(f"""
        SELECT code, initializationcode FROM playercode WHERE id = {id};
        """)
        return self.cursor.fetchone()
