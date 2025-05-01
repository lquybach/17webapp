import azure.functions as func
from services.sample_services import get_all
import logging
# from utils.handlers import with_db_error_handling



def get_samples(req: func.HttpRequest) -> func.HttpResponse:
    ret = get_all()
    if ret:
        return func.HttpResponse(body=str(ret), status_code=200)
    return func.HttpResponse('Sample not found', status_code=404)