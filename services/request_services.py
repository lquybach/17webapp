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
def get_by_user_id(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM requests WHERE user_id = %s', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    return rows

#Yasuharu 編集範囲





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