from flask import Flask, jsonify
from blueprints.operations import operations_blueprint
from commands.extensions import db
from errors.errors import ApiError


def create_app(testing=False):
    app = Flask(__name__)
    app.config['TESTING'] = testing

    # Configuración directa de la base de datos (sin variables de entorno)
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        "postgresql://postgres:postgres@postgres.cyzaayec84hz.us-east-1.rds.amazonaws.com:5432/postgres"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            print("Base de datos conectada y tablas creadas correctamente.")
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")

    # Registrar los blueprints
    app.register_blueprint(operations_blueprint)

    @app.errorhandler(ApiError)
    def handle_exception(err):
        response = {
            "mssg": err.description,
        }
        return jsonify(response), err.code

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
