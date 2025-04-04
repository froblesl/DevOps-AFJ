from flask import Flask, jsonify
from .blueprints.operations import operations_blueprint
from .commands.extensions import db
from .errors.errors import ApiError
import os


def create_app():
    app = Flask(__name__)

    # Configuración base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
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
