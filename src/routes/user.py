from flask import Blueprint, current_app, jsonify, request

from src.models.user import User, db
from src.routes.auth import admin_required, current_user, login_required
from src.security import clean_text, normalize_email, normalize_role, validate_password

user_bp = Blueprint("user", __name__)


def _json_body():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        raise ValueError("A JSON object is required")
    return data


def _safe_failure(message, status=400):
    db.session.rollback()
    return jsonify({"error": message}), status


@user_bp.route("/users", methods=["GET"])
@admin_required
def get_users():
    users = User.query.filter_by(is_active=True).order_by(User.created_at.desc()).all()
    return jsonify([user.to_dict() for user in users]), 200


@user_bp.route("/users", methods=["POST"])
@admin_required
def create_user():
    try:
        data = _json_body()
        email = normalize_email(data.get("email"))
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409
        user = User(
            name=clean_text(data.get("name"), "Name", minimum=2, maximum=100),
            email=email,
            phone=clean_text(data.get("phone", ""), "Phone", maximum=20),
            role=normalize_role(data.get("role")),
            skills=clean_text(data.get("skills", ""), "Skills", maximum=2000),
            achievements=clean_text(data.get("achievements", ""), "Achievements", maximum=4000),
        )
        user.set_password(validate_password(data.get("password")))
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
    except ValueError as error:
        return _safe_failure(str(error))
    except Exception:
        current_app.logger.exception("Admin user creation failed")
        return _safe_failure("User could not be created", 500)


@user_bp.route("/users/<int:user_id>", methods=["GET"])
@login_required
def get_user(user_id):
    actor = current_user()
    if actor.role != "admin" and actor.id != user_id:
        return jsonify({"error": "Forbidden"}), 403
    user = db.session.get(User, user_id)
    if not user or not user.is_active:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_dict()), 200


@user_bp.route("/users/<int:user_id>", methods=["PUT"])
@admin_required
def update_user(user_id):
    try:
        user = db.session.get(User, user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404
        data = _json_body()
        if "name" in data:
            user.name = clean_text(data["name"], "Name", minimum=2, maximum=100)
        if "email" in data:
            email = normalize_email(data["email"])
            if User.query.filter(User.email == email, User.id != user.id).first():
                return jsonify({"error": "Email already registered"}), 409
            user.email = email
        if "phone" in data:
            user.phone = clean_text(data["phone"], "Phone", maximum=20)
        if "role" in data:
            user.role = normalize_role(data["role"])
        if "skills" in data:
            user.skills = clean_text(data["skills"], "Skills", maximum=2000)
        if "achievements" in data:
            user.achievements = clean_text(data["achievements"], "Achievements", maximum=4000)
        if data.get("password"):
            user.set_password(validate_password(data["password"]))
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except ValueError as error:
        return _safe_failure(str(error))
    except Exception:
        current_app.logger.exception("User update failed")
        return _safe_failure("User could not be updated", 500)


@user_bp.route("/users/<int:user_id>", methods=["DELETE"])
@admin_required
def delete_user(user_id):
    actor = current_user()
    if actor.id == user_id:
        return jsonify({"error": "Administrators cannot deactivate their own active session"}), 400
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user.is_active = False
    db.session.commit()
    return jsonify({"message": "User deactivated"}), 200


@user_bp.route("/users/profile", methods=["PUT"])
@login_required
def update_profile():
    try:
        user = current_user()
        data = _json_body()
        if "name" in data:
            user.name = clean_text(data["name"], "Name", minimum=2, maximum=100)
        if "phone" in data:
            user.phone = clean_text(data["phone"], "Phone", maximum=20)
        if "skills" in data:
            user.skills = clean_text(data["skills"], "Skills", maximum=2000)
        if "achievements" in data:
            user.achievements = clean_text(data["achievements"], "Achievements", maximum=4000)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    except ValueError as error:
        return _safe_failure(str(error))
    except Exception:
        current_app.logger.exception("Profile update failed")
        return _safe_failure("Profile could not be updated", 500)
