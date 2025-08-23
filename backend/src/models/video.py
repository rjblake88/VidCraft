from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from src.models.user import db

class GeneratedVideo(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    actor_id = db.Column(db.String(100))
    voice_id = db.Column(db.String(100))
    model_used = db.Column(db.String(100))  # e.g., 'kling-1.6', 'runway-gen3'
    video_url = db.Column(db.String(500))
    thumbnail_url = db.Column(db.String(500))
    duration_seconds = db.Column(db.Integer)
    resolution = db.Column(db.String(20))
    file_size_bytes = db.Column(db.BigInteger)
    generation_status = db.Column(db.String(50), default='pending')
    generation_started_at = db.Column(db.DateTime)
    generation_completed_at = db.Column(db.DateTime)
    ai_service_used = db.Column(db.String(100))
    quality_score = db.Column(db.Numeric(3, 2))
    credits_used = db.Column(db.Integer, default=0)
    pollo_task_id = db.Column(db.String(255))  # Pollo AI task ID for tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    project = db.relationship('Project', backref=db.backref('videos', lazy=True))
    user = db.relationship('User', backref=db.backref('videos', lazy=True))

    def __repr__(self):
        return f'<GeneratedVideo {self.id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'project_id': self.project_id,
            'user_id': self.user_id,
            'actor_id': self.actor_id,
            'voice_id': self.voice_id,
            'model_used': self.model_used,
            'video_url': self.video_url,
            'thumbnail_url': self.thumbnail_url,
            'duration_seconds': self.duration_seconds,
            'resolution': self.resolution,
            'file_size_bytes': self.file_size_bytes,
            'generation_status': self.generation_status,
            'generation_started_at': self.generation_started_at.isoformat() if self.generation_started_at else None,
            'generation_completed_at': self.generation_completed_at.isoformat() if self.generation_completed_at else None,
            'ai_service_used': self.ai_service_used,
            'quality_score': float(self.quality_score) if self.quality_score else None,
            'credits_used': self.credits_used,
            'pollo_task_id': self.pollo_task_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

