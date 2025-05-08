from utils.db import get_db_connection

def get_all_histories() -> list:
    """
    sample_histories テーブルから全履歴を取得し、updated_at 降順で返します。
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
    - operator_user_id: ログインユーザーID（Noneなら requests.user_idを使用）
    - comment: リクエスト時コメント or 引数comment
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1) リクエスト基本情報取得
            cursor.execute(
                "SELECT sample_id, comment AS req_comment, user_id FROM requests WHERE id = %s",
                (request_id,)
            )
            req = cursor.fetchone()
            sample_id = req["sample_id"]
            # コメントはリクエストのもの優先。それも無ければ引数comment、さらに無ければ空文字
            final_comment = req.get("req_comment") or comment or ""
            # operator_user_id が None なら requests.user_id を使う
            final_operator = operator_user_id if operator_user_id is not None else req.get("user_id")

            # 2) サンプル情報取得（現在在庫）
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name    = samp["sample_name"]
            sample_stock   = samp["sample_stock"]
            previous_stock = samp["sample_stock"]

            # 3) 出荷後在庫を再取得（別ロジックで在庫減算済みなら最新が入る）
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            new_stock = cursor.fetchone()["sample_stock"]

            # 4) INSERT（必ず sample_stock を含める）
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
                final_operator,
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
    comment: str = "",
    request_id: int = 0
) -> None:
    """
    在庫編集用の履歴INSERT。
    - action_type は 'stock_edit'
    - operator_user_id: ログインユーザーID
    - comment: 任意コメント
    - request_id: 紐づくリクエストID（無ければ0）
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # サンプル名＆最新在庫取得
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp = cursor.fetchone()
            sample_name  = samp["sample_name"]
            sample_stock = samp["sample_stock"]

            # INSERT（必ず sample_stock を含める）
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
