# functions/stock.py

import azure.functions as func
import logging
from services.stock_service import update_sample_stock
from services.history_service import insert_history_from_request

def update_stock(req: func.HttpRequest) -> func.HttpResponse:
    """
    PUT /samples/{id}/stock
    Body JSON must include:
      - sample_id   : int
      - new_stock   : int
      - request_id  : int (can be 0 if not tied to a request)
    """
    logging.info("Processing PUT /samples/{id}/stock")

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # 必須チェック
    sample_id = data.get("sample_id")
    new_stock = data.get("new_stock")
    request_id = data.get("request_id", 0)

    if sample_id is None or new_stock is None:
        return func.HttpResponse("Missing field: sample_id or new_stock", status_code=400)

    # 型変換
    try:
        sample_id  = int(sample_id)
        new_stock  = int(new_stock)
        request_id = int(request_id)
    except (TypeError, ValueError):
        return func.HttpResponse("Invalid numeric value", status_code=400)

    logging.info(f"Updating stock for sample_id={sample_id} to new_stock={new_stock}")

    try:
        # 1) 在庫更新し、変更前在庫を受け取る
        previous_stock = update_sample_stock(sample_id, new_stock)
        logging.info(f"Stock change: sample_id={sample_id}, previous={previous_stock}, new={new_stock}")

        # 2) 履歴テーブルに INSERT (action_type="stock_edit")
        try:
            insert_history_from_request(request_id=request_id, action_type="stock_edit")
        except Exception as hist_err:
            logging.error(f"Failed to insert stock-edit history for request {request_id}: {hist_err}")

        return func.HttpResponse("Stock updated", status_code=200)

    except Exception as e:
        logging.error(f"Error in update_stock: {e}")
        return func.HttpResponse(str(e), status_code=500)
