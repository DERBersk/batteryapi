from flask import Blueprint, jsonify, request
from datetime import datetime
from models.user import User

user_bp = Blueprint('user', __name__, url_prefix='/api/user')

###################################################
# Get for multiple Users
###################################################
@user_bp.route('/', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users])

###################################################
# Get for a single User
###################################################
@user_bp.route('/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter(User.id == user_id).first()
    if user:
        return jsonify(user.serialize())
    else:
        return jsonify({'message': f'User with id {user_id} not found'}), 404

###################################################
# Post a single user
###################################################
@user_bp.route('/', methods=['POST'])
def create_user():
    from app import db
    data = request.get_json()

    if 'id' in data:
        user = User.query.get(data['id'])
        if not user:
            return jsonify({'error': f'User with id {data["id"]} not found'}), 404
        # Update existing user
        for key, value in data.items():
            setattr(user, key, value)
    else:
        # Create new user
        new_user = User(
            email=data.get('email'),
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            created_date= datetime.strptime(data.get('created_date'),'%m-%d-%y').date()
        )
        db.session.add(new_user)

    db.session.commit()
    
    return jsonify({'message': 'User created/updated successfully'}), 201

###################################################
# Delete a single user
###################################################
@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    from app import db
    user = User.query.get(user_id)
    if user:
        # Delete from the database
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted successfully'}), 200
    else:
        return jsonify({'error': 'User not found'}), 404