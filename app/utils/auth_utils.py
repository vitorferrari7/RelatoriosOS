import jwt
from flask import current_app


def verificar_token(token):
    try:
        secret = current_app.config["SECRET_KEY"]
        decoded = jwt.decode(token, secret, algorithms=["HS256"])
        print("✅ Token válido:", decoded)
        return decoded
    except jwt.ExpiredSignatureError:
        print("❌ Token expirado")
        return None
    except jwt.InvalidTokenError as e:
        print("❌ Token inválido:", str(e))
        return None
