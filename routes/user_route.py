# routes/user_routes.py

from flask import Blueprint, request, jsonify
from controller.user_controller import create_user, get_users, update_user, delete_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users', methods=['GET'])
def get_users_route():
    """Route to get all users."""
    users, status_code = get_users()
    return jsonify(users), status_code

@user_bp.route('/api/users', methods=['POST'])
def create_user_route():
    """Route to create a new user."""
    data = request.get_json()
    response, status_code = create_user(data)
    return jsonify(response), status_code

@user_bp.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user_route(user_id):
    """Route to update an existing user's details."""
    data = request.get_json()
    response, status_code = update_user(user_id, data)
    return jsonify(response), status_code

@user_bp.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user_route(user_id):
    """Route to delete a specific user by ID."""
    response, status_code = delete_user(user_id)
    return jsonify(response), status_code