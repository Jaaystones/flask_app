# controllers/user_controller.py

from datetime import datetime
from flask import jsonify
from sqlalchemy.exc import IntegrityError
from models.user_model import UserModel, db

def create_user(data):
    """Create a new user."""
    try:
        user_date = datetime.strptime(data['date'], '%Y-%m-%d')
    except ValueError as e:
        return {"error": f"Invalid date format: {str(e)}"}, 400

    new_user = UserModel(
        name=data['name'],
        email=data['email'],
        city=data['city'],
        date=user_date
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return {"message": "User created successfully", "user": data}, 201
    except IntegrityError:
        db.session.rollback()
        return {"error": "User already exists"}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def get_users():
    """Retrieve all users."""
    users = UserModel.query.all()
    return [{
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "city": user.city,
        "date": user.date.strftime('%Y-%m-%d')
    } for user in users], 200

def update_user(user_id, data):
    """Update an existing user's details."""
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User not found."}, 404

    # Update fields if they are provided in the data
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'city' in data:
        user.city = data['city']
    if 'date' in data:
        date_value = data.get('date')  # Safely get the date value
        if date_value:  # Only parse if the date value is not empty or None
            try:
                user.date = datetime.strptime(date_value, '%Y-%m-%d')
            except ValueError as e:
                return {"error": f"Invalid date format: {str(e)}"}, 400
    try:
        db.session.commit()
        return {
            "message": "User updated successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "city": user.city,
                "date": user.date.strftime('%Y-%m-%d') if user.date else None
            }
        }, 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "User with this name or email already exists."}, 400
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500

def delete_user(user_id):
    """Delete a specific user by ID."""
    user = UserModel.query.get(user_id)
    if not user:
        return {"error": "User not found."}, 404

    try:
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully."}, 200
    except Exception as e:
        db.session.rollback()
        return {"error": str(e)}, 500