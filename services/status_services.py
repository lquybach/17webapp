import logging
from utils.db import get_db_connection



def resolve_status_no(cursor, name):
    cursor.execute(
        '''
        SELECT
            status_no
        FROM
            statuses
        WHERE
            status_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'status: {ret}')
    return ret['status_no']

def get_all_statuses() -> list:
    """
    statuses テーブルから全ステータスを取得して返します。
    戻り値: [
      { "status_no": 1, "status_name": "未発送" },
      { "status_no": 2, "status_name": "発送済" },
      …
    ]
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  status_no,
                  status_name
                FROM statuses
                ORDER BY status_no
            """)
            return cursor.fetchall()
    finally:
        conn.close()