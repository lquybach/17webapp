import azure.functions as func
from services.stock_services import update_record
import logging
# from utils.handlers import with_db_error_handling



def update_stock(req: func.HttpRequest) -> func.HttpResponse:
    data = req.get_json()
    logging.info(f'Received data: {data}')
    update_record(data)
    return func.HttpResponse('Stock updated', status_code=201)