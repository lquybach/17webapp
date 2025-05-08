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
    - action_type: 'shipment'
    - operator_user_id: 操作ユーザーID (Noneならrequests.user_idを使用)
    - comment: 任意
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            # 1) リクエスト情報取得
            cursor.execute(
                "SELECT sample_id, comment AS req_comment, user_id FROM requests WHERE id = %s",
                (request_id,)
            )
            req = cursor.fetchone()
            sample_id      = req["sample_id"]
            final_comment  = req.get("req_comment") or comment or ""
            final_operator = operator_user_id if operator_user_id is not None else req.get("user_id")

            # 2) サンプル現在在庫取得
            cursor.execute(
                "SELECT sample_name, sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            samp           = cursor.fetchone()
            sample_name    = samp["sample_name"]
            sample_stock   = samp["sample_stock"]
            previous_stock = sample_stock

            # 3) 出荷後の在庫取得
            cursor.execute(
                "SELECT sample_stock FROM samples WHERE sample_id = %s",
                (sample_id,)
            )
            new_stock      = cursor.fetchone()["sample_stock"]

            # 4) INSERT
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
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,CURRENT_TIMESTAMP)
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


def insert_shipment_history(
    request_id: int,
    operator_user_id: int,
    comment: str,
    sample_id: int,
    sample_name: str,
    previous_stock: int,
    new_stock: int
) -> None:
    """
    出荷操作用に、前在庫・新在庫をそのまま履歴に INSERT する。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
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
                  %s, 'shipment', %s, %s, %s, %s, %s, %s, %s, CURRENT_TIMESTAMP
                )
            """, (
                request_id,
                sample_id,
                sample_name,
                previous_stock,  # ここは「差し引く前」の在庫
                previous_stock,
                new_stock,       # ここは「差し引いた後」の在庫
                operator_user_id,
                comment or ""
            ))
        conn.commit()
    finally:
        conn.close()