import azure.functions as func
import json
import logging
from services.login_service import get_user_by_name, verify_password


def login(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /login
    Body JSON: { "user_name": str, "password": str }
    成功時に user_id, role_id を返却。
    """
    logging.info("Processing POST /login")
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    user_name = data.get("user_name")
    password = data.get("password")
    if not user_name or not password:
        return func.HttpResponse("Missing user_name or password", status_code=400)

    user = get_user_by_name(user_name)
    if not user or not verify_password(password, user['password']):
        return func.HttpResponse("Unauthorized", status_code=401)

    # ログイン成功レスポンス
    resp = { "success": True, "user_id": user['user_id'], "role_id": user['role_id'] }
    return func.HttpResponse(
        json.dumps(resp, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )