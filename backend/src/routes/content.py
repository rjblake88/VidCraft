from flask import Blueprint, request, jsonify
import os
from datetime import datetime
import json

from ..models.user import User, db
from ..models.content import Template, Asset, UserFavorite, Collection, CollectionItem
from ..routes.auth_enhanced import verify_jwt_token, log_user_action

content_bp = Blueprint('content', __name__)

def get_authenticated_user():
    """Get authenticated user from JWT token"""
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return None
    
    token = auth_header.split(' ')[1]
    user_id = verify_jwt_token(token)
    
    if not user_id:
        return None
    
    return User.query.get(user_id)

@content_bp.route('/templates', methods=['GET'])
def get_templates():
    """Get available video templates"""
    try:
        # Get query parameters
        category = request.args.get('category')
        industry = request.args.get('industry')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Template.query.filter_by(is_active=True)
        
        if category:
            query = query.filter(Template.category == category)
        
        if industry:
            query = query.filter(Template.industry == industry)
        
        if search:
            query = query.filter(Template.name.contains(search) | Template.description.contains(search))
        
        # Order by popularity and creation date
        query = query.order_by(Template.usage_count.desc(), Template.created_at.desc())
        
        # Paginate
        templates = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # If no templates exist, create default templates
        if templates.total == 0:
            create_default_templates()
            # Re-run query
            templates = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'templates': [template.to_dict() for template in templates.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': templates.total,
                    'pages': templates.pages,
                    'has_next': templates.has_next,
                    'has_prev': templates.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get templates: {str(e)}'
        }), 500

def create_default_templates():
    """Create default video templates"""
    try:
        templates = [
            {
                'name': 'Product Launch Announcement',
                'description': 'Professional template for announcing new products with dynamic visuals and compelling copy',
                'category': 'marketing',
                'subcategory': 'product_launch',
                'script_template': 'Introducing {product_name} - the {product_category} that will {main_benefit}. Available now at {website}. Get yours today and {call_to_action}!',
                'recommended_duration': 15,
                'tags': ['product', 'launch', 'announcement', 'ecommerce'],
                'thumbnail_url': 'https://images.unsplash.com/photo-1556742049-0cfed4f6a45d?w=400&h=300',
                'preview_video_url': 'https://example.com/previews/product-launch.mp4',
                'difficulty_level': 'beginner',
                'estimated_credits': 2
            },
            {
                'name': 'Social Media Promo',
                'description': 'Eye-catching template perfect for social media promotions and special offers',
                'category': 'social',
                'subcategory': 'promotion',
                'script_template': '🔥 {offer_type} Alert! Get {discount_amount} off {product_service} this {time_period}. Use code {promo_code} at checkout. Limited time only!',
                'recommended_duration': 10,
                'tags': ['social', 'promo', 'discount', 'sale'],
                'thumbnail_url': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=400&h=300',
                'preview_video_url': 'https://example.com/previews/social-promo.mp4',
                'difficulty_level': 'beginner',
                'estimated_credits': 1
            },
            {
                'name': 'Educational Explainer',
                'description': 'Clear and engaging template for educational content and tutorials',
                'category': 'education',
                'subcategory': 'tutorial',
                'script_template': 'Did you know that {interesting_fact}? Today we\'ll learn about {topic} and discover {key_learning}. By the end of this video, you\'ll understand {outcome}.',
                'recommended_duration': 20,
                'tags': ['education', 'tutorial', 'explainer', 'learning'],
                'thumbnail_url': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=400&h=300',
                'preview_video_url': 'https://example.com/previews/educational.mp4',
                'difficulty_level': 'intermediate',
                'estimated_credits': 3
            },
            {
                'name': 'Customer Testimonial',
                'description': 'Authentic template for showcasing customer success stories and reviews',
                'category': 'testimonial',
                'subcategory': 'customer_story',
                'script_template': 'Meet {customer_name}, who {customer_background}. After using {product_service}, they achieved {result}. "{testimonial_quote}" - {customer_name}',
                'recommended_duration': 18,
                'tags': ['testimonial', 'customer', 'success', 'review'],
                'thumbnail_url': 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=400&h=300',
                'preview_video_url': 'https://example.com/previews/testimonial.mp4',
                'difficulty_level': 'beginner',
                'estimated_credits': 2
            },
            {
                'name': 'Event Invitation',
                'description': 'Professional template for promoting events, webinars, and conferences',
                'category': 'event',
                'subcategory': 'invitation',
                'script_template': 'You\'re invited to {event_name} on {event_date}! Join us for {event_description}. Register now at {registration_url} and {incentive}.',
                'recommended_duration': 12,
                'tags': ['event', 'invitation', 'webinar', 'conference'],
                'thumbnail_url': 'https://images.unsplash.com/photo-1540575467063-178a50c2df87?w=400&h=300',
                'preview_video_url': 'https://example.com/previews/event.mp4',
                'difficulty_level': 'beginner',
                'estimated_credits': 1
            },
            {
                'name': 'App Feature Showcase',
                'description': 'Dynamic template for highlighting app features and functionality',
                'category': 'technology',
                'subcategory': 'app_demo',
                'script_template': 'Discover {app_name}\'s powerful {feature_name} feature. {feature_description}. Download {app_name} today and {benefit}.',
                'recommended_duration': 14,
                'tags': ['app', 'feature', 'technology', 'mobile'],
                'thumbnail_url': 'https://images.unsplash.com/photo-1512941937669-90a1b58e7e9c?w=400&h=300',
                'preview_video_url': 'https://example.com/previews/app-feature.mp4',
                'difficulty_level': 'intermediate',
                'estimated_credits': 2
            }
        ]
        
        for template_data in templates:
            template = Template(
                name=template_data['name'],
                description=template_data['description'],
                category=template_data['category'],
                subcategory=template_data['subcategory'],
                script_template=template_data['script_template'],
                recommended_duration=template_data['recommended_duration'],
                tags=template_data['tags'],
                thumbnail_url=template_data['thumbnail_url'],
                preview_video_url=template_data['preview_video_url'],
                difficulty_level=template_data['difficulty_level'],
                estimated_credits=template_data['estimated_credits'],
                is_active=True,
                is_premium=False,
                usage_count=0,
                creator_id=None  # System templates
            )
            
            db.session.add(template)
        
        db.session.commit()
        print("Created default templates successfully")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default templates: {e}")

@content_bp.route('/templates/<template_id>', methods=['GET'])
def get_template(template_id):
    """Get specific template details"""
    try:
        template = Template.query.get(template_id)
        
        if not template or not template.is_active:
            return jsonify({
                'success': False,
                'message': 'Template not found'
            }), 404
        
        # Increment usage count
        template.usage_count += 1
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': {
                'template': template.to_dict()
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get template: {str(e)}'
        }), 500

@content_bp.route('/assets', methods=['GET'])
def get_assets():
    """Get available assets (images, videos, audio)"""
    try:
        # Get query parameters
        asset_type = request.args.get('type')  # 'image', 'video', 'audio'
        category = request.args.get('category')
        search = request.args.get('search')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        
        # Build query
        query = Asset.query.filter_by(is_active=True)
        
        if asset_type:
            query = query.filter(Asset.asset_type == asset_type)
        
        if category:
            query = query.filter(Asset.category == category)
        
        if search:
            query = query.filter(Asset.name.contains(search) | Asset.description.contains(search))
        
        # Order by popularity and creation date
        query = query.order_by(Asset.download_count.desc(), Asset.created_at.desc())
        
        # Paginate
        assets = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # If no assets exist, create default assets
        if assets.total == 0:
            create_default_assets()
            # Re-run query
            assets = query.paginate(page=page, per_page=per_page, error_out=False)
        
        return jsonify({
            'success': True,
            'data': {
                'assets': [asset.to_dict() for asset in assets.items],
                'pagination': {
                    'page': page,
                    'per_page': per_page,
                    'total': assets.total,
                    'pages': assets.pages,
                    'has_next': assets.has_next,
                    'has_prev': assets.has_prev
                }
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get assets: {str(e)}'
        }), 500

def create_default_assets():
    """Create default assets library"""
    try:
        assets = [
            # Background Images
            {
                'name': 'Modern Office Background',
                'description': 'Clean, professional office environment perfect for business videos',
                'asset_type': 'image',
                'category': 'backgrounds',
                'file_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=1920&h=1080',
                'thumbnail_url': 'https://images.unsplash.com/photo-1497366216548-37526070297c?w=400&h=300',
                'tags': ['office', 'business', 'professional', 'modern'],
                'license': 'free',
                'file_size': 2048000,
                'dimensions': '1920x1080'
            },
            {
                'name': 'Abstract Gradient Background',
                'description': 'Colorful gradient background ideal for tech and creative content',
                'asset_type': 'image',
                'category': 'backgrounds',
                'file_url': 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=1920&h=1080',
                'thumbnail_url': 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?w=400&h=300',
                'tags': ['gradient', 'abstract', 'colorful', 'tech'],
                'license': 'free',
                'file_size': 1536000,
                'dimensions': '1920x1080'
            },
            {
                'name': 'Nature Landscape',
                'description': 'Serene mountain landscape for wellness and lifestyle content',
                'asset_type': 'image',
                'category': 'backgrounds',
                'file_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1920&h=1080',
                'thumbnail_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=400&h=300',
                'tags': ['nature', 'landscape', 'mountains', 'wellness'],
                'license': 'free',
                'file_size': 2560000,
                'dimensions': '1920x1080'
            },
            # Product Images
            {
                'name': 'Smartphone Mockup',
                'description': 'Modern smartphone mockup for app and mobile product demos',
                'asset_type': 'image',
                'category': 'products',
                'file_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=800&h=1200',
                'thumbnail_url': 'https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300',
                'tags': ['smartphone', 'mobile', 'mockup', 'technology'],
                'license': 'free',
                'file_size': 1024000,
                'dimensions': '800x1200'
            },
            {
                'name': 'Laptop Workspace',
                'description': 'Clean laptop setup perfect for software and service demos',
                'asset_type': 'image',
                'category': 'products',
                'file_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=1920&h=1080',
                'thumbnail_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300',
                'tags': ['laptop', 'workspace', 'technology', 'productivity'],
                'license': 'free',
                'file_size': 1792000,
                'dimensions': '1920x1080'
            },
            # Audio Assets
            {
                'name': 'Upbeat Corporate',
                'description': 'Energetic background music perfect for business and marketing videos',
                'asset_type': 'audio',
                'category': 'music',
                'file_url': 'https://example.com/audio/upbeat-corporate.mp3',
                'thumbnail_url': 'https://example.com/thumbnails/audio-wave.jpg',
                'tags': ['corporate', 'upbeat', 'business', 'energetic'],
                'license': 'royalty_free',
                'file_size': 5120000,
                'duration': 120
            },
            {
                'name': 'Calm Ambient',
                'description': 'Peaceful ambient music for wellness and educational content',
                'asset_type': 'audio',
                'category': 'music',
                'file_url': 'https://example.com/audio/calm-ambient.mp3',
                'thumbnail_url': 'https://example.com/thumbnails/audio-wave.jpg',
                'tags': ['ambient', 'calm', 'peaceful', 'wellness'],
                'license': 'royalty_free',
                'file_size': 4608000,
                'duration': 90
            },
            # Video Assets
            {
                'name': 'City Timelapse',
                'description': 'Dynamic city timelapse perfect for urban and business content',
                'asset_type': 'video',
                'category': 'backgrounds',
                'file_url': 'https://example.com/videos/city-timelapse.mp4',
                'thumbnail_url': 'https://example.com/thumbnails/city-timelapse.jpg',
                'tags': ['city', 'timelapse', 'urban', 'dynamic'],
                'license': 'royalty_free',
                'file_size': 52428800,
                'duration': 15,
                'dimensions': '1920x1080'
            }
        ]
        
        for asset_data in assets:
            asset = Asset(
                name=asset_data['name'],
                description=asset_data['description'],
                asset_type=asset_data['asset_type'],
                category=asset_data['category'],
                file_url=asset_data['file_url'],
                thumbnail_url=asset_data['thumbnail_url'],
                tags=asset_data['tags'],
                license=asset_data['license'],
                file_size=asset_data['file_size'],
                dimensions=asset_data.get('dimensions'),
                duration=asset_data.get('duration'),
                is_active=True,
                is_premium=False,
                download_count=0,
                creator_id=None  # System assets
            )
            
            db.session.add(asset)
        
        db.session.commit()
        print("Created default assets successfully")
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating default assets: {e}")

@content_bp.route('/favorites', methods=['GET'])
def get_user_favorites():
    """Get user's favorite templates and assets"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        favorites = UserFavorite.query.filter_by(user_id=user.id).all()
        
        # Group by type
        templates = []
        assets = []
        
        for favorite in favorites:
            if favorite.item_type == 'template':
                template = Template.query.get(favorite.item_id)
                if template and template.is_active:
                    templates.append(template.to_dict())
            elif favorite.item_type == 'asset':
                asset = Asset.query.get(favorite.item_id)
                if asset and asset.is_active:
                    assets.append(asset.to_dict())
        
        return jsonify({
            'success': True,
            'data': {
                'templates': templates,
                'assets': assets
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get favorites: {str(e)}'
        }), 500

@content_bp.route('/favorites', methods=['POST'])
def add_to_favorites():
    """Add template or asset to user's favorites"""
    try:
        user = get_authenticated_user()
        if not user:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        data = request.get_json()
        item_type = data.get('item_type')  # 'template' or 'asset'
        item_id = data.get('item_id')
        
        if not item_type or not item_id:
            return jsonify({
                'success': False,
                'message': 'item_type and item_id are required'
            }), 400
        
        # Check if already favorited
        existing = UserFavorite.query.filter_by(
            user_id=user.id,
            item_type=item_type,
            item_id=item_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'message': 'Item already in favorites'
            }), 400
        
        # Add to favorites
        favorite = UserFavorite(
            user_id=user.id,
            item_type=item_type,
            item_id=item_id
        )
        
        db.session.add(favorite)
        db.session.commit()
        
        # Log action
        log_user_action(user.id, 'item_favorited', {
            'item_type': item_type,
            'item_id': item_id
        })
        
        return jsonify({
            'success': True,
            'message': 'Added to favorites'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to add to favorites: {str(e)}'
        }), 500

@content_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get available categories for templates and assets"""
    try:
        # Template categories
        template_categories = db.session.query(Template.category).filter_by(is_active=True).distinct().all()
        template_categories = [cat[0] for cat in template_categories if cat[0]]
        
        # Template subcategories
        template_subcategories = db.session.query(Template.subcategory).filter_by(is_active=True).distinct().all()
        template_subcategories = [sub[0] for sub in template_subcategories if sub[0]]
        
        # Asset categories
        asset_categories = db.session.query(Asset.category).filter_by(is_active=True).distinct().all()
        asset_categories = [cat[0] for cat in asset_categories if cat[0]]
        
        return jsonify({
            'success': True,
            'data': {
                'template_categories': template_categories,
                'template_subcategories': template_subcategories,
                'asset_categories': asset_categories
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get categories: {str(e)}'
        }), 500

