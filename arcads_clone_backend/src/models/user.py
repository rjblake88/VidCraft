from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=True)  # Nullable for OAuth users
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    company = db.Column(db.String(255))
    avatar_url = db.Column(db.String(500))
    
    # Authentication fields
    google_id = db.Column(db.String(100), unique=True, nullable=True)
    auth_provider = db.Column(db.String(50), default='email')  # 'email', 'google'
    email_verified = db.Column(db.Boolean, default=False)
    two_factor_enabled = db.Column(db.Boolean, default=False)
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expires = db.Column(db.DateTime, nullable=True)
    
    # Subscription and billing
    role = db.Column(db.String(50), default='user')
    subscription_tier = db.Column(db.String(50), default='free')
    subscription_status = db.Column(db.String(50), default='active')
    stripe_customer_id = db.Column(db.String(100), nullable=True)
    stripe_subscription_id = db.Column(db.String(100), nullable=True)
    credits_remaining = db.Column(db.Integer, default=10)  # Free tier gets 10 credits
    credits_purchased = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0.0)
    
    # Usage tracking
    videos_generated = db.Column(db.Integer, default=0)
    minutes_generated = db.Column(db.Float, default=0.0)
    api_calls_made = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    subscription_expires = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def set_password(self, password):
        """Set password hash"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check password against hash"""
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

    def get_full_name(self):
        """Get user's full name"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.email.split('@')[0]

    def can_generate_video(self, credits_required=1):
        """Check if user has enough credits to generate video"""
        return self.credits_remaining >= credits_required

    def deduct_credits(self, amount):
        """Deduct credits from user account"""
        if self.credits_remaining >= amount:
            self.credits_remaining -= amount
            return True
        return False

    def add_credits(self, amount):
        """Add credits to user account"""
        self.credits_remaining += amount
        self.credits_purchased += amount

    def is_premium(self):
        """Check if user has premium subscription"""
        return self.subscription_tier in ['pro', 'enterprise']
    
    def is_admin(self):
        """Check if user has admin role"""
        return self.role == 'admin'
    
    def can_access_analytics(self):
        """Check if user can access platform analytics"""
        return self.is_admin()

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'company': self.company,
            'avatar_url': self.avatar_url,
            'role': self.role,
            'subscription_tier': self.subscription_tier,
            'subscription_status': self.subscription_status,
            'credits_remaining': self.credits_remaining,
            'credits_purchased': self.credits_purchased,
            'total_spent': self.total_spent,
            'videos_generated': self.videos_generated,
            'minutes_generated': self.minutes_generated,
            'auth_provider': self.auth_provider,
            'email_verified': self.email_verified,
            'two_factor_enabled': self.two_factor_enabled,
            'is_premium': self.is_premium(),
            'is_admin': self.is_admin(),
            'can_access_analytics': self.can_access_analytics(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'subscription_expires': self.subscription_expires.isoformat() if self.subscription_expires else None
        }
