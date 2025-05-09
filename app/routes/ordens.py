from flask import Blueprint, jsonify, request
from app.utils.auth_utils import verificar_token
from app.services.hubsoft import buscar_ordens_servico

ordens_bp = Blueprint("ordens", __name__)

@ordens_bp.route("/ordens-servico", methods=["GET"])
def ordens_servico():
    token = request.headers.get("Authorization")
    if not token or not verificar_token(token.replace("Bearer ", "")):
        return jsonify({"error": "Acesso não autorizado"}), 403

    try:
        ordens = buscar_ordens_servico()
        return jsonify(ordens)
    except Exception as e:
        return jsonify({"error": f"Erro ao buscar ordens de serviço: {str(e)}"}), 500
