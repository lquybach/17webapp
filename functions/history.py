import azure.functions as func
from services.sample_history_services import get_all
import logging
import json



def get_sample_histories(req: func.HttpRequest) -> func.HttpResponse:
    ret = get_all()
    if ret:
        return func.HttpResponse(
            body=json.dumps(ret, ensure_ascii=False, default=str),
            status_code=200,
            mimetype='application/json'
        )
    return func.HttpResponse('Request not found', status_code=404)