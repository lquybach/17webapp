from utils.db import get_db_connection

def get_all_histories() -> list:
    """
    sample_histories テーブルから全履歴を取得し、
    updated_at 降順で返します。
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
    request_id に紐づくリクエスト情報を元に
    sample_histories テーブルへ INSERT します。
    action_type は 'shipment' など。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # リクエスト情報取得
            cursor.execute(
                "SELECT sample_id, user_id, comment FROM requests WHERE id = %s",
                (request_id,)
            )
            req = cursor.fetchone()
            sample_id = req["sample_id"]
            operator_user_id = req.get("user_id")
            comment = req.get("comment")

            # サンプル現在情報取得
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name = samp["sample_name"]
            previous_stock = samp["sample_stock"]

            # 新在庫を再取得しておく（出荷時には stock が減る）
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            new_stock = cursor.fetchone()["sample_stock"]

            # INSERT
            cursor.execute("""
                INSERT INTO sample_histories (
                  request_id,
                  action_type,
                  sample_id,
                  sample_name,
                  previous_stock,
                  new_stock,
                  operator_user_id,
                  comment,
                  updated_at
                ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
            """, (
                request_id,
                action_type,
                sample_id,
                sample_name,
                previous_stock,
                new_stock,
                operator_user_id,
                comment
            ))
        conn.commit()
    finally:
        conn.close()


def insert_stock_history(
    sample_id: int,
    previous_stock: int,
    new_stock: int,
    operator_user_id: int = None,
    comment: str = None
) -> None:
    """
    在庫編集専用の履歴 INSERT。
    action_type は 'stock_edit' 固定。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # サンプル名取得
            cursor.execute(
                "SELECT sample_name FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name = samp["sample_name"]

            # INSERT
            cursor.execute("""
                INSERT INTO sample_histories (
                  action_type,
                  sample_id,
                  sample_name,
                  previous_stock,
                  new_stock,
                  operator_user_id,
                  comment,
                  updated_at
                ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
            """, (
                "stock_edit",
                sample_id,
                sample_name,
                previous_stock,
                new_stock,
                operator_user_id,
                comment
            ))
        conn.commit()
    finally:
        conn.close()
