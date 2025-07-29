from .models_models import db, UUID
from datetime import datetime
import uuid

class Epic(db.Model):
    """Epic model for grouping related issues (SRS requirement)"""
    __tablename__ = 'epic'
    
    epic_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=False)
    status = db.Column(db.String(50), default='open')
    start_date = db.Column(db.DateTime)
    target_date = db.Column(db.DateTime)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='epics')
    created_by = db.relationship('User', backref='created_epics')
    issues = db.relationship('Task', backref='epic', lazy='dynamic')
