# functions/login.py

import azure.functions as func
import json, logging
from services.login_service import get_user_by_id, verify_password

def login(req: func.HttpRequest) -> func.HttpResponse:
    """
    POST /login
    Body JSON: { "user_id": int, "password": str }
    成功時に { success: true, user_id, role_id } を返却。
    """
    logging.info("Processing POST /login")
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    # user_id を数値として取得
    try:
        user_id = int(data.get("user_id"))
    except (TypeError, ValueError):
        return func.HttpResponse("Missing or invalid field: user_id", status_code=400)
    password = data.get("password")
    if not password:
        return func.HttpResponse("Missing field: password", status_code=400)

    # DB から取得
    user = get_user_by_id(user_id)
    if not user or not verify_password(password, user['password']):
        return func.HttpResponse("Unauthorized", status_code=401)

    # ログイン成功
    resp = {
        "success": True,
        "user_id": user['user_id'],
        "role_id": user['role_id']
    }
    return func.HttpResponse(
        json.dumps(resp, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )
