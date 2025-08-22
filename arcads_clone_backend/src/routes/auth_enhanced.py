from flask import Blueprint, request, jsonify, session, url_for, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash
import jwt
import secrets
import requests
from datetime import datetime, timedelta
import os

from ..models.user import User, db
from ..models.subscription import UsageLog

auth_enhanced_bp = Blueprint('auth_enhanced', __name__)

def generate_jwt_token(user_id):
    """Generate JWT token for user authentication"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=7),  # Token expires in 7 days
        'iat': datetime.utcnow()
    }
    secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_jwt_token(token):
    """Verify JWT token and return user_id"""
    try:
        secret_key = os.getenv('JWT_SECRET_KEY', 'your-secret-key-here')
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def log_user_action(user_id, action, metadata=None):
    """Log user action for analytics"""
    try:
        log = UsageLog(
            user_id=user_id,
            action=action,
            log_metadata=metadata,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"Error logging user action: {e}")

@auth_enhanced_bp.route('/register', methods=['POST'])
def register():
    """Register a new user with email and password"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'message': f'{field.replace("_", " ").title()} is required'
                }), 400
        
        email = data['email'].lower().strip()
        
        # Check if user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({
                'success': False,
                'message': 'User with this email already exists'
            }), 409
        
        # Create new user
        user = User(
            email=email,
            first_name=data['first_name'].strip(),
            last_name=data.get('last_name', '').strip(),
            company=data.get('company', '').strip(),
            auth_provider='email'
        )
        user.set_password(data['password'])
        
        db.session.add(user)
        db.session.commit()
        
        # Generate JWT token
        token = generate_jwt_token(user.id)
        
        # Log registration
        log_user_action(user.id, 'user_registered', {
            'auth_provider': 'email',
            'email': email
        })
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Registration failed: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/login', methods=['POST'])
def login():
    """Login user with email and password"""
    try:
        data = request.get_json()
        
        email = data.get('email', '').lower().strip()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({
                'success': False,
                'message': 'Email and password are required'
            }), 400
        
        # Find user
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            return jsonify({
                'success': False,
                'message': 'Invalid email or password'
            }), 401
        
        # Update last login
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        token = generate_jwt_token(user.id)
        
        # Log login
        log_user_action(user.id, 'user_login', {
            'auth_provider': 'email',
            'email': email
        })
        
        return jsonify({
            'success': True,
            'message': 'Login successful',
            'data': {
                'user': user.to_dict(),
                'token': token
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Login failed: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/google/login', methods=['POST'])
def google_login():
    """Handle Google OAuth login (demo mode)"""
    try:
        data = request.get_json()
        
        # For demo purposes, create a mock Google user
        # In production, this would handle actual Google OAuth tokens
        
        mock_google_user = {
            'email': 'demo@google.com',
            'first_name': 'Demo',
            'last_name': 'User',
            'avatar_url': 'https://via.placeholder.com/150',
            'google_id': 'demo_google_id_123'
        }
        
        email = mock_google_user['email']
        
        # Find or create user
        user = User.query.filter_by(email=email).first()
        if not user:
            user = User(
                email=email,
                first_name=mock_google_user['first_name'],
                last_name=mock_google_user['last_name'],
                avatar_url=mock_google_user['avatar_url'],
                google_id=mock_google_user['google_id'],
                auth_provider='google',
                email_verified=True
            )
            db.session.add(user)
        else:
            # Update existing user with Google info
            user.google_id = mock_google_user['google_id']
            user.auth_provider = 'google'
            user.email_verified = True
            if not user.avatar_url:
                user.avatar_url = mock_google_user['avatar_url']
        
        user.last_login = datetime.utcnow()
        db.session.commit()
        
        # Generate JWT token
        token = generate_jwt_token(user.id)
        
        # Log login
        log_user_action(user.id, 'user_login', {
            'auth_provider': 'google',
            'email': email
        })
        
        return jsonify({
            'success': True,
            'message': 'Google login successful (demo mode)',
            'data': {
                'user': user.to_dict(),
                'token': token,
                'demo_mode': True
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Google login failed: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/verify-token', methods=['POST'])
def verify_token():
    """Verify JWT token"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({
                'success': False,
                'message': 'Token is required'
            }), 400
        
        user_id = verify_jwt_token(token)
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict(),
                'valid': True
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Token verification failed: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset email"""
    try:
        data = request.get_json()
        email = data.get('email', '').lower().strip()
        
        if not email:
            return jsonify({
                'success': False,
                'message': 'Email is required'
            }), 400
        
        user = User.query.filter_by(email=email).first()
        if user:
            # Generate reset token
            reset_token = secrets.token_urlsafe(32)
            user.reset_token = reset_token
            user.reset_token_expires = datetime.utcnow() + timedelta(hours=1)
            db.session.commit()
            
            # In production, send email here
            # For demo, just return success
            
        # Always return success for security (don't reveal if email exists)
        return jsonify({
            'success': True,
            'message': 'If an account with that email exists, a password reset link has been sent'
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Password reset failed: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password with token"""
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        if not token or not new_password:
            return jsonify({
                'success': False,
                'message': 'Token and new password are required'
            }), 400
        
        user = User.query.filter_by(reset_token=token).first()
        if not user or not user.reset_token_expires or user.reset_token_expires < datetime.utcnow():
            return jsonify({
                'success': False,
                'message': 'Invalid or expired reset token'
            }), 400
        
        # Update password
        user.set_password(new_password)
        user.reset_token = None
        user.reset_token_expires = None
        db.session.commit()
        
        # Log password reset
        log_user_action(user.id, 'password_reset')
        
        return jsonify({
            'success': True,
            'message': 'Password reset successful'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Password reset failed: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/profile', methods=['GET'])
def get_profile():
    """Get user profile"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'Authorization token is required'
            }), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_jwt_token(token)
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get profile: {str(e)}'
        }), 500

@auth_enhanced_bp.route('/profile', methods=['PUT'])
def update_profile():
    """Update user profile"""
    try:
        # Get token from Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({
                'success': False,
                'message': 'Authorization token is required'
            }), 401
        
        token = auth_header.split(' ')[1]
        user_id = verify_jwt_token(token)
        
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Invalid or expired token'
            }), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        data = request.get_json()
        
        # Update allowed fields
        if 'first_name' in data:
            user.first_name = data['first_name'].strip()
        if 'last_name' in data:
            user.last_name = data['last_name'].strip()
        if 'company' in data:
            user.company = data['company'].strip()
        
        user.updated_at = datetime.utcnow()
        db.session.commit()
        
        # Log profile update
        log_user_action(user.id, 'profile_updated')
        
        return jsonify({
            'success': True,
            'message': 'Profile updated successfully',
            'data': {
                'user': user.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Profile update failed: {str(e)}'
        }), 500

