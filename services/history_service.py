from utils.db import get_db_connection

def get_all_histories() -> list:
    """
    sample_histories テーブルから全履歴を取得して返します。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT
                  history_id,
                  request_id,
                  action_type,
                  sample_id,
                  sample_name,
                  previous_stock,
                  new_stock,
                  operator_user_id,
                  user_id,
                  comment,
                  updated_at
                FROM sample_histories
                ORDER BY updated_at DESC
            """)
            return cursor.fetchall()
    finally:
        conn.close()

def insert_history_from_request(request_id: int, action_type: str) -> None:
    """
    request_id からリクエスト／サンプル情報を取得し、
    sample_histories テーブルに履歴レコードを INSERT します。
    action_type は 'shipment' or 'stock_edit' など。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1) リクエスト情報取得
            cursor.execute(
                "SELECT sample_id, user_id, comment FROM requests WHERE id = %s",
                (request_id,)
            )
            req = cursor.fetchone()
            sample_id = req["sample_id"]
            user_id   = req.get("user_id")
            comment   = req.get("comment")

            # 2) サンプル情報取得
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name  = samp["sample_name"]
            previous_stock = samp["sample_stock"]

            # 3) 更新対象が出荷の場合は在庫を即時引き落とす(既存ロジック)、
            #    stock_edit 時は在庫編集後の値を取得して new_stock とする。
            #    ここでは新在庫を再取得しておく例：
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            new_stock = cursor.fetchone()["sample_stock"]

            # 4) 履歴テーブルにINSERT
            cursor.execute(
                """
                INSERT INTO sample_histories
                  (request_id, action_type,
                   sample_id, sample_name,
                   previous_stock, new_stock,
                   operator_user_id, comment, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
                """,
                (
                  request_id, action_type,
                  sample_id, sample_name,
                  previous_stock, new_stock,
                  user_id, comment
                )
            )
        conn.commit()
    finally:
        conn.close()
