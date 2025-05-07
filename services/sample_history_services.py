
from utils.db import get_db_connection
import logging


def get_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT
            *
        FROM 
            sample_histories
        ORDER BY
            updated_at DESC
        """)
    rows = cursor.fetchall()
    conn.close()
    return rows