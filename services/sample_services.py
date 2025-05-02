
from utils.db import get_db_connection
import logging


def get_all():
    """
    samples テーブルから全レコードを取得し、
    list[dict] 形式で返す。
    各 dict のキー: sample_id, sample_name, sample_stock
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT sample_id, sample_name, sample_stock FROM samples;"
            )
            return cursor.fetchall()
    finally:
        conn.close()




# def create_sample(name: str, stock: int = 0) -> int:
#     """
#     samples テーブルに新しいレコードを追加し、
#     作成された sample_id を返す。

#     :param name: サンプル名
#     :param stock: 初期在庫量（デフォルト 0）
#     :return: 新規作成レコードの sample_id
#     """
#     conn = get_db_connection()
#     try:
#         with conn.cursor() as cursor:
#             cursor.execute(
#                 "INSERT INTO samples (sample_name, sample_stock) VALUES (%s, %s);",
#                 (name, stock)
#             )
#             conn.commit()
#             return cursor.lastrowid
#     finally:
#         conn.close()


def resolve_sample_id(cursor, name):
    cursor.execute(
        '''
        SELECT
            sample_id
        FROM
            samples
        WHERE
            sample_name = %s
        ''',
        (name,)
    )
    ret = cursor.fetchone()
    logging.info(f'sample: {ret}')
    # if not ret:
    #     raise ValueError('サンプルが見つかりません')
    return ret['sample_id']
