from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from src.models.user import db

class AIActor(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    gender = db.Column(db.String(20))
    age_range = db.Column(db.String(20))
    ethnicity = db.Column(db.String(50))
    style = db.Column(db.String(100))
    environment = db.Column(db.String(100))
    thumbnail_url = db.Column(db.String(500))
    preview_video_url = db.Column(db.String(500))
    ai_service = db.Column(db.String(100))
    quality_rating = db.Column(db.Numeric(3, 2))
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    supported_models = db.Column(db.JSON)  # List of models that support this actor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<AIActor {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'gender': self.gender,
            'age_range': self.age_range,
            'ethnicity': self.ethnicity,
            'style': self.style,
            'environment': self.environment,
            'thumbnail_url': self.thumbnail_url,
            'preview_video_url': self.preview_video_url,
            'ai_service': self.ai_service,
            'quality_rating': float(self.quality_rating) if self.quality_rating else None,
            'usage_count': self.usage_count,
            'is_active': self.is_active,
            'supported_models': self.supported_models,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

