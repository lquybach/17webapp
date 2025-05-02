from utils.db import get_db_connection

def get_user_by_id(user_id: int) -> dict:
    """
    users テーブルから user_id をキーにユーザー情報を取得。
    見つからない場合は None を返す。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, user_name, password, role_id "
                "FROM users WHERE user_id = %s;",
                (user_id,)
            )
            return cursor.fetchone()
    finally:
        conn.close()

def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    平文パスワードをそのまま比較。
    """
    return plain_password == stored_password