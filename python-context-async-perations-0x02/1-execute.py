import sqlite3

class ExecuteQuery:
    def __init__(self, db_path, query, params=None):
        self.db_path = db_path
        self.query = query
        self.params = params or ()
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.cursor.execute(self.query, self.params)
        return self.cursor.fetchall()  # returns the result of the query

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
          
