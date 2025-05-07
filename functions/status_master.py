# functions/status_master.py

import azure.functions as func
import json
import logging
from utils.db import get_db_connection
from services.status_services import resolve_status_no, get_all_statuses


def get_status_master(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /api/status_master
    ステータスマスター一覧を JSON で返却します。
    """
    logging.info("Processing GET /status_master")
    try:
        statuses = get_all_statuses()
        return func.HttpResponse(
            json.dumps(statuses, ensure_ascii=False),
            status_code=200,
            mimetype="application/json"
        )
    except Exception as e:
        logging.error(f"Error in get_status_master: {e}")
        return func.HttpResponse(str(e), status_code=500)
