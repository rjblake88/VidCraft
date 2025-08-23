from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta, date
from sqlalchemy import func, and_, or_
import json

from ..models.user import User, db
from ..models.analytics import AnalyticsEvent, DailyMetrics, UserSession, RevenueMetrics
from ..models.subscription import Payment, SubscriptionPlan
from ..models.video import GeneratedVideo
from ..models.content import Template
from ..routes.auth_enhanced import verify_jwt_token, log_user_action

analytics_bp = Blueprint('analytics', __name__)

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

def require_admin():
    """Check if user has admin privileges"""
    user = get_authenticated_user()
    if not user or user.role != 'admin':
        return False
    return True

@analytics_bp.route('/track', methods=['POST'])
def track_event():
    """Track analytics event"""
    try:
        data = request.get_json()
        
        # Extract event data
        event_type = data.get('event_type')
        event_category = data.get('event_category', 'user_action')
        event_data = data.get('event_data', {})
        
        if not event_type:
            return jsonify({
                'success': False,
                'message': 'event_type is required'
            }), 400
        
        # Get user if authenticated
        user = get_authenticated_user()
        user_id = user.id if user else None
        
        # Extract request context
        session_id = data.get('session_id')
        page_url = data.get('page_url')
        referrer = data.get('referrer')
        
        # Create analytics event
        event = AnalyticsEvent(
            user_id=user_id,
            session_id=session_id,
            event_type=event_type,
            event_category=event_category,
            event_data=event_data,
            page_url=page_url,
            referrer=referrer,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', ''),
            device_type=detect_device_type(request.headers.get('User-Agent', '')),
            browser=detect_browser(request.headers.get('User-Agent', '')),
            os=detect_os(request.headers.get('User-Agent', ''))
        )
        
        db.session.add(event)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Event tracked successfully'
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'Failed to track event: {str(e)}'
        }), 500

@analytics_bp.route('/dashboard', methods=['GET'])
def get_dashboard_data():
    """Get analytics dashboard data - ADMIN ONLY"""
    try:
        # Check admin access
        user = get_authenticated_user()
        if not user or not user.is_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required. Only administrators can view platform analytics.'
            }), 403
        
        # Get date range
        days = int(request.args.get('days', 30))
        end_date = date.today()
        start_date = end_date - timedelta(days=days)
        
        # Get daily metrics
        daily_metrics = DailyMetrics.query.filter(
            and_(DailyMetrics.date >= start_date, DailyMetrics.date <= end_date)
        ).order_by(DailyMetrics.date.asc()).all()
        
        # If no metrics exist, generate sample data
        if not daily_metrics:
            daily_metrics = generate_sample_daily_metrics(start_date, end_date)
        
        # Calculate totals and trends
        total_users = User.query.count()
        total_videos = GeneratedVideo.query.count()
        total_revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.status == 'succeeded'
        ).scalar() or 0
        
        # Recent activity
        recent_events = AnalyticsEvent.query.filter(
            AnalyticsEvent.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).order_by(AnalyticsEvent.created_at.desc()).limit(50).all()
        
        # Top templates
        top_templates = db.session.query(
            Template.name,
            Template.usage_count
        ).filter(Template.is_active == True).order_by(
            Template.usage_count.desc()
        ).limit(10).all()
        
        # User growth
        user_growth = []
        for metric in daily_metrics:
            user_growth.append({
                'date': metric.date.isoformat(),
                'new_users': metric.new_users,
                'active_users': metric.active_users,
                'total_users': metric.new_users  # Simplified for demo
            })
        
        # Revenue trend
        revenue_trend = []
        for metric in daily_metrics:
            revenue_trend.append({
                'date': metric.date.isoformat(),
                'revenue': metric.revenue,
                'subscriptions': metric.new_subscriptions,
                'credits': metric.credits_purchased
            })
        
        # Video generation trend
        video_trend = []
        for metric in daily_metrics:
            video_trend.append({
                'date': metric.date.isoformat(),
                'videos': metric.videos_generated,
                'credits_used': metric.total_credits_used,
                'avg_duration': metric.avg_video_duration
            })
        
        return jsonify({
            'success': True,
            'data': {
                'overview': {
                    'total_users': total_users,
                    'total_videos': total_videos,
                    'total_revenue': total_revenue,
                    'active_sessions': len(recent_events)
                },
                'user_growth': user_growth,
                'revenue_trend': revenue_trend,
                'video_trend': video_trend,
                'top_templates': [{'name': name, 'usage': count} for name, count in top_templates],
                'recent_activity': [event.to_dict() for event in recent_events[:10]]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get dashboard data: {str(e)}'
        }), 500

@analytics_bp.route('/users', methods=['GET'])
def get_user_analytics():
    """Get detailed user analytics - ADMIN ONLY"""
    try:
        # Check admin access
        user = get_authenticated_user()
        if not user or not user.is_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required. Only administrators can view user analytics.'
            }), 403
        
        # User distribution by plan
        user_plans = db.session.query(
            User.subscription_tier,
            func.count(User.id).label('count')
        ).group_by(User.subscription_tier).all()
        
        # User registration trend (last 30 days)
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        registration_trend = db.session.query(
            func.date(User.created_at).label('date'),
            func.count(User.id).label('registrations')
        ).filter(
            User.created_at >= thirty_days_ago
        ).group_by(func.date(User.created_at)).all()
        
        # Active users by day
        active_users = db.session.query(
            func.date(AnalyticsEvent.created_at).label('date'),
            func.count(func.distinct(AnalyticsEvent.user_id)).label('active_users')
        ).filter(
            and_(
                AnalyticsEvent.created_at >= thirty_days_ago,
                AnalyticsEvent.user_id.isnot(None)
            )
        ).group_by(func.date(AnalyticsEvent.created_at)).all()
        
        return jsonify({
            'success': True,
            'data': {
                'plan_distribution': [{'plan': plan, 'count': count} for plan, count in user_plans],
                'registration_trend': [{'date': str(date), 'registrations': count} for date, count in registration_trend],
                'active_users': [{'date': str(date), 'active_users': count} for date, count in active_users]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get user analytics: {str(e)}'
        }), 500

@analytics_bp.route('/revenue', methods=['GET'])
def get_revenue_analytics():
    """Get detailed revenue analytics - ADMIN ONLY"""
    try:
        # Check admin access
        user = get_authenticated_user()
        if not user or not user.is_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required. Only administrators can view revenue analytics.'
            }), 403
        
        # Revenue by payment type
        revenue_by_type = db.session.query(
            Payment.payment_type,
            func.sum(Payment.amount).label('total_revenue'),
            func.count(Payment.id).label('transaction_count')
        ).filter(
            Payment.status == 'succeeded'
        ).group_by(Payment.payment_type).all()
        
        # Monthly recurring revenue
        current_month = date.today().replace(day=1)
        mrr = db.session.query(
            func.sum(SubscriptionPlan.price_monthly)
        ).join(User, User.subscription_tier == SubscriptionPlan.tier).filter(
            and_(
                User.subscription_status == 'active',
                SubscriptionPlan.tier != 'free'
            )
        ).scalar() or 0
        
        # Revenue trend (last 12 months)
        twelve_months_ago = datetime.utcnow() - timedelta(days=365)
        revenue_trend = db.session.query(
            func.date_trunc('month', Payment.created_at).label('month'),
            func.sum(Payment.amount).label('revenue')
        ).filter(
            and_(
                Payment.created_at >= twelve_months_ago,
                Payment.status == 'succeeded'
            )
        ).group_by(func.date_trunc('month', Payment.created_at)).all()
        
        return jsonify({
            'success': True,
            'data': {
                'mrr': mrr,
                'revenue_by_type': [
                    {'type': payment_type, 'revenue': float(revenue), 'transactions': count}
                    for payment_type, revenue, count in revenue_by_type
                ],
                'revenue_trend': [
                    {'month': str(month), 'revenue': float(revenue)}
                    for month, revenue in revenue_trend
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get revenue analytics: {str(e)}'
        }), 500

@analytics_bp.route('/content', methods=['GET'])
def get_content_analytics():
    """Get content usage analytics - ADMIN ONLY"""
    try:
        # Check admin access
        user = get_authenticated_user()
        if not user or not user.is_admin():
            return jsonify({
                'success': False,
                'message': 'Admin access required. Only administrators can view content analytics.'
            }), 403
        
        # Template usage statistics
        template_stats = db.session.query(
            Template.name,
            Template.category,
            Template.usage_count,
            Template.estimated_credits
        ).filter(Template.is_active == True).order_by(
            Template.usage_count.desc()
        ).limit(20).all()
        
        # Category popularity
        category_stats = db.session.query(
            Template.category,
            func.sum(Template.usage_count).label('total_usage'),
            func.count(Template.id).label('template_count')
        ).filter(Template.is_active == True).group_by(
            Template.category
        ).order_by(func.sum(Template.usage_count).desc()).all()
        
        # Video generation by model
        model_usage = db.session.query(
            GeneratedVideo.ai_model,
            func.count(GeneratedVideo.id).label('usage_count'),
            func.avg(GeneratedVideo.duration_seconds).label('avg_duration')
        ).group_by(GeneratedVideo.ai_model).all()
        
        return jsonify({
            'success': True,
            'data': {
                'template_stats': [
                    {
                        'name': name,
                        'category': category,
                        'usage_count': usage_count,
                        'estimated_credits': estimated_credits
                    }
                    for name, category, usage_count, estimated_credits in template_stats
                ],
                'category_stats': [
                    {
                        'category': category,
                        'total_usage': total_usage,
                        'template_count': template_count
                    }
                    for category, total_usage, template_count in category_stats
                ],
                'model_usage': [
                    {
                        'model': model,
                        'usage_count': usage_count,
                        'avg_duration': float(avg_duration) if avg_duration else 0
                    }
                    for model, usage_count, avg_duration in model_usage
                ]
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Failed to get content analytics: {str(e)}'
        }), 500

def generate_sample_daily_metrics(start_date, end_date):
    """Generate sample daily metrics for demo purposes"""
    import random
    
    metrics = []
    current_date = start_date
    
    while current_date <= end_date:
        # Generate realistic sample data
        base_users = 50 + (current_date - start_date).days * 2
        
        metric = DailyMetrics(
            date=current_date,
            new_users=random.randint(5, 25),
            active_users=base_users + random.randint(-10, 20),
            returning_users=random.randint(20, 40),
            videos_generated=random.randint(100, 500),
            total_credits_used=random.randint(200, 1000),
            avg_video_duration=random.uniform(10, 30),
            templates_used=random.randint(50, 200),
            revenue=random.uniform(500, 2000),
            new_subscriptions=random.randint(2, 15),
            cancelled_subscriptions=random.randint(0, 5),
            credits_purchased=random.randint(100, 500),
            avg_session_duration=random.uniform(5, 25),
            bounce_rate=random.uniform(20, 60),
            page_views=random.randint(500, 2000),
            model_usage={
                'kling': random.randint(30, 50),
                'runway': random.randint(20, 40),
                'veo2': random.randint(15, 35),
                'luma': random.randint(10, 25)
            }
        )
        
        db.session.add(metric)
        metrics.append(metric)
        current_date += timedelta(days=1)
    
    try:
        db.session.commit()
    except:
        db.session.rollback()
    
    return metrics

def detect_device_type(user_agent):
    """Detect device type from user agent"""
    user_agent = user_agent.lower()
    if 'mobile' in user_agent or 'android' in user_agent or 'iphone' in user_agent:
        return 'mobile'
    elif 'tablet' in user_agent or 'ipad' in user_agent:
        return 'tablet'
    else:
        return 'desktop'

def detect_browser(user_agent):
    """Detect browser from user agent"""
    user_agent = user_agent.lower()
    if 'chrome' in user_agent:
        return 'Chrome'
    elif 'firefox' in user_agent:
        return 'Firefox'
    elif 'safari' in user_agent:
        return 'Safari'
    elif 'edge' in user_agent:
        return 'Edge'
    else:
        return 'Other'

def detect_os(user_agent):
    """Detect operating system from user agent"""
    user_agent = user_agent.lower()
    if 'windows' in user_agent:
        return 'Windows'
    elif 'mac' in user_agent:
        return 'macOS'
    elif 'linux' in user_agent:
        return 'Linux'
    elif 'android' in user_agent:
        return 'Android'
    elif 'ios' in user_agent:
        return 'iOS'
    else:
        return 'Other'

