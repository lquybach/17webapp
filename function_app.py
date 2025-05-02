import azure.functions as func
from functions.requests import post_request, get_requests
from functions.samples import get_samples
from function.shipping_address_service import get_shipping_addresses



app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route='post_request', methods=['POST'])
@app.function_name(name='PostRequest')
def _post_request(req: func.HttpRequest) -> func.HttpResponse:
    return post_request(req)


@app.route(route='get_requests', methods=['GET'])
@app.function_name(name='GetRequests')
def _get_requests(req: func.HttpRequest) -> func.HttpResponse:
    return get_requests(req)


# @app.route(route='get_requests', methods=['GET'])
# @app.function_name(name='GetRequests')
# def _get_requests(req: func.HttpRequest) -> func.HttpResponse:
#     return get_requests(req)

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
