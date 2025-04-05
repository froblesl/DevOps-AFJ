from flask import request

AUTH_TOKEN = "12345"

def validar_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return False

    token = auth_header.split(" ")[1]
    return token == AUTH_TOKEN
