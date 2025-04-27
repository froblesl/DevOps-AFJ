from flask import Flask, jsonify, request, Blueprint
from commands.create import Create
import uuid
from commands.extensions import db
from models.model import List
from commands.config import validar_token


operations_blueprint = Blueprint('operations', __name__)

# POST /blacklists
@operations_blueprint.route('/blacklists', methods=['POST'])
def create_blacklist_entry():
    if not validar_token():
        return jsonify({"msg": "Token inválido o no proporcionado"}), 403

    data = request.get_json()
    required_fields = ["email", "app_uuid", "blocked_reason"]
    if not data or not all(field in data for field in required_fields):
        return jsonify({"msg": "Faltan campos requeridos: email, app_uuid, blocked_reason"}), 400

    try:
        app_uuid = uuid.UUID(str(data["app_uuid"]).strip())
    except ValueError:
        return jsonify({"msg": "El app_uuid no es un UUID válido"}), 400

    try:
        request_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        create_command = Create(
            email=data["email"],
            app_uuid=app_uuid,
            blocked_reason=data["blocked_reason"],
            request_ip=request_ip
        )
        entry_data = create_command.execute()

        return jsonify({
            "msg": "Entrada agregada correctamente a la lista negra.",
            "data": entry_data
        }), 201

    except Exception as e:
        return jsonify({"msg": f"Error inesperado: {str(e)}"}), 500


# GET /blacklists/<email>
@operations_blueprint.route('/blacklists/<string:email>', methods=['GET'])
def check_blacklist_entry(email):
    if not validar_token():
        return jsonify({"msg": "Token inválido o no proporcionado"}), 403

    try:
        entry = db.session.query(List).filter_by(email=email).first()

        if entry:
            return jsonify({
                "blacklisted": True,
                "reason": entry.blocked_reason
            }), 200
        else:
            return jsonify({
                "blacklisted": False,
                "reason": None
            }), 200

    except Exception as e:
        return jsonify({"msg": f"Error inesperado: {str(e)}"}), 500

# GET /ping - Healthcheck
@operations_blueprint.route('/ping', methods=['GET'])
def healthcheck():
    return jsonify({"status": "ok"}), 200
