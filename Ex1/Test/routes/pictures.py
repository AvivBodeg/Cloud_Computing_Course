"""
Routes for /pictures/{file-name}
"""
from flask import Blueprint, send_file, jsonify
import os

pictures_bp = Blueprint('pictures', __name__)


@pictures_bp.route('/pictures/<filename>', methods=['GET'])
def get_picture(filename):
    """Get a picture file"""
    filepath = f"pictures/{filename}"
    
    if not os.path.exists(filepath):
        return jsonify({"error": "Not found"}), 404
    
    # Determine MIME type based on extension
    ext = filename.split('.')[-1].lower()
    mimetype = 'image/jpeg'  # Default
    
    if ext == 'png':
        mimetype = 'image/png'
    elif ext in ['jpg', 'jpeg']:
        mimetype = 'image/jpeg'
    elif ext == 'gif':
        mimetype = 'image/gif'
    
    return send_file(filepath, mimetype=mimetype)
