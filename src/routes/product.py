from flask import Blueprint, jsonify, request
from src.models.user import Product, db
from src.routes.auth import login_required, admin_required

product_bp = Blueprint('product', __name__)

@product_bp.route('/products', methods=['GET'])
@login_required
def get_products():
    try:
        products = Product.query.filter_by(is_active=True).all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products', methods=['POST'])
@admin_required
def create_product():
    try:
        data = request.json
        
        product = Product(
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            image=data.get('image', ''),
            category=data.get('category', '')
        )
        
        db.session.add(product)
        db.session.commit()
        return jsonify(product.to_dict()), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        if not product.is_active:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify(product.to_dict()), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@admin_required
def update_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        data = request.json
        
        product.name = data.get('name', product.name)
        product.description = data.get('description', product.description)
        product.price = float(data.get('price', product.price))
        product.image = data.get('image', product.image)
        product.category = data.get('category', product.category)
        
        db.session.commit()
        return jsonify(product.to_dict()), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    try:
        product = Product.query.get_or_404(product_id)
        product.is_active = False  # Soft delete
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/categories', methods=['GET'])
@login_required
def get_categories():
    try:
        categories = db.session.query(Product.category).filter(
            Product.is_active == True,
            Product.category != None,
            Product.category != ''
        ).distinct().all()
        
        category_list = [cat[0] for cat in categories if cat[0]]
        return jsonify(category_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@product_bp.route('/products/category/<category>', methods=['GET'])
@login_required
def get_products_by_category(category):
    try:
        products = Product.query.filter_by(category=category, is_active=True).all()
        return jsonify([product.to_dict() for product in products]), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

