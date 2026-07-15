from functools import wraps

from flask import Blueprint, current_app, jsonify, request, session

from src.models.user import User, db
from src.security import AttemptLimiter, clean_text, normalize_email, normalize_role, validate_password


auth_bp = Blueprint("auth", __name__)
_login_limiter = AttemptLimiter()


def _json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("A JSON object is required")
    return data


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    user = db.session.get(User, user_id)
    if not user or not user.is_active:
        session.clear()
        return None
    return user


def login_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        if not current_user():
            return jsonify({"error": "Authentication required"}), 401
        return view(*args, **kwargs)
    return decorated_function


def admin_required(view):
    @wraps(view)
    def decorated_function(*args, **kwargs):
        user = current_user()
        if not user:
            return jsonify({"error": "Authentication required"}), 401
        if user.role != "admin":
            return jsonify({"error": "Admin access required"}), 403
        return view(*args, **kwargs)
    return decorated_function


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = _json_body()
        email = normalize_email(data.get("email"))
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409
        user = User(
            name=clean_text(data.get("name"), "Name", minimum=2, maximum=100),
            email=email,
            phone=clean_text(data.get("phone", ""), "Phone", maximum=20),
            role=normalize_role(data.get("role"), public_registration=True),
            skills=clean_text(data.get("skills", ""), "Skills", maximum=2000),
            achievements=clean_text(data.get("achievements", ""), "Achievements", maximum=4000),
        )
        user.set_password(validate_password(data.get("password")))
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "User registered successfully", "user": user.to_dict()}), 201
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Registration failed")
        return jsonify({"error": "Registration could not be completed"}), 500


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = _json_body()
        email = normalize_email(data.get("email"))
        key = f"{request.remote_addr or 'unknown'}:{email}"
        allowed, retry_after = _login_limiter.check(key)
        if not allowed:
            response = jsonify({"error": "Too many failed attempts. Try again later."})
            response.status_code = 429
            response.headers["Retry-After"] = str(retry_after)
            return response
        user = User.query.filter_by(email=email).first()
        if not user or not user.is_active or not user.check_password(str(data.get("password") or "")):
            _login_limiter.failure(key)
            return jsonify({"error": "Invalid credentials"}), 401
        _login_limiter.success(key)
        session.clear()
        session.permanent = True
        session["user_id"] = user.id
        return jsonify({"message": "Login successful", "user": user.to_dict()}), 200
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    except Exception:
        current_app.logger.exception("Login failed")
        return jsonify({"error": "Login could not be completed"}), 500


@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"}), 200


@auth_bp.route("/me", methods=["GET"])
@login_required
def get_current_user():
    return jsonify(current_user().to_dict()), 200


@auth_bp.route("/change-password", methods=["POST"])
@login_required
def change_password():
    try:
        data = _json_body()
        user = current_user()
        if not user.check_password(str(data.get("current_password") or "")):
            return jsonify({"error": "Current password is incorrect"}), 400
        new_password = validate_password(data.get("new_password"))
        if user.check_password(new_password):
            return jsonify({"error": "New password must be different"}), 400
        user.set_password(new_password)
        db.session.commit()
        session.clear()
        return jsonify({"message": "Password changed. Sign in again."}), 200
    except ValueError as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 400
    except Exception:
        db.session.rollback()
        current_app.logger.exception("Password change failed")
        return jsonify({"error": "Password could not be changed"}), 500
