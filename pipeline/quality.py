import sqlite3


def count_invalid_klines(conn: sqlite3.Connection) -> int:
    return conn.execute("""
        SELECT count(*) FROM klines
        WHERE open NOT BETWEEN low AND high
           OR close NOT BETWEEN low AND high
           OR low <= 0
           OR volume < 0
    """).fetchone()[0]


def count_gaps(conn: sqlite3.Connection, interval: str, step_seconds: int) -> int:
    return conn.execute("""
        SELECT count(*) FROM (
            SELECT unixepoch(open_time)
                 - unixepoch(LAG(open_time) OVER (PARTITION BY symbol ORDER BY open_time)) AS gap
            FROM klines
            WHERE interval = ?
        )
        WHERE gap != ?
    """, (interval, step_seconds)).fetchone()[0]
