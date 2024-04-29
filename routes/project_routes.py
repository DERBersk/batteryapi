from flask import Blueprint, jsonify, request
from models.project import Project

project_bp = Blueprint('project', __name__, url_prefix='/api/projects')

@project_bp.route('/', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([project.serialize() for project in projects])

@project_bp.route('/', methods=['POST'])
def create_project():
    from app import db
    data = request.get_json()
    new_project = Project(name=data['name'])
    db.session.add(new_project)
    db.session.commit()
    return jsonify(new_project.serialize()), 201