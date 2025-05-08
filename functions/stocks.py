# functions/stock.py

import azure.functions as func
import logging
from services.stock_services import update_sample_stock
from services.history_service import insert_history_from_request, insert_stock_history

def update_stock(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing PUT /samples/{id}/stock with history")

    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # フロントから送られるキー名に合わせて取得
    sample_id   = data.get("sample_id")
    new_stock   = data.get("new_stock")
    # operator_id = data.get("user_id")   # フロントで localStorage の user_id を送っている場合
    # comment     = data.get("comment")   # 任意

    if sample_id is None or new_stock is None:
        return func.HttpResponse("Missing field: sample_id or new_stock", status_code=400)

    try:
        sample_id = int(sample_id)
        new_stock = int(new_stock)
    except (TypeError, ValueError):
        return func.HttpResponse("Invalid numeric value", status_code=400)

    try:
        # 1) 在庫更新＆previous_stock取得
        previous_stock = update_sample_stock(sample_id, new_stock)
        logging.info(f"Stock for sample {sample_id}: {previous_stock}→{new_stock}")

        logging.info(data.get("user_id"))

        # 2) 在庫編集履歴をINSERT (action_type="stock_edit")
        try:
            insert_stock_history(
                sample_id=sample_id,
                previous_stock=previous_stock,
                new_stock=new_stock,
                operator_user_id=int(data.get("operator_user_id", 0)),
                comment=data.get("comment"),
                request_id=int(data.get("request_id", 0))
            )
        except Exception as hist_err:
            logging.error(f"Stock-edit history insert failed: {hist_err}")

        return func.HttpResponse("Stock updated", status_code=200)

    except Exception as e:
        logging.error(f"Error in update_stock: {e}")
        return func.HttpResponse(str(e), status_code=500)
