from flask import Blueprint, request, jsonify, render_template, redirect, url_for, current_app
import jwt
import datetime
from app.utils.auth_utils import verificar_token
from app import db

auth_bp = Blueprint("auth", __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    from app.models.user import User
    if request.method == 'POST':
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        if User.query.filter_by(email=email).first():
            return jsonify({'success': False, 'message': 'Email já registrado'}), 400

        user = User(email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Usuário registrado com sucesso'})

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    from app.models.user import User
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        token = jwt.encode(
            {"user": email, "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
            key=current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

        return jsonify({"success": True, "token": token})
    else:
        return jsonify({"success": False, "message": "Credenciais inválidas"}), 401


@auth_bp.route("/me")
def get_logged_user():
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"email": None}), 401

    token = auth_header.split(" ")[1]

    if not verificar_token(token):
        return jsonify({"email": None}), 401

    try:
        data = jwt.decode(token, current_app.config["SECRET_KEY"], algorithms=["HS256"])
        return jsonify({"email": data["user"]})
    except Exception:
        return jsonify({"email": None}), 401


@auth_bp.route("/logout")
def logout():
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/")
def home():
    return render_template("index.html")
