import sqlite3
import functools

#### decorator to lof SQL queries

 def log_queries(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # Attempt to extract and log the SQL query
        if 'query' in kwargs:
            query = kwargs['query']
        elif args:
            query = args[0]
        else:
            query = "UNKNOWN QUERY"

        print(f"Executing SQL Query: {query}")
        return func(*args, **kwargs)
    return wrapper

@log_queries
def fetch_all_users(query):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results

#### fetch users while logging the query
users = fetch_all_users(query="SELECT * FROM users")
