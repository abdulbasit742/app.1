from flask import Blueprint, jsonify, request
from src.models.user import User, db
from src.routes.auth import login_required, admin_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    try:
        users = User.query.filter_by(is_active=True).all()
        return jsonify([user.to_dict() for user in users]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users', methods=['POST'])
@admin_required
def create_user():
    try:
        data = request.json
        
        # Check if user already exists
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        user = User(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', ''),
            role=data.get('role', 'member'),
            skills=data.get('skills', ''),
            achievements=data.get('achievements', '')
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['GET'])
@login_required
def get_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        if not user.is_active:
            return jsonify({'error': 'User not found'}), 404
        return jsonify(user.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        data = request.json
        
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.role = data.get('role', user.role)
        user.skills = data.get('skills', user.skills)
        user.achievements = data.get('achievements', user.achievements)
        
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    try:
        user = User.query.get_or_404(user_id)
        user.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@user_bp.route('/users/profile', methods=['PUT'])
@login_required
def update_profile():
    try:
        from flask import session
        user = User.query.get(session['user_id'])
        data = request.json
        
        user.name = data.get('name', user.name)
        user.phone = data.get('phone', user.phone)
        user.skills = data.get('skills', user.skills)
        user.achievements = data.get('achievements', user.achievements)
        
        db.session.commit()
        return jsonify(user.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

