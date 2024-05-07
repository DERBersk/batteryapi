from flask import Blueprint, jsonify, request
from models.product import Product
from models.material import Material
from models.materials_per_product import MaterialsPerProduct
from models.products_per_project import ProductsPerProject


product_bp = Blueprint('product', __name__, url_prefix='/api/products')

###################################################
# Get for multiple products
###################################################
@product_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([product.serialize() for product in products])

###################################################
# Get for a single product
###################################################
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    if product:
        materials = Material.query.join(MaterialsPerProduct)\
                                  .join(Product)\
                                  .filter(MaterialsPerProduct.product_id==product_id)\
                                  .filter(Material.id==MaterialsPerProduct.material_id)\
                                  .add_columns(Material.id,Material.name,Material.safety_stock,Material.lot_size,Material.stock_level,MaterialsPerProduct.amount)\
                                  .all()
        materials_list = []
        for material in materials:
            materials_list.append(
                {
                    'id': material.id,
                    'name': material.name,
                    'safety_stock': material.safety_stock,
                    'lot_size': material.lot_size,
                    'stock_level': material.stock_level,
                    'amount': material.amount
                }
            )
        product_data = {
                'id': product.id,
                'description': product.description,
                'specification': product.specification,
                'materials': materials_list
        }
        return jsonify(product_data), 200
    else:
        return jsonify({'message': f'Product with id {product_id} not found'}), 404

###################################################
# Post a single or multiple products
###################################################
def create_products():
    from app import db
    data = request.get_json()

    if not isinstance(data, list):
        return jsonify({'error': 'JSON payload must be a list of products'}), 400

    new_products = []
    for product_data in data:
        new_product = Product(
            description=product_data.get('description'),
            specification=product_data.get('specification')
        )
        new_products.append(new_product)
        db.session.add(new_product)

    db.session.commit()

    serialized_products = [product.serialize() for product in new_products]
    return jsonify(serialized_products), 201

###################################################
# Delete a single product
###################################################
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    from app import db
    product = Product.query.get(product_id)
    if product:
        # Delete from the database
        MaterialsPerProduct.query.filter_by(product_id=product_id).delete()
        
        ProductsPerProject.query.filter_by(product_id=product_id).delete()
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404