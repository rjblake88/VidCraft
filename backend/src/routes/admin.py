from flask import Blueprint, request, jsonify
from ..models.user import User, db
from ..routes.auth_enhanced import verify_jwt_token

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/set-admin', methods=['POST'])
def set_admin():
    """Set a user as admin - for initial setup only"""
    try:
        data = request.get_json()
        email = data.get('email')
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        # Find user by email
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        # Set user as admin
        user.role = 'admin'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'User {email} has been set as admin',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to set admin: {str(e)}'
        }), 500

@admin_bp.route('/check-admin', methods=['GET'])
def check_admin():
    """Check if current user is admin"""
    try:
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'No authentication token provided'
            }), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_jwt_token(token)
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Invalid token'
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'is_admin': user.is_admin(),
            'can_access_analytics': user.can_access_analytics(),
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to check admin status: {str(e)}'
        }), 500

