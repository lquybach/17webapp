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
            user_id
        ) 
        VALUES (%s, %s, %s, %s)
        ''',
        (
            resolve_sample_id(cursor, data['sample_name']),
            data['sample_name'],
            data['sample_stock'],
            data['user_id'],
            # data['comment']
        )
    )