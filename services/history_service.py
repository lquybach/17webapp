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
                  sample_stock,
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


def insert_history_from_request(
    request_id: int,
    action_type: str,
    operator_user_id: int = None,
    comment: str = None
) -> None:
    """
    出荷操作用の履歴INSERT。
    - action_type は 'shipment'
    - operator_user_id: 実際に出荷操作を行ったユーザーID（必須）
    - comment: 申請時コメント or 空文字
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1) リクエスト基本情報取得
            cursor.execute(
                "SELECT sample_id, comment AS req_comment FROM requests WHERE id = %s",
                (request_id,)
            )
            req = cursor.fetchone()
            sample_id = req["sample_id"]
            # fallback: リクエストにコメントがなければ引数
            req_comment = req.get("req_comment") or ""
            final_comment = comment if comment is not None else req_comment

            # 2) サンプル現在情報取得
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name  = samp["sample_name"]
            sample_stock = samp["sample_stock"]
            previous_stock = sample_stock

            # 3) 出荷後の在庫を再取得（もし出荷時に別ロジックで更新している場合）
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            new_stock = cursor.fetchone()["sample_stock"]

            # 4) 履歴テーブルにINSERT
            cursor.execute("""
                INSERT INTO sample_histories (
                  request_id,
                  action_type,
                  sample_id,
                  sample_name,
                  sample_stock,
                  previous_stock,
                  new_stock,
                  operator_user_id,
                  comment,
                  updated_at
                ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
            """, (
                request_id,
                action_type,
                sample_id,
                sample_name,
                sample_stock,
                previous_stock,
                new_stock,
                operator_user_id,
                final_comment
            ))
        conn.commit()
    finally:
        conn.close()


def insert_stock_history(
    sample_id: int,
    previous_stock: int,
    new_stock: int,
    operator_user_id: int,
    comment: str = None,
    request_id: int = 0
) -> None:
    """
    在庫編集用の履歴INSERT。
    - action_type は 'stock_edit'
    - operator_user_id: 在庫編集を行ったユーザーID（必須）
    - comment: 任意のコメント
    - request_id: 申請に紐づくIDがあれば、なければ 0
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1) サンプル名＆最新在庫取得
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name  = samp["sample_name"]
            sample_stock = samp["sample_stock"]

            # 2) INSERT
            cursor.execute("""
                INSERT INTO sample_histories (
                  request_id,
                  action_type,
                  sample_id,
                  sample_name,
                  sample_stock,
                  previous_stock,
                  new_stock,
                  operator_user_id,
                  comment,
                  updated_at
                ) VALUES (
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
            """, (
                request_id,
                "stock_edit",
                sample_id,
                sample_name,
                sample_stock,
                previous_stock,
                new_stock,
                operator_user_id,
                comment or ""
            ))
        conn.commit()
    finally:
        conn.close()
