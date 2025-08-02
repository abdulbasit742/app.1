from flask import Blueprint, jsonify, request
from src.models.user import Contact, db
from src.routes.auth import admin_required

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('/contact', methods=['POST'])
def create_contact():
    try:
        data = request.json
        
        contact = Contact(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )
        
        db.session.add(contact)
        db.session.commit()
        return jsonify({
            'message': 'Contact form submitted successfully',
            'contact': contact.to_dict()
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts', methods=['GET'])
@admin_required
def get_contacts():
    try:
        contacts = Contact.query.order_by(Contact.created_at.desc()).all()
        return jsonify([contact.to_dict() for contact in contacts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/<int:contact_id>', methods=['GET'])
@admin_required
def get_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        return jsonify(contact.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/<int:contact_id>/read', methods=['PUT'])
@admin_required
def mark_contact_read(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        contact.is_read = True
        db.session.commit()
        return jsonify(contact.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/<int:contact_id>', methods=['DELETE'])
@admin_required
def delete_contact(contact_id):
    try:
        contact = Contact.query.get_or_404(contact_id)
        db.session.delete(contact)
        db.session.commit()
        return jsonify({'message': 'Contact deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/unread', methods=['GET'])
@admin_required
def get_unread_contacts():
    try:
        contacts = Contact.query.filter_by(is_read=False).order_by(Contact.created_at.desc()).all()
        return jsonify([contact.to_dict() for contact in contacts]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@contact_bp.route('/contacts/stats', methods=['GET'])
@admin_required
def get_contact_stats():
    try:
        total = Contact.query.count()
        unread = Contact.query.filter_by(is_read=False).count()
        return jsonify({
            'total': total,
            'unread': unread,
            'read': total - unread
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

