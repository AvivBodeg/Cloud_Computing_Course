"""
Pet Store REST API - Main Application
"""
from flask import Flask
from routes.pet_types import pet_types_bp
from routes.pets import pets_bp
from routes.pictures import pictures_bp
import os

app = Flask(__name__)

# Register blueprints
app.register_blueprint(pet_types_bp)
app.register_blueprint(pets_bp)
app.register_blueprint(pictures_bp)

# Create pictures directory if it doesn't exist
if not os.path.exists('pictures'):
    os.makedirs('pictures')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
