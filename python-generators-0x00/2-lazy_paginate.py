from typing import Generator, List, Tuple
import mysql.connector

Row = Tuple[str, str, str, int]


def _get_connection():
    import os
    return mysql.connector.connect(
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        host=os.getenv("MYSQL_HOST", "127.0.0.1"),
        port=int(os.getenv("MYSQL_PORT", 3306)),
        database="ALX_prodev",
    )


def paginate_users(page_size: int, offset: int = 0) -> List[Row]:
    """Fetch a single page of rows starting from `offset` using LIMIT/OFFSET."""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        # Requirement: must contain "SELECT * FROM user_data LIMIT"
        cur.execute(
            "SELECT * FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset),
        )
        return cur.fetchall()
    finally:
        conn.close()


def lazy_paginate(page_size: int) -> Generator[List[Row], None, None]:
    """Lazily yield pages of size `page_size`, fetching the next page only when needed.

    Fulfills constraints:
    * exactly ONE loop (the while below)
    * uses yield for lazy generation
    * relies on paginate_users which itself executes the SQL containing
      "SELECT * FROM user_data LIMIT"
    """
    offset = 0
    while True:  # single loop
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size

