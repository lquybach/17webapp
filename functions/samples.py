import azure.functions as func
import json
from services.sample_services import get_all
import logging
# from utils.handlers import with_db_error_handling



# def get_samples(req: func.HttpRequest) -> func.HttpResponse:
#     ret = get_all()
#     if ret:
#         return func.HttpResponse(body=str(ret), status_code=200)
#     return func.HttpResponse('Sample not found', status_code=404)

def get_samples(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /samples
    全サンプルを取得して返す。
    """
    try:
        samples = get_all()
        return func.HttpResponse(
            json.dumps(samples, ensure_ascii=False, default=str),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error in get_samples: {e}")
        return func.HttpResponse(str(e), status_code=500)





