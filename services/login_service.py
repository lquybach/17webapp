# services/login_service.py

from utils.db import get_db_connection
import logging

def get_user_by_name(user_name: str) -> dict:
    """
    users テーブルから user_name で検索し、
    { user_id, user_name, password, role_id } を返す（見つからない場合は None）。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # カラム名を password に変更
            cursor.execute(
                "SELECT user_id, user_name, password, role_id "
                "FROM users WHERE user_name = %s;",
                (user_name,)
            )
            return cursor.fetchone()
    finally:
        conn.close()

def verify_password(plain_password: str, stored_password: str) -> bool:
 
    return plain_password == stored_password
