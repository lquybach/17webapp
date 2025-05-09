import azure.functions as func
from services.request_services import post_record, get_all, get_by_user_id, change_request_status, change_comment
import logging
from utils.db import get_db_connection
import json
from services.history_service import insert_history_from_request, insert_shipment_history
from services.stock_services import update_sample_stock, get_stock



def post_request(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    logging.info(f'Received data: {data}')
    post_record(data)
    return func.HttpResponse('Request added', status_code=201)


def get_requests(req: func.HttpRequest) -> func.HttpResponse:
    ret = get_all()
    if ret:
        return func.HttpResponse(
            body=json.dumps(ret, ensure_ascii=False, default=str),
            status_code=200,
            mimetype='application/json'
        )
    return func.HttpResponse('Request not found', status_code=404)

#Yasuharu編集分


def get_requests_by_user(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing GET /get_requests_by_user")
    
    # 1) クエリパラメータ user_id を取得
    user_id = req.params.get('user_id')
    if not user_id:
        return func.HttpResponse("Missing user_id", status_code=400)

    try:
        # 2) サービス層から取得
        ret = get_by_user_id(int(user_id))

        # 3) JSON 化して返却
        return func.HttpResponse(
            body=json.dumps(ret, ensure_ascii=False, default=str),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error in get_requests_by_user: {e}")
        return func.HttpResponse(str(e), status_code=500)

#Yasuharu 編集範囲


def update_request_status(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing PUT /requests/{id}/status with precise history")

    rid = req.route_params.get("id")
    if not rid:
        return func.HttpResponse("Missing request id", status_code=400)

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    if "status_no" not in data or "comment" not in data:
        return func.HttpResponse("Missing field: status_no or comment", status_code=400)

    try:
        rid = int(rid)
        new_status = int(data["status_no"])
        comment    = data["comment"]
        op_uid     = data.get("operator_user_id")
    except:
        return func.HttpResponse("Invalid numeric value", status_code=400)

    try:
        # 1) コメントを更新
        change_comment(request_id=rid, comment=comment)
        # 2) ステータスを更新
        change_request_status(request_id=rid, status_no=new_status)

        # 3) 出荷済み(3)なら在庫差し引き＋精密履歴
        if new_status == 3:
            info       = get_request_by_id(rid)
            sample_id  = info["sample_id"]
            quantity   = int(info["quantity"])

            prev_stock = get_stock(sample_id)
            new_stock  = max(0, prev_stock - quantity)
            # 在庫更新
            update_sample_stock(sample_id, new_stock)

            # 正確な prev/new を履歴に入れる
            insert_shipment_history(
                request_id=rid,
                operator_user_id=op_uid,
                comment=comment,
                sample_id=sample_id,
                sample_name=info.get("sample_name", ""),
                previous_stock=prev_stock,
                new_stock=new_stock
            )

        return func.HttpResponse(status_code=200)

    except Exception as e:
        logging.error(f"Error in update_request_status: {e}", exc_info=True)
        return func.HttpResponse(f"Internal error: {e}", status_code=500)

def update_comment(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing PUT /requests/{id}/comment")

   # 1) route から id を取得
    request_id = req.route_params.get("id")
    if not request_id:
        return func.HttpResponse("Missing request id", status_code=400)

    # 2) JSON ボディを parse
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    comment = data.get("comment")
    if comment is None:
        return func.HttpResponse("Missing field: comment", status_code=400)

    try:
        rid = int(request_id)
    except (TypeError, ValueError):
        return func.HttpResponse("Invalid request id", status_code=400)

    # 3) サービス層を呼び出して DB 更新
    try:
        change_comment(rid, comment)
        return func.HttpResponse(status_code=200)
    except Exception as e:
        logging.error(f"Error updating comment: {e}")
        return func.HttpResponse(str(e), status_code=500)

def get_request_by_id(request_id: int) -> dict:
    """
    requests テーブルから ID 指定で 1 レコード取得。
    sample_id, quantity, user_id, comment などを返します。
    """
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                SELECT r.id, r.sample_id, s.sample_name, r.quantity, r.user_id, r.comment
                FROM requests AS r
                JOIN samples AS s ON r.sample_id = s.sample_id
                WHERE r.id = %s
                """,
                (request_id,)
            )
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"Request ID {request_id} not found")
            return row
    finally:
        conn.close()