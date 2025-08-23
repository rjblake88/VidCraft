from datetime import datetime
import uuid
from .user import db

class Template(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(100), nullable=False)  # 'marketing', 'education', 'entertainment', etc.
    subcategory = db.Column(db.String(100))
    script_template = db.Column(db.Text, nullable=False)
    thumbnail_url = db.Column(db.String(500))
    preview_video_url = db.Column(db.String(500))
    
    # Template settings
    recommended_duration = db.Column(db.Integer, default=10)  # seconds
    recommended_model = db.Column(db.String(100))
    recommended_actor = db.Column(db.String(100))
    recommended_voice = db.Column(db.String(100))
    
    # Metadata
    tags = db.Column(db.JSON, nullable=True)  # Array of tags
    difficulty_level = db.Column(db.String(50), default='beginner')  # 'beginner', 'intermediate', 'advanced'
    estimated_credits = db.Column(db.Integer, default=1)
    
    # Usage and popularity
    usage_count = db.Column(db.Integer, default=0)
    rating_average = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    
    # Access control
    is_premium = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Authorship
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    is_user_generated = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<Template {self.name}>'

    def increment_usage(self):
        """Increment usage count when template is used"""
        self.usage_count += 1

    def add_rating(self, rating):
        """Add a new rating and update average"""
        total_rating = self.rating_average * self.rating_count
        self.rating_count += 1
        self.rating_average = (total_rating + rating) / self.rating_count

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category': self.category,
            'subcategory': self.subcategory,
            'script_template': self.script_template,
            'thumbnail_url': self.thumbnail_url,
            'preview_video_url': self.preview_video_url,
            'recommended_duration': self.recommended_duration,
            'recommended_model': self.recommended_model,
            'recommended_actor': self.recommended_actor,
            'recommended_voice': self.recommended_voice,
            'tags': self.tags,
            'difficulty_level': self.difficulty_level,
            'estimated_credits': self.estimated_credits,
            'usage_count': self.usage_count,
            'rating_average': self.rating_average,
            'rating_count': self.rating_count,
            'is_premium': self.is_premium,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'is_user_generated': self.is_user_generated,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Asset(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    asset_type = db.Column(db.String(50), nullable=False)  # 'image', 'video', 'audio', 'music'
    category = db.Column(db.String(100), nullable=False)
    file_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    file_size = db.Column(db.Integer)  # in bytes
    duration = db.Column(db.Float, nullable=True)  # for video/audio assets
    dimensions = db.Column(db.String(50), nullable=True)  # e.g., "1920x1080"
    
    # Metadata
    tags = db.Column(db.JSON, nullable=True)
    license_type = db.Column(db.String(100), default='royalty_free')
    attribution_required = db.Column(db.Boolean, default=False)
    attribution_text = db.Column(db.String(500))
    
    # Usage and popularity
    download_count = db.Column(db.Integer, default=0)
    usage_count = db.Column(db.Integer, default=0)
    rating_average = db.Column(db.Float, default=0.0)
    rating_count = db.Column(db.Integer, default=0)
    
    # Access control
    is_premium = db.Column(db.Boolean, default=False)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    
    # Authorship
    created_by = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=True)
    source = db.Column(db.String(255))  # Source/provider of the asset
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<Asset {self.name} ({self.asset_type})>'

    def increment_usage(self):
        """Increment usage count when asset is used"""
        self.usage_count += 1

    def increment_downloads(self):
        """Increment download count when asset is downloaded"""
        self.download_count += 1

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'asset_type': self.asset_type,
            'category': self.category,
            'file_url': self.file_url,
            'thumbnail_url': self.thumbnail_url,
            'file_size': self.file_size,
            'duration': self.duration,
            'dimensions': self.dimensions,
            'tags': self.tags,
            'license_type': self.license_type,
            'attribution_required': self.attribution_required,
            'attribution_text': self.attribution_text,
            'download_count': self.download_count,
            'usage_count': self.usage_count,
            'rating_average': self.rating_average,
            'rating_count': self.rating_count,
            'is_premium': self.is_premium,
            'is_featured': self.is_featured,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'source': self.source,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserFavorite(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # 'template', 'asset'
    item_id = db.Column(db.String(36), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<UserFavorite {self.user_id} - {self.item_type}:{self.item_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Collection(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<Collection {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'name': self.name,
            'description': self.description,
            'is_public': self.is_public,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class CollectionItem(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    collection_id = db.Column(db.String(36), db.ForeignKey('collection.id'), nullable=False)
    item_type = db.Column(db.String(50), nullable=False)  # 'template', 'asset'
    item_id = db.Column(db.String(36), nullable=False)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships will be handled by foreign keys

    def __repr__(self):
        return f'<CollectionItem {self.collection_id} - {self.item_type}:{self.item_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'collection_id': self.collection_id,
            'item_type': self.item_type,
            'item_id': self.item_id,
            'added_at': self.added_at.isoformat() if self.added_at else None
        }

