from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid
from src.models.user import db

class VoiceClone(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    voice_id_external = db.Column(db.String(255))  # ElevenLabs voice ID
    ai_service = db.Column(db.String(100))
    sample_audio_url = db.Column(db.String(500))
    preview_audio_url = db.Column(db.String(500))
    language = db.Column(db.String(10))
    gender = db.Column(db.String(20))
    quality_score = db.Column(db.Numeric(3, 2))
    is_public = db.Column(db.Boolean, default=False)
    usage_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to user
    user = db.relationship('User', backref=db.backref('voice_clones', lazy=True))

    def __repr__(self):
        return f'<VoiceClone {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'voice_id_external': self.voice_id_external,
            'ai_service': self.ai_service,
            'sample_audio_url': self.sample_audio_url,
            'preview_audio_url': self.preview_audio_url,
            'language': self.language,
            'gender': self.gender,
            'quality_score': float(self.quality_score) if self.quality_score else None,
            'is_public': self.is_public,
            'usage_count': self.usage_count,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class VoiceLibrary(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    language = db.Column(db.String(10))
    accent = db.Column(db.String(50))
    gender = db.Column(db.String(20))
    style = db.Column(db.String(100))
    preview_audio_url = db.Column(db.String(500))
    ai_service = db.Column(db.String(100))
    quality_score = db.Column(db.Numeric(3, 2))
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<VoiceLibrary {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'language': self.language,
            'accent': self.accent,
            'gender': self.gender,
            'style': self.style,
            'preview_audio_url': self.preview_audio_url,
            'ai_service': self.ai_service,
            'quality_score': float(self.quality_score) if self.quality_score else None,
            'usage_count': self.usage_count,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

