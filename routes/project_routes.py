# import external packages
from flask import Blueprint, jsonify, request
from sqlalchemy import func
from sqlalchemy.orm import aliased
# import functions and data
from extensions import db
# import models
from models.project import Project
from models.product import Product
from models.week import Week
from models.products_per_project import ProductsPerProject

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

###################################################
# Get for multiple projects
###################################################
@project_bp.route('/', methods=['GET'])
def get_projects():    
    # Alias the Week table for start and end weeks
    start_week_alias = aliased(Week)
    end_week_alias = aliased(Week)
    
    # Subquery to count the products per project
    product_counts = db.session.query(
        ProductsPerProject.project_id,
        func.count(ProductsPerProject.product_id).label('product_count')
    ).group_by(ProductsPerProject.project_id).subquery()

    # Main query joining all necessary data
    projects_query = db.session.query(
        Project,
        start_week_alias.week.label('start_week'),
        start_week_alias.year.label('start_year'),
        end_week_alias.week.label('end_week'),
        end_week_alias.year.label('end_year'),
        product_counts.c.product_count
    ).join(start_week_alias, start_week_alias.id == Project.start_week) \
     .join(end_week_alias, end_week_alias.id == Project.end_week) \
     .outerjoin(product_counts, product_counts.c.project_id == Project.id) \
     .order_by(Project.id.asc())

    # Fetch results and prepare data
    projects_data = []
    for project, start_week, start_year, end_week, end_year, product_count in projects_query:
        project_data = project.serialize()
        if not product_count:
            product_count = 0
        project_data.update({
            'start_week': start_week,
            'start_year': start_year,
            'end_week': end_week,
            'end_year': end_year,
            'product_count': product_count
        })
        projects_data.append(project_data)

    return jsonify(projects_data)

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
                                .add_columns(Product.id,Product.description,Product.specification,ProductsPerProject.amount,Product.external_id)\
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
                    "external_id": product.external_id
                }
            )
        st_wk = Week.query.filter(Week.id == project.start_week).first()
        en_wk = Week.query.filter(Week.id == project.end_week).first()
        project_data = {
                'id': project.id,
                'partner': project.partner,
                'start_week': st_wk.week,
                'start_year': st_wk.year,
                'end_week': en_wk.week,
                'end_year': en_wk.year,
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
        # Create or update project

        project_start_id = get_project_date_id(project_data.get("start_week"), project_data.get("start_year"))
        project_end_id = get_project_date_id(project_data.get("end_week"), project_data.get("end_year"))
        
        project_start_id = create_or_get_week(project_start_id,project_data.get("start_week"),project_data.get("start_year"),db)
        project_end_id = create_or_get_week(project_end_id,project_data.get("end_week"),project_data.get("end_year"),db)

        if(project_start_id):
            project_data["start_week"] = project_start_id
        
        if(project_end_id):
            project_data["end_week"] = project_end_id
        
        if 'id' in project_data:
            project = Project.query.get(project_data['id'])
            if not project:
                return jsonify({'message': f'Project with id {project_data["id"]} not found'}), 404
            for key, value in project_data.items():
                if key != 'id' and key != 'products':
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
            
            # Add or update ProductsPerProject
            amount = product_data.get('amount')

            products_per_project = ProductsPerProject(
                project_id=project.id,
                product_id=product_id,
                amount=amount,
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

def get_project_date_id(week, year):
    if week and year:
        if(week < 1 or week > 53):
            return jsonify({'message': f'Week number {week} is invalid'}), 501
        return 'wk'+ str(week) + '_' + str(year)
    return None

def create_or_get_week(week_year,w,y,db):
    if(week_year):
        st_wk = Week.query.filter(Week.id == week_year).first()
        if(st_wk):
            return week_year
        else:
            new_week = Week(**{"id": week_year,"week":w,"year":y})
            db.session.add(new_week)
            return week_year
    return None