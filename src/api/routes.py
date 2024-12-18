from flask import Blueprint, jsonify
from src.utils.helpers import handle_exceptions

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
@handle_exceptions
def health_check():
    return jsonify({"status": "healthy"})

# API routes will be implemented based on your requirements
# Example:
# @api_bp.route('/your-endpoint', methods=['GET'])
# @handle_exceptions
# def your_endpoint():
#     return jsonify({"message": "Your response"})
