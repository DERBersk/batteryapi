# import external packages
from flask import Blueprint, jsonify, request
from sqlalchemy import func
# import functions and data
from extensions import db
# import models
from models.product import Product
from models.material import Material
from models.materials_per_product import MaterialsPerProduct
from models.products_per_project import ProductsPerProject
from models.external_production_data import ExternalProductionData
from models.week import Week


product_bp = Blueprint('product', __name__, url_prefix='/api/products')

###################################################
# Get for multiple products
###################################################
@product_bp.route('/', methods=['GET'])
def get_products():
    # Subquery to count the materials per product
    material_counts = db.session.query(
        MaterialsPerProduct.product_id,
        func.count(MaterialsPerProduct.material_id).label('material_count')
    ).group_by(MaterialsPerProduct.product_id).subquery()

    # Main query joining the product and material counts
    products_query = db.session.query(
        Product,
        material_counts.c.material_count
    ).outerjoin(material_counts, material_counts.c.product_id == Product.id) \
    .order_by(Product.id.asc())

    # Fetch results and prepare data
    products_data = []
    for product, material_count in products_query:
        product_data = product.serialize()
        product_data['material_count'] = material_count
        products_data.append(product_data)

    return jsonify(products_data)

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
                                  .add_columns(Material.id,Material.name,Material.safety_stock,Material.lot_size,Material.stock_level,MaterialsPerProduct.amount,Material.unit,Material.external_id)\
                                  .order_by(Material.id.asc())\
                                  .all()
        external_production = ExternalProductionData.query.join(Product)\
                                                        .join(Week)\
                                                        .filter(ExternalProductionData.product_id == Product.id)\
                                                        .filter(ExternalProductionData.week_id == Week.id)\
                                                        .filter(ExternalProductionData.product_id == product_id)\
                                                        .add_columns(Week.week, Week.year, ExternalProductionData.amount)\
                                                        .order_by(Week.year, Week.week)\
                                                        .all()
        
        external_production_list = []
        for prod in external_production:
            external_production_list.append(
                {
                    'week': prod.week,
                    'year': prod.year,
                    'amount': prod.amount
                }
            )
        
        
        materials_list = []
        for material in materials:
            materials_list.append(
                {
                    'id': material.id,
                    'name': material.name,
                    'safety_stock': material.safety_stock,
                    'lot_size': material.lot_size,
                    'stock_level': material.stock_level,
                    'amount': material.amount,
                    'unit': material.unit.value,
                    'external_id': material.external_id
                }
            )
        product_data = {
                'id': product.id,
                'description': product.description,
                'specification': product.specification,
                'external_id': product.external_id,
                'materials': materials_list,
                'external_production': external_production_list
        }
        return jsonify(product_data), 200
    else:
        return jsonify({'message': f'Product with id {product_id} not found'}), 404

###################################################
# Post a single or multiple products
###################################################
@product_bp.route('', methods=['POST'])
def create_or_update_products():
    from app import db
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of products.'}), 400

    for product_data in data:

        # Create or update product
        if 'id' in product_data and product_data.get('id') != None:
            product = Product.query.get(product_data['id'])
            if not product:
                return jsonify({'message': f'Product with id {product_data["id"]} not found'}), 404
            for key, value in product_data.items():
                if key != 'id' and key != 'materials':
                    setattr(product, key, value)
        else:
            product = Product(**{k: v for k, v in product_data.items() if k != 'materials'})

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

            # Add or update MaterialsPerProduct
            amount = material_data.get('amount')

            materials_per_product = MaterialsPerProduct(
                product_id=product.id,
                material_id=material_id,
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