from flask import Blueprint, request, jsonify
from datetime import datetime
from src.models.user import User, db
from src.models.project import Project
from src.routes.auth import verify_token

projects_bp = Blueprint('projects', __name__)

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

@projects_bp.route('/', methods=['POST'])
def create_project():
    """Create a new project"""
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
        if not data.get('name'):
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_FIELD',
                    'message': 'Project name is required'
                }
            }), 400
        
        # Create new project
        project = Project(
            user_id=user.id,
            name=data['name'],
            description=data.get('description', ''),
            script_content=data.get('script', ''),
            video_settings=data.get('settings', {})
        )
        
        db.session.add(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'project_id': project.id,
                'name': project.name,
                'status': project.status,
                'created_at': project.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'PROJECT_CREATION_ERROR',
                'message': str(e)
            }
        }), 500

@projects_bp.route('/', methods=['GET'])
def get_user_projects():
    """Get user's projects with pagination and filtering"""
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
        
        # Get query parameters
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 20, type=int)
        status = request.args.get('status')
        
        # Build query
        query = Project.query.filter_by(user_id=user.id)
        
        if status:
            query = query.filter_by(status=status)
        
        # Order by creation date (newest first)
        query = query.order_by(Project.created_at.desc())
        
        # Paginate
        projects = query.paginate(
            page=page, 
            per_page=limit, 
            error_out=False
        )
        
        # Count videos for each project
        project_list = []
        for project in projects.items:
            project_dict = project.to_dict()
            # Count generated videos for this project
            video_count = len(project.videos) if hasattr(project, 'videos') else 0
            project_dict['videos_generated'] = video_count
            project_list.append(project_dict)
        
        return jsonify({
            'success': True,
            'data': {
                'projects': project_list,
                'pagination': {
                    'page': page,
                    'limit': limit,
                    'total': projects.total,
                    'total_pages': projects.pages
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'PROJECTS_FETCH_ERROR',
                'message': str(e)
            }
        }), 500

@projects_bp.route('/<project_id>', methods=['GET'])
def get_project(project_id):
    """Get specific project details"""
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
        
        # Get project
        project = Project.query.filter_by(id=project_id, user_id=user.id).first()
        if not project:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'PROJECT_NOT_FOUND',
                    'message': 'Project not found'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': {
                'project': project.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'PROJECT_FETCH_ERROR',
                'message': str(e)
            }
        }), 500

@projects_bp.route('/<project_id>', methods=['PUT'])
def update_project(project_id):
    """Update project details"""
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
        
        # Get project
        project = Project.query.filter_by(id=project_id, user_id=user.id).first()
        if not project:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'PROJECT_NOT_FOUND',
                    'message': 'Project not found'
                }
            }), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            project.name = data['name']
        if 'description' in data:
            project.description = data['description']
        if 'script_content' in data:
            project.script_content = data['script_content']
        if 'selected_actors' in data:
            project.selected_actors = data['selected_actors']
        if 'voice_settings' in data:
            project.voice_settings = data['voice_settings']
        if 'video_settings' in data:
            project.video_settings = data['video_settings']
        if 'status' in data:
            project.status = data['status']
        
        project.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'project': project.to_dict()
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'PROJECT_UPDATE_ERROR',
                'message': str(e)
            }
        }), 500

@projects_bp.route('/<project_id>', methods=['DELETE'])
def delete_project(project_id):
    """Delete a project"""
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
        
        # Get project
        project = Project.query.filter_by(id=project_id, user_id=user.id).first()
        if not project:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'PROJECT_NOT_FOUND',
                    'message': 'Project not found'
                }
            }), 404
        
        db.session.delete(project)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Project deleted successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'PROJECT_DELETE_ERROR',
                'message': str(e)
            }
        }), 500

