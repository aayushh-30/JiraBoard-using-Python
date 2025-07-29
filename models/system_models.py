from .models_models import db, UUID
from datetime import datetime
import uuid

class Backup(db.Model):
    """Backup model for SRS requirement: Backup and Restore"""
    __tablename__ = 'backup'
    
    backup_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=False)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    backup_type = db.Column(db.String(20), default='full')  # full, incremental
    file_path = db.Column(db.String(500))
    size_bytes = db.Column(db.BigInteger)
    status = db.Column(db.String(20), default='in_progress')  # in_progress, completed, failed
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    project = db.relationship('Project', backref='backups')
    created_by = db.relationship('User', backref='created_backups')

class SavedFilter(db.Model):
    """Saved search filters for SRS requirement: Advanced Search"""
    __tablename__ = 'saved_filter'
    
    filter_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    query = db.Column(db.Text, nullable=False)  # JQL-like query
    is_public = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='saved_filters')

class AutomationRule(db.Model):
    """Automation rules for SRS requirement: Automation"""
    __tablename__ = 'automation_rule'
    
    rule_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    trigger_event = db.Column(db.String(50), nullable=False)  # task_created, status_changed, etc.
    conditions = db.Column(db.JSON)  # Rule conditions
    actions = db.Column(db.JSON)  # Actions to perform
    is_active = db.Column(db.Boolean, default=True)
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='automation_rules')
    created_by = db.relationship('User', backref='automation_rules')

class NotificationPreference(db.Model):
    """Notification preferences for SRS requirement: Task Notifications Customization"""
    __tablename__ = 'notification_preference'
    
    preference_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    event_type = db.Column(db.String(50), nullable=False)  # task_assigned, task_updated, etc.
    email_enabled = db.Column(db.Boolean, default=True)
    in_app_enabled = db.Column(db.Boolean, default=True)
    frequency = db.Column(db.String(20), default='immediate')  # immediate, daily, weekly
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='notification_preferences')

class ActivityLog(db.Model):
    """Activity log for SRS requirement: Real-time collaboration tracking"""
    __tablename__ = 'activity_log'
    
    log_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    action = db.Column(db.String(100), nullable=False)
    entity_type = db.Column(db.String(50), nullable=False)  # task, project, comment, etc.
    entity_id = db.Column(UUID(as_uuid=True), nullable=False)
    details = db.Column(db.JSON)  # Additional action details
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='activity_logs')
