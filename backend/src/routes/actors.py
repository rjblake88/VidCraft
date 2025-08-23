from flask import Blueprint, request, jsonify
from src.models.actor import AIActor, db
from src.routes.auth import verify_token

actors_bp = Blueprint('actors', __name__)

@actors_bp.route('/', methods=['GET'])
def get_actors():
    """Get available AI actors with filtering"""
    try:
        # Mock actors data for demo - in production this would come from database
        mock_actors = [
            {
                'id': 'actor_1',
                'name': 'Sarah Chen',
                'style': 'Professional',
                'gender': 'Female',
                'age_range': '25-35',
                'ethnicity': 'Asian',
                'description': 'Professional business presenter with warm demeanor',
                'thumbnail_url': 'https://demo-actors.pollo.ai/sarah_chen.jpg',
                'preview_video_url': 'https://demo-actors.pollo.ai/sarah_chen_sample.mp4',
                'quality_rating': 4.8,
                'usage_count': 1250
            },
            {
                'id': 'actor_2',
                'name': 'Marcus Johnson',
                'style': 'Casual',
                'gender': 'Male',
                'age_range': '30-40',
                'ethnicity': 'African American',
                'description': 'Friendly and approachable casual presenter',
                'thumbnail_url': 'https://demo-actors.pollo.ai/marcus_johnson.jpg',
                'preview_video_url': 'https://demo-actors.pollo.ai/marcus_johnson_sample.mp4',
                'quality_rating': 4.6,
                'usage_count': 980
            },
            {
                'id': 'actor_3',
                'name': 'Elena Rodriguez',
                'style': 'Elegant',
                'gender': 'Female',
                'age_range': '35-45',
                'ethnicity': 'Hispanic',
                'description': 'Sophisticated and elegant presenter for luxury brands',
                'thumbnail_url': 'https://demo-actors.pollo.ai/elena_rodriguez.jpg',
                'preview_video_url': 'https://demo-actors.pollo.ai/elena_rodriguez_sample.mp4',
                'quality_rating': 4.9,
                'usage_count': 750
            },
            {
                'id': 'actor_4',
                'name': 'David Kim',
                'style': 'Tech Expert',
                'gender': 'Male',
                'age_range': '25-35',
                'ethnicity': 'Asian',
                'description': 'Technical expert presenter for tech and software products',
                'thumbnail_url': 'https://demo-actors.pollo.ai/david_kim.jpg',
                'preview_video_url': 'https://demo-actors.pollo.ai/david_kim_sample.mp4',
                'quality_rating': 4.7,
                'usage_count': 1100
            },
            {
                'id': 'actor_5',
                'name': 'Emma Thompson',
                'style': 'Friendly',
                'gender': 'Female',
                'age_range': '20-30',
                'ethnicity': 'Caucasian',
                'description': 'Young and energetic presenter for lifestyle brands',
                'thumbnail_url': 'https://demo-actors.pollo.ai/emma_thompson.jpg',
                'preview_video_url': 'https://demo-actors.pollo.ai/emma_thompson_sample.mp4',
                'quality_rating': 4.5,
                'usage_count': 650
            },
            {
                'id': 'actor_6',
                'name': 'James Wilson',
                'style': 'Corporate',
                'gender': 'Male',
                'age_range': '40-50',
                'ethnicity': 'Caucasian',
                'description': 'Executive-level presenter for corporate communications',
                'thumbnail_url': 'https://demo-actors.pollo.ai/james_wilson.jpg',
                'preview_video_url': 'https://demo-actors.pollo.ai/james_wilson_sample.mp4',
                'quality_rating': 4.8,
                'usage_count': 890
            }
        ]
        
        # Apply filters if provided
        gender_filter = request.args.get('gender')
        style_filter = request.args.get('style')
        age_filter = request.args.get('age_range')
        
        filtered_actors = mock_actors
        
        if gender_filter:
            filtered_actors = [a for a in filtered_actors if a['gender'].lower() == gender_filter.lower()]
        
        if style_filter:
            filtered_actors = [a for a in filtered_actors if style_filter.lower() in a['style'].lower()]
        
        if age_filter:
            filtered_actors = [a for a in filtered_actors if a['age_range'] == age_filter]
        
        # Get filter options
        filters = {
            'genders': list(set([a['gender'] for a in mock_actors])),
            'styles': list(set([a['style'] for a in mock_actors])),
            'age_ranges': list(set([a['age_range'] for a in mock_actors])),
            'ethnicities': list(set([a['ethnicity'] for a in mock_actors]))
        }
        
        return jsonify({
            'success': True,
            'data': {
                'actors': filtered_actors,
                'total_count': len(filtered_actors),
                'filters': filters,
                'pagination': {
                    'page': 1,
                    'limit': 50,
                    'total': len(filtered_actors),
                    'total_pages': 1
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'ACTORS_FETCH_ERROR',
                'message': str(e)
            }
        }), 500

@actors_bp.route('/<actor_id>', methods=['GET'])
def get_actor_details(actor_id):
    """Get detailed information about a specific actor"""
    try:
        actor = AIActor.query.get(actor_id)
        if not actor or not actor.is_active:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ACTOR_NOT_FOUND',
                    'message': 'Actor not found'
                }
            }), 404
        
        return jsonify({
            'success': True,
            'data': actor.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'ACTOR_FETCH_ERROR',
                'message': str(e)
            }
        }), 500

@actors_bp.route('/popular', methods=['GET'])
def get_popular_actors():
    """Get most popular actors based on usage"""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        actors = AIActor.query.filter_by(is_active=True)\
            .order_by(AIActor.usage_count.desc())\
            .limit(limit).all()
        
        return jsonify({
            'success': True,
            'data': {
                'actors': [actor.to_dict() for actor in actors]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'POPULAR_ACTORS_ERROR',
                'message': str(e)
            }
        }), 500

@actors_bp.route('/search', methods=['GET'])
def search_actors():
    """Search actors by name or description"""
    try:
        query_text = request.args.get('q', '')
        if not query_text:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'MISSING_QUERY',
                    'message': 'Search query is required'
                }
            }), 400
        
        # Search in name and description
        actors = AIActor.query.filter(
            AIActor.is_active == True,
            (AIActor.name.ilike(f'%{query_text}%') | 
             AIActor.description.ilike(f'%{query_text}%'))
        ).order_by(AIActor.quality_rating.desc()).all()
        
        return jsonify({
            'success': True,
            'data': {
                'actors': [actor.to_dict() for actor in actors],
                'query': query_text,
                'count': len(actors)
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': {
                'code': 'ACTOR_SEARCH_ERROR',
                'message': str(e)
            }
        }), 500

# Admin routes for managing actors (would require admin authentication in production)
@actors_bp.route('/admin/create', methods=['POST'])
def create_actor():
    """Create a new AI actor (admin only)"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['id', 'name', 'ai_service']
        for field in required_fields:
            if not data.get(field):
                return jsonify({
                    'success': False,
                    'error': {
                        'code': 'MISSING_FIELD',
                        'message': f'{field} is required'
                    }
                }), 400
        
        # Check if actor already exists
        existing_actor = AIActor.query.get(data['id'])
        if existing_actor:
            return jsonify({
                'success': False,
                'error': {
                    'code': 'ACTOR_EXISTS',
                    'message': 'Actor with this ID already exists'
                }
            }), 400
        
        # Create new actor
        actor = AIActor(
            id=data['id'],
            name=data['name'],
            description=data.get('description', ''),
            gender=data.get('gender'),
            age_range=data.get('age_range'),
            ethnicity=data.get('ethnicity'),
            style=data.get('style'),
            environment=data.get('environment'),
            thumbnail_url=data.get('thumbnail_url'),
            preview_video_url=data.get('preview_video_url'),
            ai_service=data['ai_service'],
            quality_rating=data.get('quality_rating', 0),
            supported_models=data.get('supported_models', [])
        )
        
        db.session.add(actor)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': actor.to_dict(),
            'message': 'Actor created successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': {
                'code': 'ACTOR_CREATION_ERROR',
                'message': str(e)
            }
        }), 500

