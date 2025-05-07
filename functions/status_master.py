# functions/status_master.py

import azure.functions as func
import json
import logging
from utils.db import get_db_connection
from services.status_service import resolve_status_no


def status_master(req: func.HttpRequest) -> func.HttpResponse:
    """
    GET /api/status_master?status_name=差戻し
    or POST /api/status_master with JSON {"status_name": "..."}
    Returns {"status_no": <number>} or 404 if not found.
    """
    logging.info("Processing GET/POST /status_master")

    # パラメータ取得
    status_name = req.params.get("status_name")
    if not status_name:
        try:
            data = req.get_json()
            status_name = data.get("status_name")
        except ValueError:
            pass

    if not status_name:
        return func.HttpResponse("Missing status_name", status_code=400)

    # DB 検索
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            status_no = resolve_status_no(cursor, status_name)
    finally:
        conn.close()

    if status_no is None:
        return func.HttpResponse(f"Status '{status_name}' not found", status_code=404)

    # JSON レスポンス
    return func.HttpResponse(
        json.dumps({"status_no": status_no}, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )
