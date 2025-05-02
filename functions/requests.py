import azure.functions as func
from services.request_services import post_record, get_all
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

from services.request_services import post_record, get_all, get_by_user_id

def get_requests_by_user(req: func.HttpRequest) -> func.HttpResponse:
    user_id = req.params.get('user_id')  # クエリパラメータから user_id を受け取る
    if not user_id:
        return func.HttpResponse("Missing user_id", status_code=400)

    ret = get_by_user_id(user_id)
    if ret:
        return func.HttpResponse(body=str(ret), status_code=200)
    return func.HttpResponse('Request not found', status_code=404)

#Yasuharu 編集範囲