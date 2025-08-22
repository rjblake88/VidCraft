from datetime import datetime, timedelta
import uuid
from .user import db

class AnalyticsEvent(db.Model):
    """Track all user events for analytics"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)  # Can be null for anonymous events
    session_id = db.Column(db.String(36), nullable=True)
    event_type = db.Column(db.String(100), nullable=False)  # 'page_view', 'video_generated', 'template_used', etc.
    event_category = db.Column(db.String(50), nullable=False)  # 'user_action', 'system', 'payment', etc.
    
    # Event details
    event_data = db.Column(db.JSON, nullable=True)  # Flexible event data
    page_url = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
    
    # User context
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    device_type = db.Column(db.String(50))  # 'desktop', 'mobile', 'tablet'
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<AnalyticsEvent {self.event_type} by {self.user_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'event_type': self.event_type,
            'event_category': self.event_category,
            'event_data': self.event_data,
            'page_url': self.page_url,
            'referrer': self.referrer,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'device_type': self.device_type,
            'browser': self.browser,
            'os': self.os,
            'country': self.country,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class DailyMetrics(db.Model):
    """Daily aggregated metrics for performance tracking"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False, unique=True)
    
    # User metrics
    new_users = db.Column(db.Integer, default=0)
    active_users = db.Column(db.Integer, default=0)
    returning_users = db.Column(db.Integer, default=0)
    
    # Video generation metrics
    videos_generated = db.Column(db.Integer, default=0)
    total_credits_used = db.Column(db.Integer, default=0)
    avg_video_duration = db.Column(db.Float, default=0.0)
    
    # Template usage
    templates_used = db.Column(db.Integer, default=0)
    most_popular_template = db.Column(db.String(255))
    
    # Revenue metrics
    revenue = db.Column(db.Float, default=0.0)
    new_subscriptions = db.Column(db.Integer, default=0)
    cancelled_subscriptions = db.Column(db.Integer, default=0)
    credits_purchased = db.Column(db.Integer, default=0)
    
    # Engagement metrics
    avg_session_duration = db.Column(db.Float, default=0.0)  # in minutes
    bounce_rate = db.Column(db.Float, default=0.0)  # percentage
    page_views = db.Column(db.Integer, default=0)
    
    # AI model usage
    model_usage = db.Column(db.JSON, nullable=True)  # {'kling': 50, 'runway': 30, 'veo2': 20}
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<DailyMetrics {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'new_users': self.new_users,
            'active_users': self.active_users,
            'returning_users': self.returning_users,
            'videos_generated': self.videos_generated,
            'total_credits_used': self.total_credits_used,
            'avg_video_duration': self.avg_video_duration,
            'templates_used': self.templates_used,
            'most_popular_template': self.most_popular_template,
            'revenue': self.revenue,
            'new_subscriptions': self.new_subscriptions,
            'cancelled_subscriptions': self.cancelled_subscriptions,
            'credits_purchased': self.credits_purchased,
            'avg_session_duration': self.avg_session_duration,
            'bounce_rate': self.bounce_rate,
            'page_views': self.page_views,
            'model_usage': self.model_usage,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserSession(db.Model):
    """Track user sessions for analytics"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    session_id = db.Column(db.String(36), nullable=False, unique=True)
    
    # Session details
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime)
    duration_minutes = db.Column(db.Float, default=0.0)
    page_views = db.Column(db.Integer, default=0)
    
    # Entry and exit
    landing_page = db.Column(db.String(500))
    exit_page = db.Column(db.String(500))
    referrer = db.Column(db.String(500))
    
    # User context
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    device_type = db.Column(db.String(50))
    browser = db.Column(db.String(100))
    os = db.Column(db.String(100))
    country = db.Column(db.String(100))
    
    # Actions taken
    videos_generated = db.Column(db.Integer, default=0)
    templates_used = db.Column(db.Integer, default=0)
    credits_used = db.Column(db.Integer, default=0)
    
    # Conversion tracking
    converted = db.Column(db.Boolean, default=False)  # Did they complete a desired action
    conversion_type = db.Column(db.String(100))  # 'signup', 'subscription', 'video_generated'
    
    def __repr__(self):
        return f'<UserSession {self.session_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'session_id': self.session_id,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'duration_minutes': self.duration_minutes,
            'page_views': self.page_views,
            'landing_page': self.landing_page,
            'exit_page': self.exit_page,
            'referrer': self.referrer,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'device_type': self.device_type,
            'browser': self.browser,
            'os': self.os,
            'country': self.country,
            'videos_generated': self.videos_generated,
            'templates_used': self.templates_used,
            'credits_used': self.credits_used,
            'converted': self.converted,
            'conversion_type': self.conversion_type
        }

class RevenueMetrics(db.Model):
    """Track detailed revenue metrics"""
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    date = db.Column(db.Date, nullable=False)
    
    # Revenue breakdown
    subscription_revenue = db.Column(db.Float, default=0.0)
    credits_revenue = db.Column(db.Float, default=0.0)
    total_revenue = db.Column(db.Float, default=0.0)
    
    # Subscription metrics
    mrr = db.Column(db.Float, default=0.0)  # Monthly Recurring Revenue
    arr = db.Column(db.Float, default=0.0)  # Annual Recurring Revenue
    churn_rate = db.Column(db.Float, default=0.0)  # Monthly churn rate
    
    # Customer metrics
    total_customers = db.Column(db.Integer, default=0)
    paying_customers = db.Column(db.Integer, default=0)
    free_customers = db.Column(db.Integer, default=0)
    
    # Lifetime value
    avg_customer_ltv = db.Column(db.Float, default=0.0)
    avg_revenue_per_user = db.Column(db.Float, default=0.0)
    
    # Plan distribution
    free_plan_users = db.Column(db.Integer, default=0)
    pro_plan_users = db.Column(db.Integer, default=0)
    enterprise_plan_users = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<RevenueMetrics {self.date}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'date': self.date.isoformat() if self.date else None,
            'subscription_revenue': self.subscription_revenue,
            'credits_revenue': self.credits_revenue,
            'total_revenue': self.total_revenue,
            'mrr': self.mrr,
            'arr': self.arr,
            'churn_rate': self.churn_rate,
            'total_customers': self.total_customers,
            'paying_customers': self.paying_customers,
            'free_customers': self.free_customers,
            'avg_customer_ltv': self.avg_customer_ltv,
            'avg_revenue_per_user': self.avg_revenue_per_user,
            'free_plan_users': self.free_plan_users,
            'pro_plan_users': self.pro_plan_users,
            'enterprise_plan_users': self.enterprise_plan_users,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

