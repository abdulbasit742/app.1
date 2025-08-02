from flask import Blueprint, jsonify, request
from src.models.user import Service, db
from src.routes.auth import login_required, admin_required

service_bp = Blueprint('service', __name__)

@service_bp.route('/services', methods=['GET'])
@login_required
def get_services():
    try:
        services = Service.query.filter_by(is_active=True).all()
        return jsonify([service.to_dict() for service in services]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@service_bp.route('/services', methods=['POST'])
@admin_required
def create_service():
    try:
        data = request.json
        
        service = Service(
            name=data['name'],
            description=data.get('description', ''),
            contact_info=data.get('contact_info', ''),
            price=float(data['price']) if data.get('price') else None
        )
        
        db.session.add(service)
        db.session.commit()
        return jsonify(service.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@service_bp.route('/services/<int:service_id>', methods=['GET'])
@login_required
def get_service(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        if not service.is_active:
            return jsonify({'error': 'Service not found'}), 404
        return jsonify(service.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@service_bp.route('/services/<int:service_id>', methods=['PUT'])
@admin_required
def update_service(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        data = request.json
        
        service.name = data.get('name', service.name)
        service.description = data.get('description', service.description)
        service.contact_info = data.get('contact_info', service.contact_info)
        service.price = float(data['price']) if data.get('price') else service.price
        
        db.session.commit()
        return jsonify(service.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@service_bp.route('/services/<int:service_id>', methods=['DELETE'])
@admin_required
def delete_service(service_id):
    try:
        service = Service.query.get_or_404(service_id)
        service.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({'message': 'Service deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

