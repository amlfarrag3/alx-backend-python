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
    """Return a single page of users starting from offset."""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            "SELECT user_id, name, email, age FROM user_data LIMIT %s OFFSET %s",
            (page_size, offset),
        )
        return cur.fetchall()
    finally:
        conn.close()


def lazy_paginate(page_size):
    """Generator that lazily paginates through user_data table.
    Args:
        page_size (int): Number of rows to fetch per page.
    Yields:
        list of dict: A page of user rows.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
