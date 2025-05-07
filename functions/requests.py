import azure.functions as func
from services.request_services import post_record, get_all, get_by_user_id, change_request_status, change_comment
import logging
import json
from services.history_service import insert_history_from_request


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
    logging.info("Processing PUT /requests/{id}/status with history")

    # 1) ルートパラメータから request_id を取得
    request_id = req.route_params.get("id")
    if not request_id:
        return func.HttpResponse("Missing request id in route", status_code=400)

    # 2) ボディから新しい status_no をパース
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    if "status_no" not in data:
        return func.HttpResponse("Missing field: status_no", status_code=400)

    # 3) ステータス更新 + 4) 履歴登録
    try:
        rid = int(request_id)
        new_status = int(data["status_no"])

        # a) ステータス更新
        change_request_status(request_id=rid, status_no=new_status)

        # b) 履歴テーブルに INSERT (action_type="shipment")
        try:
            insert_history_from_request(request_id=rid, action_type="shipment")
        except Exception as hist_err:
            logging.error(f"Failed to insert history for request {rid}: {hist_err}")

        return func.HttpResponse(status_code=200)

    except Exception as e:
        logging.error(f"Error in update_request_status: {e}")
        return func.HttpResponse(str(e), status_code=500)
    

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
    