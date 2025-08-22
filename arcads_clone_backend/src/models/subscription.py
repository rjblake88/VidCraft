from datetime import datetime
import uuid
from .user import db

class SubscriptionPlan(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(100), nullable=False)
    tier = db.Column(db.String(50), nullable=False)  # 'free', 'pro', 'enterprise'
    stripe_price_id = db.Column(db.String(100), nullable=True)
    price_monthly = db.Column(db.Float, nullable=False)
    price_yearly = db.Column(db.Float, nullable=True)
    credits_included = db.Column(db.Integer, default=0)
    features = db.Column(db.JSON, nullable=True)
    max_videos_per_month = db.Column(db.Integer, nullable=True)
    max_duration_seconds = db.Column(db.Integer, default=10)
    priority_support = db.Column(db.Boolean, default=False)
    api_access = db.Column(db.Boolean, default=False)
    custom_branding = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<SubscriptionPlan {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'tier': self.tier,
            'stripe_price_id': self.stripe_price_id,
            'price_monthly': self.price_monthly,
            'price_yearly': self.price_yearly,
            'credits_included': self.credits_included,
            'features': self.features,
            'max_videos_per_month': self.max_videos_per_month,
            'max_duration_seconds': self.max_duration_seconds,
            'priority_support': self.priority_support,
            'api_access': self.api_access,
            'custom_branding': self.custom_branding,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Payment(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    stripe_payment_intent_id = db.Column(db.String(100), nullable=True)
    stripe_invoice_id = db.Column(db.String(100), nullable=True)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    status = db.Column(db.String(50), nullable=False)  # 'pending', 'succeeded', 'failed', 'refunded'
    payment_type = db.Column(db.String(50), nullable=False)  # 'subscription', 'credits', 'one_time'
    credits_purchased = db.Column(db.Integer, default=0)
    description = db.Column(db.String(255))
    payment_metadata = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<Payment {self.id} - {self.amount} {self.currency}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'stripe_payment_intent_id': self.stripe_payment_intent_id,
            'stripe_invoice_id': self.stripe_invoice_id,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'payment_type': self.payment_type,
            'credits_purchased': self.credits_purchased,
            'description': self.description,
            'payment_metadata': self.payment_metadata,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UsageLog(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)  # 'video_generated', 'credits_purchased', 'login'
    credits_used = db.Column(db.Integer, default=0)
    log_metadata = db.Column(db.JSON, nullable=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<UsageLog {self.action} by {self.user_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'action': self.action,
            'credits_used': self.credits_used,
            'log_metadata': self.log_metadata,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

