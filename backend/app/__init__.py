from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from app.models import db
from app.routes import register_blueprints
from app.config import Config
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Enable CORS for all routes
    CORS(app)
    
    # Initialize SQLAlchemy
    db.init_app(app)
    
    # Initialize Flask-Smorest Api
    api = Api(app)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Register blueprints from the new routes directory
    register_blueprints(api)
    
    # Create tables if they don't exist
    with app.app_context():
        db.create_all()
        
    return app
