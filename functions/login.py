# functions/login.py

import azure.functions as func
import json, logging
from services.login_service import get_user_by_name, verify_password
from shared.auth import generate_token

def login(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Processing POST /login")
    try:
        data = req.get_json()
    except ValueError:
        return func.HttpResponse("Invalid JSON", status_code=400)

    user_name = data.get("user_name")
    password  = data.get("password")
    if not user_name or not password:
        return func.HttpResponse("Missing user_name or password", status_code=400)

    user = get_user_by_name(user_name)
    # stored_password に平文が入り、verify_password でそのまま比較
    if not user or not verify_password(password, user["password"]):
        return func.HttpResponse("Unauthorized", status_code=401)

    token = generate_token({"sub": user["user_id"], "role": user["role_id"]})
    return func.HttpResponse(
        json.dumps({
            "token":   token,
            "user_id": user["user_id"],
            "role_id": user["role_id"]
        }, ensure_ascii=False),
        status_code=200,
        mimetype="application/json"
    )
