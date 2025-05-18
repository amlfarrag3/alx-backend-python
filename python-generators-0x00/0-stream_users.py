from contextlib import contextmanager
from typing import Generator, Tuple

import mysql.connector
from mysql.connector import MySQLConnection


@contextmanager
def _cursor(conn: MySQLConnection):
    cur = conn.cursor()
    try:
        yield cur
    finally:
        cur.close()


def _get_connection() -> MySQLConnection:
    """Assumes the database ALX_prodev already exists and credentials are in env vars."""
    import os

    cfg = {
        "user": os.getenv("MYSQL_USER", "root"),
        "password": os.getenv("MYSQL_PASSWORD", ""),
        "host": os.getenv("MYSQL_HOST", "127.0.0.1"),
        "port": int(os.getenv("MYSQL_PORT", 3306)),
        "database": "ALX_prodev",
    }
    return mysql.connector.connect(**cfg)


def stream_users() -> Generator[Tuple[str, str, str, int], None, None]:
    """Yield rows from user_data table one at a time using a single loop."""
    conn = _get_connection()
    try:
        with _cursor(conn) as cur:
            cur.execute("SELECT user_id, name, email, age FROM user_data")
            # Single loop: iterating directly over cursor yields rows lazily
            for row in cur:
                yield row
    finally:
        conn.close()
