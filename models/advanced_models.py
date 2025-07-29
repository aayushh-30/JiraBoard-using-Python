from .models_models import db, UUID
from datetime import datetime
import uuid

class Integration(db.Model):
    """External tool integration model (SRS requirement)"""
    __tablename__ = 'integration'
    
    integration_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # slack, github, google_drive, etc.
    config = db.Column(db.JSON)  # Integration-specific configuration
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_by = db.relationship('User', backref='integrations')
    project = db.relationship('Project', backref='integrations')

class Dashboard(db.Model):
    """Customizable dashboard model (SRS requirement)"""
    __tablename__ = 'dashboard'
    
    dashboard_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    widgets = db.Column(db.JSON)  # Store widget configuration
    layout = db.Column(db.JSON)  # Store layout preferences
    is_default = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='dashboards')

class GuestToken(db.Model):
    """Guest access tokens model (SRS requirement)"""
    __tablename__ = 'guest_token'
    
    token_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    token = db.Column(db.String(255), nullable=False, unique=True)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=False)
    usage_limit = db.Column(db.Integer, default=1)
    usage_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    permissions = db.Column(db.JSON)  # Define what the token can access
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    created_by = db.relationship('User', backref='guest_tokens')
