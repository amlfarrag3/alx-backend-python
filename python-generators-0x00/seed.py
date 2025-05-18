import csv
import uuid
from contextlib import contextmanager
from typing import Generator, Tuple

import mysql.connector
from mysql.connector import errorcode, MySQLConnection

# -------------------
# Low‑level utilities
# -------------------

@contextmanager
def _cursor(conn: MySQLConnection):
    """Context‑manager that yields a freshly created cursor and commits/rolls back automatically."""
    cur = conn.cursor()
    try:
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cur.close()

# -------------------
# Connection helpers
# -------------------

def connect_db() -> MySQLConnection:
    """Connects to the MySQL server using environment variables for creds (or defaults)."""
    import os

    cfg = {
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
    }
    return mysql.connector.connect(**cfg)


def create_database(conn: MySQLConnection, db_name: str = "ALX_prodev") -> None:
    """Create database if it does not exist."""
    with _cursor(conn) as cur:
        cur.execute(f"CREATE DATABASE IF NOT EXISTS {db_name} DEFAULT CHARACTER SET 'utf8mb4'")


def connect_to_prodev() -> MySQLConnection:
    """Return a connection object already using the ALX_prodev database (creating it if needed)."""
    root_conn = connect_db()
    create_database(root_conn)
    root_conn.database = "ALX_prodev"
    return root_conn

# -------------------
# Schema helpers
# -------------------

def create_table(conn: MySQLConnection) -> None:
    """Create user_data table with required columns if it does not exist."""
    ddl = (
        "CREATE TABLE IF NOT EXISTS user_data ("
        "  user_id CHAR(36) NOT NULL PRIMARY KEY,"
        "  name VARCHAR(255) NOT NULL,"
        "  email VARCHAR(255) NOT NULL UNIQUE,"
        "  age DECIMAL(3,0) NOT NULL,"
        "  INDEX (user_id)"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )
    with _cursor(conn) as cur:
        cur.execute(ddl)

# -------------------
# Data helpers
# -------------------

def _row_exists(cur, email: str) -> bool:
    cur.execute("SELECT 1 FROM user_data WHERE email = %s LIMIT 1", (email,))
    return cur.fetchone() is not None


def insert_data(conn: MySQLConnection, csv_path: str) -> None:
    """Insert rows from CSV if they do not already exist (based on unique email)."""
    with open(csv_path, newline="", encoding="utf-8") as f, _cursor(conn) as cur:
        reader = csv.DictReader(f)
        for row in reader:
            if _row_exists(cur, row["email"]):
                continue
            data = (
                str(uuid.uuid4()),
                row["name"],
                row["email"],
                row["age"],
            )
            cur.execute(
                "INSERT INTO user_data (user_id, name, email, age) VALUES (%s,%s,%s,%s)",
                data,
            )

# -------------------
# Streaming generator
# -------------------

def stream_users(conn: MySQLConnection, chunk_size: int = 1) -> Generator[Tuple[str, str, str, int], None, None]:
    """Yield user rows one by one (or in arbitrarily sized chunks)."""
    query = "SELECT user_id, name, email, age FROM user_data"
    with _cursor(conn) as cur:
        cur.execute(query)
        while True:
            rows = cur.fetchmany(chunk_size)
            if not rows:
                break
            for row in rows:
                yield row

# -------------------
# Entrypoint for CLI use
# -------------------

if __name__ == "__main__":
    import argparse, sys

    parser = argparse.ArgumentParser(description="Seed ALX_prodev database and optionally stream data.")
    parser.add_argument("csv", help="Path to user_data.csv")
    parser.add_argument("--stream", action="store_true", help="Stream rows after seeding")
    args = parser.parse_args()

    try:
        connection = connect_to_prodev()
        create_table(connection)
        insert_data(connection, args.csv)
        print("Database seeded successfully.")
        if args.stream:
            for rec in stream_users(connection):
                print(rec)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Authentication error – check your MySQL credentials.")
        else:
            print(err)
            sys.exit(1)
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
