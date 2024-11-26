# app.py
import os
from flask import Flask
from flask_migrate import Migrate
from models.user_model import db
from routes.user_route import user_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Function to initialize the database
def init_db():
    with app.app_context():
        if not db.engine.dialect.has_table(db.engine, 'users'):  
            db.create_all()  # Create tables if they don't exist
            print("Database created successfully.")
        else:
            print("Database already exists. No changes made.")

# Register blueprints for routing
app.register_blueprint(user_bp)

@app.route('/')
def home():
    """Home route for the Flask application."""
    return '<h1>MY SIMPLE FLASK APP</h1>'

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)