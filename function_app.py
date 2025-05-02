import azure.functions as func
from functions.requests import post_request, get_requests




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