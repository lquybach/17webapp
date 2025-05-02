import azure.functions as func
import json
from services.request_services import post_record, get_all, get_by_user_id, change_request_status
import logging


def post_request(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    logging.info(f'Received data: {data}')
    post_record(data)
    return func.HttpResponse('Request added', status_code=201)


def get_requests(req: func.HttpRequest) -> func.HttpResponse:
    ret = get_all()
    if ret:
        return func.HttpResponse(body=str(ret), status_code=200)
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
    logging.info("Processing PUT /requests/{id}/status")

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

    # 3) サービス層を呼び出して DB 更新
    try:
        change_request_status(
            request_id=int(request_id),
            status_no=int(data["status_no"])
        )
        return func.HttpResponse(status_code=200)
    except Exception as e:
        logging.error(f"Error in update_request_status: {e}")
        return func.HttpResponse(str(e), status_code=500)