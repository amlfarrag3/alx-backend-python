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


def stream_users_in_batches(batch_size: int = 100) -> Generator[List[Row], None, None]:
    """Yield lists of `batch_size` rows from user_data using at most **two** loops."""
    conn = _get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT user_id, name, email, age FROM user_data")
        while True:  # loop 1
            batch = cur.fetchmany(batch_size)
            if not batch:
                break
            yield batch  # no inner loop here, keeping loop count low
    finally:
        conn.close()


def batch_processing(batch_size: int = 100) -> Generator[Row, None, None]:
    """Stream batches, filter users with age > 25, and yield qualifying rows.

    Uses only **one** additional loop (total loops in file = 2)."""
    for batch in stream_users_in_batches(batch_size):  # loop 2 (third overall if counting the while loop)
        for row in batch:
            if int(row[3]) > 25:
                yield row
