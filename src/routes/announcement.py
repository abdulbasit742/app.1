from flask import Blueprint, jsonify, request, session
from src.models.user import Announcement, User, db
from src.routes.auth import login_required, admin_required

announcement_bp = Blueprint('announcement', __name__)

@announcement_bp.route('/announcements', methods=['GET'])
@login_required
def get_announcements():
    try:
        announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.date.desc()).all()
        result = []
        for announcement in announcements:
            announcement_dict = announcement.to_dict()
            # Get creator name
            creator = User.query.get(announcement.created_by)
            announcement_dict['created_by_name'] = creator.name if creator else 'Unknown'
            result.append(announcement_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@announcement_bp.route('/announcements', methods=['POST'])
@admin_required
def create_announcement():
    try:
        data = request.json
        
        announcement = Announcement(
            title=data['title'],
            description=data.get('description', ''),
            created_by=session['user_id']
        )
        
        db.session.add(announcement)
        db.session.commit()
        
        # Return with creator name
        result = announcement.to_dict()
        creator = User.query.get(announcement.created_by)
        result['created_by_name'] = creator.name if creator else 'Unknown'
        
        return jsonify(result), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@announcement_bp.route('/announcements/<int:announcement_id>', methods=['GET'])
@login_required
def get_announcement(announcement_id):
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        if not announcement.is_active:
            return jsonify({'error': 'Announcement not found'}), 404
        
        result = announcement.to_dict()
        creator = User.query.get(announcement.created_by)
        result['created_by_name'] = creator.name if creator else 'Unknown'
        
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@announcement_bp.route('/announcements/<int:announcement_id>', methods=['PUT'])
@admin_required
def update_announcement(announcement_id):
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        data = request.json
        
        announcement.title = data.get('title', announcement.title)
        announcement.description = data.get('description', announcement.description)
        
        db.session.commit()
        
        result = announcement.to_dict()
        creator = User.query.get(announcement.created_by)
        result['created_by_name'] = creator.name if creator else 'Unknown'
        
        return jsonify(result), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@announcement_bp.route('/announcements/<int:announcement_id>', methods=['DELETE'])
@admin_required
def delete_announcement(announcement_id):
    try:
        announcement = Announcement.query.get_or_404(announcement_id)
        announcement.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({'message': 'Announcement deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@announcement_bp.route('/announcements/recent', methods=['GET'])
@login_required
def get_recent_announcements():
    try:
        announcements = Announcement.query.filter_by(is_active=True).order_by(Announcement.date.desc()).limit(5).all()
        result = []
        for announcement in announcements:
            announcement_dict = announcement.to_dict()
            creator = User.query.get(announcement.created_by)
            announcement_dict['created_by_name'] = creator.name if creator else 'Unknown'
            result.append(announcement_dict)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

