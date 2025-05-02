import azure.functions as func
import json
from services.shipping_address_services import list_addresses

def get_shipping_addresses(req: func.HttpRequest) -> func.HttpResponse:
    addresses = list_addresses()
    return func.HttpResponse(
        json.dumps(addresses, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )