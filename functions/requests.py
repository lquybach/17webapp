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