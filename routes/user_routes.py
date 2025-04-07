from flask import Blueprint, request, jsonify
from models import db, User
from datetime import datetime
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/signup', methods=['POST'])
def signup_user():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    date_of_birth_str = data.get('date_of_birth')
    gender = data.get('gender', '').capitalize()
    email = data.get('email')
    password = data.get('password')

    if gender not in ['Male', 'Female', 'Other']:
        return jsonify({'error': 'Invalid gender. Must be Male, Female, or Other'}), 400
    
    if not (first_name and last_name and date_of_birth_str and gender and email and password):
        return jsonify({'error': 'All fields are required'}), 400

    try:
        date_of_birth = datetime.strptime(date_of_birth_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'error': 'User already exists'}), 409

    new_user = User(
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        gender=gender,
        email=email
    )
    new_user.set_password(password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({'error': 'Email and password are required'}), 400
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        access_token = user.generate_token()
        return jsonify({'message': 'Login successful', 'access_token': access_token,  'user_id': user.id }), 200
    else:
        return jsonify({'error': 'Invalid email or password'}), 401


@bp.route('/profile', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    return jsonify({'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'date_of_birth': str(user.date_of_birth), 'gender': user.gender, 'created_at': str(user.created_at), 'updated_at': str(user.updated_at)}), 200


@bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    required_fields = ['first_name', 'last_name', 'email', 'date_of_birth', 'gender']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'All fields are required'}), 400
    
    if data['gender'] not in ['Male', 'Female', 'Other']:
        return jsonify({'error': 'Invalid gender. Must be Male, Female, or Other'}), 400
    
    if data['email'] != user.email:
        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({'error': 'Email already exists'}), 409

    try:
        date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400
    
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.date_of_birth = date_of_birth
    user.gender = data['gender']
    
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'date_of_birth': str(user.date_of_birth), 'gender': user.gender, 'updated_at': str(user.updated_at)}}), 200
 

@bp.route('/profile', methods=['PATCH'])
@jwt_required()
def patch_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    
    if not user:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'Invalid input'}), 400

    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        if data['email'] != user.email:
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({'error': 'Email already exists'}), 409
        user.email = data['email']
    if 'date_of_birth' in data:
        try:
            user.date_of_birth = datetime.strptime(data['date_of_birth'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({'error': 'Invalid date format, use YYYY-MM-DD'}), 400
    if 'gender' in data:
        if data['gender'] not in ['Male', 'Female', 'Other']:
            return jsonify({'error': 'Invalid gender. Must be Male, Female, or Other'}), 400
        user.gender = data['gender']
    if 'password' in data:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify({'message': 'User updated successfully', 'user': {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email, 'date_of_birth': str(user.date_of_birth), 'gender': user.gender, 'updated_at': str(user.updated_at)}}), 200
  
@bp.route('/profile', methods=['DELETE'])
@jwt_required()
def delete_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(int(current_user_id))
    if not user:
        return jsonify({'error': 'User not found'}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200