from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
import os
from sqlalchemy import text

from app.extensions import db
from app.routes.auth import auth_bp
from app.routes.ordens import ordens_bp

def create_app():
    load_dotenv()
    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "chave-padrao")
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    CORS(app,
         supports_credentials=True,
         origins=["http://127.0.0.1:5000"],
         methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization"]
    )

    db.init_app(app)

    # Verifica a conexão antes de qualquer requisição
    def check_db_connection():
        try:
            db.session.execute(text('SELECT 1'))  # Consulta simples
            print("✅ Conexão com o banco de dados bem-sucedida!")
        except Exception as e:
            print(f"❌ Erro ao conectar ao banco de dados: {e}")

    app.register_blueprint(auth_bp)
    app.register_blueprint(ordens_bp)

    return app
