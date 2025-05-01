from utils.db import get_db_connection
import logging


def get_all():
    logging.info('ccc')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM roles',
    )
    row = cursor.fetchone()
    conn.close()
    return dict(zip([col[0] for col in cursor.description], row)) if row else None
