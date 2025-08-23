from flask import Blueprint, request, jsonify
from datetime import datetime
import requests
import os
import uuid
from src.models.user import User, db
from src.models.project import Project
from src.models.video import GeneratedVideo
from src.routes.auth import verify_token
from .pollo_integration import pollo_client

videos_bp = Blueprint('videos', __name__)

# Pollo AI configuration
POLLO_API_KEY = os.environ.get('POLLO_API_KEY', 'your-pollo-api-key')
POLLO_API_BASE = 'https://api.pollo.ai/v1'

def get_current_user_from_token():
    """Helper function to get current user from JWT token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    user_id = verify_token(token)
    
    if not user_id:
        return None
    
    return User.query.get(user_id)

@videos_bp.route('/models', methods=['GET'])
def get_available_models():
    """Get available video generation models from Pollo AI"""
    try:
        result = pollo_client.get_available_models()
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'models': result['models']
                }
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MODELS_FETCH_ERROR',
                    'message': result.get('error', 'Failed to fetch models')
                }
            }), 500
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'MODELS_FETCH_ERROR',
                'message': str(e)
            }
        }), 500

@videos_bp.route('/generate', methods=['POST'])
def generate_video():
    """Generate video using Pollo AI"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['script', 'model_id', 'actor_id', 'voice_id', 'duration']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'message': f'Missing required field: {field}'
                }), 400
        
        # Extract data
        script = data['script']
        model_id = data['model_id']
        actor_id = data['actor_id']
        voice_id = data['voice_id']
        duration = data['duration']
        settings = data.get('settings', {})
        
        # Create video record
        video_id = str(uuid.uuid4())
        
        # Generate video using Pollo AI
        result = pollo_client.generate_video(
            prompt=script,
            model_id=model_id,
            duration=duration,
            aspect_ratio=settings.get('aspect_ratio', '16:9'),
            quality=settings.get('quality', 'high')
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'video_id': video_id,
                    'pollo_video_id': result['video_id'],
                    'status': 'processing',
                    'message': 'Video generation started successfully'
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('error', 'Failed to start video generation')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@videos_bp.route('/<video_id>/status', methods=['GET'])
def get_video_status(video_id):
    """Get video generation status"""
    try:
        # For demo, extract pollo_video_id from video_id
        # In production, you'd look this up in the database
        pollo_video_id = f"video_{int(datetime.utcnow().timestamp())}"
        
        result = pollo_client.get_video_status(pollo_video_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'video_id': video_id,
                    'status': result['status'],
                    'progress': result.get('progress', 0),
                    'message': result.get('message', ''),
                    'video_url': result.get('video_url'),
                    'thumbnail_url': result.get('thumbnail_url')
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('error', 'Failed to get video status')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@videos_bp.route('/<video_id>', methods=['GET'])
def get_video_result(video_id):
    """Get completed video result"""
    try:
        # For demo, extract pollo_video_id from video_id
        # In production, you'd look this up in the database
        pollo_video_id = f"video_{int(datetime.utcnow().timestamp())}"
        
        result = pollo_client.get_video_result(pollo_video_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'data': {
                    'video_id': video_id,
                    'status': result['status'],
                    'video_url': result['video_url'],
                    'thumbnail_url': result['thumbnail_url'],
                    'duration': result['duration'],
                    'resolution': result['resolution'],
                    'file_size': result['file_size'],
                    'created_at': result['created_at'],
                    'metadata': result['metadata']
                }
            })
        else:
            return jsonify({
                'success': False,
                'message': result.get('error', 'Failed to get video result')
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500

@videos_bp.route('/bulk-generate', methods=['POST'])
def bulk_generate_videos():
    """Generate multiple videos with different variations"""
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Invalid or missing authorization token'
                }
            }), 401
        
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['project_id', 'script', 'variations']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'MISSING_FIELD',
                        'message': f'{field} is required'
                    }
                }), 400
        
        # Verify project belongs to user
        project = Project.query.filter_by(id=data['project_id'], user_id=user.id).first()
        if not project:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'PROJECT_NOT_FOUND',
                    'message': 'Project not found'
                }
            }), 404
        
        variations = data['variations']
        total_credits = len(variations) * 10  # Mock calculation
        
        # Check if user has enough credits
        if user.credits_remaining < total_credits:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'INSUFFICIENT_CREDITS',
                    'message': 'Not enough credits for bulk generation',
                    'details': {
                        'required': total_credits,
                        'available': user.credits_remaining
                    }
                }
            }), 400
        
        # Create video generation records for each variation
        generation_ids = []
        for variation in variations:
            video = GeneratedVideo(
                project_id=data['project_id'],
                user_id=user.id,
                actor_id=variation.get('actor_id'),
                voice_id=variation.get('voice_id'),
                model_used=variation.get('model', 'kling-1.6'),
                generation_status='queued',
                generation_started_at=datetime.utcnow(),
                credits_used=10
            )
            db.session.add(video)
            generation_ids.append(video.id)
        
        # Deduct credits from user
        user.credits_remaining -= total_credits
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'bulk_job_id': f'bulk_{generation_ids[0]}',
                'generation_ids': generation_ids,
                'total_videos': len(variations),
                'credits_required': total_credits,
                'estimated_completion_time': '2025-08-13T10:35:00Z'
            }
        }), 202
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'BULK_GENERATION_ERROR',
                'message': str(e)
            }
        }), 500

@videos_bp.route('/user', methods=['GET'])
def get_user_videos():
    """Get user's generated videos"""
    try:
        user = get_current_user_from_token()
        if not user:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'UNAUTHORIZED',
                    'message': 'Invalid or missing authorization token'
                }
            }), 401
        
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        
        # Build query
        query = GeneratedVideo.query.filter_by(user_id=user.id)
        
        if status:
            query = query.filter_by(generation_status=status)
        
        # Order by creation date (newest first)
        query = query.order_by(GeneratedVideo.created_at.desc())
        
        # Paginate
        videos = query.paginate(
            page=page,
            per_page=limit,
            error_out=False
        )
        
        return jsonify({
            'success': True,
            'data': {
                'videos': [video.to_dict() for video in videos.items],
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': videos.total,
                    'total_pages': videos.pages
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'VIDEOS_FETCH_ERROR',
                'message': str(e)
            }
        }), 500

