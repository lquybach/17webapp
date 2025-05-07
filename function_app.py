import azure.functions as func
from functions.requests import post_request, get_requests, get_requests_by_user, update_request_status, update_comment
from functions.samples import get_samples
from functions.shipping_address import get_shipping_addresses
from functions.login import login
from functions.stocks import update_stock
from functions.history import get_sample_histories
from functions.status_master import get_status_master





app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route='post_request', methods=['POST'])
@app.function_name(name='PostRequest')
def _post_request(req: func.HttpRequest) -> func.HttpResponse:
    return post_request(req)


@app.route(route='get_requests', methods=['GET'])
@app.function_name(name='GetRequests')
def _get_requests(req: func.HttpRequest) -> func.HttpResponse:
    return get_requests(req)


@app.route(route='get_requests_by_user', methods=['GET'])
@app.function_name(name='GetRequestsByUser')
def _get_requests_by_user(req: func.HttpRequest) -> func.HttpResponse:
    return get_requests_by_user(req)


# Samples endpoints
@app.route(route='samples', methods=['GET'])
@app.function_name(name='GetSamples')
def _get_samples(req: func.HttpRequest) -> func.HttpResponse:
    return get_samples(req)


# Shipping Addresses endpoint
@app.route(route='shipping_addresses', methods=['GET'])
@app.function_name(name='GetShippingAddresses')
def _get_shipping_addresses(req: func.HttpRequest) -> func.HttpResponse:
    return get_shipping_addresses(req)

# ステータス変更用 PUT /requests/{id}/status
@app.route(route="requests/{id}/status", methods=[func.HttpMethod.PUT])
@app.function_name(name="UpdateRequestStatus")
def _update_request_status(req: func.HttpRequest) -> func.HttpResponse:
    return update_request_status(req)

@app.route(route="requests/{id}/comment", methods=[func.HttpMethod.PUT])
@app.function_name(name="UpdateComment")
def _update_comment(req: func.HttpRequest) -> func.HttpResponse:
    return update_comment(req)

# 既存のエンドポイント定義の前に、ログインを追加
@app.route(route="login", methods=[func.HttpMethod.POST])
@app.function_name(name="Login")
def _login(req: func.HttpRequest) -> func.HttpResponse:
    return login(req)


@app.route(route='sample_histories', methods=['GET'])
@app.function_name(name='GetSampleHistories')
def _get_sample_histories(req: func.HttpRequest) -> func.HttpResponse:
    return get_sample_histories(req)

@app.route(route="status_master", methods=[func.HttpMethod.GET, func.HttpMethod.POST])
@app.function_name(name="StatusMaster")
def _status_master(req: func.HttpRequest) -> func.HttpResponse:
    return get_status_master(req)


@app.route(route="samples/{id}/stock", methods=[func.HttpMethod.PUT])
@app.function_name(name="UpdateStock")
def _update_stock(req: func.HttpRequest) -> func.HttpResponse:
    return update_stock(req)
