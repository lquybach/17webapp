# functions/stock.py など

import azure.functions as func
import logging
from services.stock_service import update_sample_stock
from services.history_service import insert_history_from_request

def update_stock(req: func.HttpRequest) -> func.HttpResponse:
    """
    PUT /stock  等
    Body JSON: { "request_id": <int>, "sample_id": <int>, "new_stock": <int> }
    """
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # 必須フィールドチェック
    for key in ("request_id", "sample_id", "new_stock"):
        if key not in data:
            return func.HttpResponse(f"Missing field: {key}", status_code=400)

    rid       = int(data["request_id"])
    sample_id = int(data["sample_id"])
    new_stock = int(data["new_stock"])

    logging.info(f"Updating stock for sample {sample_id} to {new_stock}")

    try:
        # 1) 在庫更新
        update_sample_stock(sample_id, new_stock)

        # 2) 履歴 INSERT （action_type="stock_edit"）
        try:
            insert_history_from_request(request_id=rid, action_type="stock_edit")
        except Exception as hist_err:
            logging.error(f"Failed to insert stock-edit history for request {rid}: {hist_err}")

        return func.HttpResponse("Stock updated", status_code=200)

    except Exception as e:
        logging.error(f"Error in update_stock: {e}")
        return func.HttpResponse(str(e), status_code=500)
