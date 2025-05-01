import azure.functions as func
from services.role_services import get_all
import logging


def get_roles(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('bbb')
    roles = get_all()
    if roles:
        return func.HttpResponse(body=str(roles), status_code=200)
    return func.HttpResponse('Sample not found', status_code=404)