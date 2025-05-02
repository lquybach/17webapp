from utils.db import get_db_connection
from services.sample_services import *
from services.shipping_address_services import *
from services.status_services import *
from services.user_services import *
import logging
import pymysql



def get_all():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests')
    rows = cursor.fetchall()
    conn.close()
    return rows
    # conn = get_db_connection()
    # cursor = conn.cursor()
    # cursor.execute(
    #     'SELECT * FROM requests',
    # )
    # row = cursor.fetchone()
    # conn.close()
    # return dict(zip([col[0] for col in cursor.description], row)) if row else None



def post_record(data):
    conn = get_db_connection()
    cursor = conn.cursor()

    try: 
        cursor.execute(
            '''
            INSERT INTO requests (
                sample_id, 
                quantity, 
                shipping_address_code,
                preferred_date, 
                status_no, 
                user_id
            ) 
            VALUES (%s, %s, %s, %s, %s, %s)
            ''',
            (
                resolve_sample_id(cursor, data['sample_name']),
                data['quantity'],
                resolve_shipping_address_code(cursor, data['address_name']),
                data['preferred_date'],
                resolve_status_no(cursor, data['status_name']),
                resolve_user_id(cursor, data['user_name'])
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

#Yasuharu編集範囲
def get_by_user_id(user_id: int) -> list:
    """
    user_id に紐づくリクエストの詳細を
    JOIN クエリで取得して返します。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """
                SELECT
                  r.id,
                  s.sample_name,
                  r.quantity,
                  sa.address_name,
                  r.preferred_date,
                  r.comment,
                  st.status_name,
                  r.created_at
                FROM requests r
                JOIN samples s
                  ON r.sample_id = s.sample_id
                JOIN shipping_addresses sa
                  ON r.shipping_address_code = sa.shipping_address_code
                JOIN status_master st
                  ON r.status_no = st.status_no
                WHERE r.user_id = %s
                ORDER BY r.created_at DESC
            """
            cursor.execute(sql, (user_id,))
            return cursor.fetchall()
    finally:
        conn.close()

#Yasuharu 編集範囲



def change_request_status(request_id: int, status_no: int) -> None:
    """
    指定された request_id の status_no を更新し、
    updated_at を CURRENT_TIMESTAMP で上書きします。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE requests
                   SET status_no   = %s,
                       updated_at  = CURRENT_TIMESTAMP
                 WHERE id = %s
                """,
                (status_no, request_id)
            )
            conn.commit()
    finally:
        conn.close()


'''
{
  "sample_name": "ミルクティー",
  "quantity": 3,
  "address_name": "関東広域",
  "preferred_date": "2025-05-01",
  "status_name": "承認待ち",
  "user_name": "木下 かんな"
}
'''