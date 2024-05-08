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
@product_bp.route('/', methods=['POST'])
def create_or_update_products():
    from app import db
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of products.'}), 400

    for product_data in data:
        # Extract product data
        product_data = {
            'description': product_data.get('description'),
            'specification': product_data.get('specification')
        }

        # Create or update product
        if 'id' in product_data:
            product = Product.query.get(product_data['id'])
            if not product:
                return jsonify({'message': f'Product with id {product_data["id"]} not found'}), 404
            for key, value in product_data.items():
                setattr(product, key, value)
        else:
            product = Product(**product_data)

        db.session.add(product)

        # Extract materials data
        materials_data = product_data.get('materials', [])
        MaterialsPerProduct.query.filter(MaterialsPerProduct.product_id == product.id).delete()
        for material_data in materials_data:
            material_id = material_data.get('id')
            if material_id:
                material = Material.query.get(material_id)
                if not material:
                    return jsonify({'message': f'Material with id {material_id} not found'}), 404
            else:
                material = Material()

            material.name = material_data.get('name')
            material.safety_stock = material_data.get('safety_stock')
            material.lot_size = material_data.get('lot_size')
            material.stock_level = material_data.get('stock_level')

            # Add or update MaterialsPerProduct
            amount = material_data.get('amount')

            materials_per_product = MaterialsPerProduct(
                product_id=product.id,
                material_id=material.id,
                amount=amount
            )
            db.session.add(materials_per_product)

    db.session.commit()

    return jsonify({'message': 'Products created/updated successfully'}), 200

###################################################
# Delete a single product
###################################################
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    from app import db
    product = Product.query.get(product_id)
    if product:
        # Delete from the database
        MaterialsPerProduct.query.filter_by(MaterialsPerProduct.product_id==product_id).delete()
        
        ProductsPerProject.query.filter_by(ProductsPerProject.product_id==product_id).delete()
        
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Product not found'}), 404