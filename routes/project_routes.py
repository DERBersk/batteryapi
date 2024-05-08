from flask import Blueprint, jsonify, request
from models.project import Project
from models.product import Product
from models.products_per_project import ProductsPerProject

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

###################################################
# Get for multiple projects
###################################################
@project_bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.serialize() for project in projects])

###################################################
# Get for a single project
###################################################
@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.filter(Project.id == project_id).first()
    if project:
        products = Product.query.join(ProductsPerProject)\
                                .join(Project)\
                                .filter(ProductsPerProject.project_id==project_id)\
                                .filter(Product.id==ProductsPerProject.product_id)\
                                .add_columns(Product.id,Product.description,Product.specification,ProductsPerProject.amount,ProductsPerProject.raw_material_type,ProductsPerProject.component_parts_type)\
                                .all()
        print(products)
        products_list = []
        for product in products:
            products_list.append(
                {
                    'id': product.id,
                    'description': product.description,
                    'specification': product.specification,
                    'amount': product.amount,
                    'raw_material_type': product.raw_material_type,
                    'component_parts_type': product.component_parts_type
                }
            )
        project_data = {
                'id': project.id,
                'partner': project.partner,
                'start_date': project.start_date,
                'end_date': project.end_date,
                'production_schedule': project.production_schedule,
                'machine_labor_availability': project.machine_labor_availability,
                'materials': products_list
        }
        return jsonify(project_data), 200
    else:
        return jsonify({'message': f'Project with id {project_id} not found'}), 404

###################################################
# Post a single or multiple project
###################################################
@project_bp.route('/', methods=['POST'])
def create_or_update_project():
    from app import db
    data = request.json

    if not isinstance(data, list):
        return jsonify({'message': 'Invalid data format. Expected a list of projects.'}), 400

    for project_data in data:
        # Extract project data
        project_data = {
            'partner': project_data.get('partner'),
            'start_date': project_data.get('start_date'),
            'end_date': project_data.get('end_date'),
            'production_schedule': project_data.get('production_schedule'),
            'machine_labor_availability': project_data.get('machine_labor_availability')
        }

        # Create or update project
        if 'id' in project_data:
            project = Project.query.get(project_data['id'])
            if not project:
                return jsonify({'message': f'Project with id {project_data["id"]} not found'}), 404
            for key, value in project_data.items():
                setattr(project, key, value)
        else:
            project = Project(**project_data)

        db.session.add(project)

        # Extract products data
        products_data = project_data.get('products', [])
        ProductsPerProject.query.filter(ProductsPerProject.project_id == project.id).delete()
        for product_data in products_data:
            product_id = product_data.get('id')
            if product_id:
                product = Product.query.get(product_id)
                if not product:
                    return jsonify({'message': f'Product with id {product_id} not found'}), 404
            else:
                product = Product()
            
            product.description = product_data.get('description')
            product.specification = product_data.get('specification')

            # Add or update ProductsPerProject
            amount = product_data.get('amount')
            raw_material_type = product_data.get('raw_material_type')
            component_parts_type = product_data.get('component_parts_type')

            products_per_project = ProductsPerProject(
                project_id=project.id,
                product_id=product.id,
                amount=amount,
                raw_material_type=raw_material_type,
                component_parts_type=component_parts_type
            )
            db.session.add(products_per_project)

    db.session.commit()

    return jsonify({'message': 'Projects created/updated successfully'}), 200

###################################################
# Delete a single project
###################################################
@project_bp.route('/<int:project_id>', methods=['DELETE'])
def delete_project(project_id):
    from app import db
    project = Project.query.get(project_id)
    if project:
        # Delete from the database
        ProductsPerProject.query.filter_by(ProductsPerProject.project_id==project_id).delete()
        
        db.session.delete(project)
        db.session.commit()
        return jsonify({'message': 'Project and associated records deleted successfully'}), 200
    else:
        return jsonify({'error': 'Project not found'}), 404