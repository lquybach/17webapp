from utils.db import get_db_connection
from services.sample_services import *
import logging
import pymysql



def update_record(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        post_history(cursor, data)
        cursor.execute(
            '''
            UPDATE
                samples
            SET
                sample_stock = %s
            WHERE
                sample_id = %s
            ''',
            (
                data['sample_stock'],
                resolve_sample_id(cursor, data['sample_name'])
            )
        )
        conn.commit()
    except pymysql.err.OperationalError as e:
        logging.error(f'Operational error: {e}')
        # return func.HttpResponse(f'Database operational error: {str(e)}', status_code=500)
    except pymysql.err.ProgrammingError as e:
        logging.error(f'Programming error: {e}')
        # return func.HttpResponse(f'Database programming error: {str(e)}', status_code=500)
    except Exception as e:
        logging.error(f'Unexpected error: {e}')
        # return func.HttpResponse(f'Unexpected error: {str(e)}', status_code=500)
    finally:
        conn.close()


def post_history(cursor, data):
    cursor.execute(
        '''
        INSERT INTO sample_histories (
            sample_id, 
            sample_name, 
            sample_stock,
            user_id,
            comment
        ) 
        VALUES (%s, %s, %s, %s, %s)
        ''',
        (
            resolve_sample_id(cursor, data['sample_name']),
            data['sample_name'],
            data['sample_stock'],
            data['user_id'],
            data['comment']
        )
    )



def update_sample_stock(sample_id: int, new_stock: int) -> int:
    """
    前在庫を返しつつ、新在庫をセットします。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 前在庫取得
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            prev = cursor.fetchone()["sample_stock"]

            # 在庫更新
            cursor.execute(
                "UPDATE samples SET sample_stock = %s, updated_at = CURRENT_TIMESTAMP WHERE sample_id = %s",
                (new_stock, sample_id)
            )
        conn.commit()
        return prev
    finally:
        conn.close()

def get_stock(sample_id: int) -> int:
    """
    現在の在庫数を返します。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            row = cursor.fetchone()
            if row is None:
                raise ValueError(f"Sample {sample_id} not found")
            return row["sample_stock"]
    finally:
        conn.close()