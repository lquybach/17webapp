import logging
from utils.db import get_db_connection




def resolve_shipping_address_code(cursor, name):
    cursor.execute(
        '''
        SELECT
            shipping_address_code
        FROM
            shipping_addresses
        WHERE
            address_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'addr: {ret}')
    # if not ret:
    #     raise ValueError('サンプルが見つかりません')
    return ret['shipping_address_code']


def list_addresses():
    """
    shipping_addresses テーブルから全レコードを取得し、
    list of dict 形式で返す。
    各 dict のキー: shipping_address_code, address_name
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM shipping_addresses;"
            )
            return cursor.fetchall()
    finally:
        conn.close()