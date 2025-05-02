from utils.db import get_db_connection


def get_user_by_name(user_name: str) -> dict:
    """
    users テーブルから user_name をキーにユーザ情報を取得。
    見つからない場合は None を返す。

    :param user_name: ログイン試行するユーザ名
    :return: {
        'user_id': int,
        'user_name': str,
        'password': str,
        'role_id': int
    } または None
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT user_id, user_name, password, role_id"
                " FROM users WHERE user_name = %s;",
                (user_name,)
            )
            return cursor.fetchone()
    finally:
        conn.close()


def verify_password(plain_password: str, stored_password: str) -> bool:
    """
    プレーンテキストのパスワードをそのまま比較する。
    :param plain_password: 入力されたパスワード
    :param stored_password: DB 保存のパスワード（平文）
    :return: 一致すれば True
    """
    return plain_password == stored_password