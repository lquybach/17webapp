import azure.functions as func
import json
from services.history_service import get_all_histories

def get_sample_histories(req: func.HttpRequest) -> func.HttpResponse:
    histories = get_all_histories()
    return func.HttpResponse(
        json.dumps(histories, ensure_ascii=False, default=str),
        status_code=200,
        mimetype="application/json"
    )
