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
    samples テーブルの sample_stock を new_stock に更新し、
    変更前の在庫数を戻り値として返します。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1) 変更前の在庫を取得
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Sample ID {sample_id} not found")
            previous_stock = row["sample_stock"]

            # 2) 在庫を更新
            cursor.execute(
                "UPDATE samples SET sample_stock = %s WHERE sample_id = %s",
                (new_stock, sample_id)
            )
        conn.commit()
        return previous_stock

    finally:
        conn.close()