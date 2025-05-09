import os
import logging
import pymysql


def get_db_connection():
    try:
        conn = pymysql.connect(
            host=os.environ['DB_HOST'],
            user=os.environ['DB_USER'],
            password=os.environ['DB_PASSWORD'],
            database=os.environ['DB_NAME'],
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=5,
            ssl={'fake_flag_to_enable_tls': True},
            init_command="SET time_zone = '+09:00';"
        )
        return conn
    except pymysql.MySQLError as e:
        logging.error(f'MySQL connection error: {e}')
        raise