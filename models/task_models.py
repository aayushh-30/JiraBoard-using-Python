from .models_models import db, UUID, TaskStatus, TaskType
from datetime import datetime
import uuid

class Task(db.Model):
    __tablename__ = 'task'
    task_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TaskStatus), nullable=False, default='todo')
    type = db.Column(db.Enum(TaskType), nullable=False)
    priority = db.Column(db.String(10), default='medium')  # low, medium, high
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=False)
    subproject_id = db.Column(UUID(as_uuid=True), db.ForeignKey('subproject.subproject_id'))
    sprint_id = db.Column(UUID(as_uuid=True), db.ForeignKey('sprint.sprint_id'))
    epic_id = db.Column(UUID(as_uuid=True), db.ForeignKey('epic.epic_id'))  # SRS: Epic grouping
    assigned_to_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'))
    parent_task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'))
    estimated_hours = db.Column(db.Float)  # Time tracking
    logged_hours = db.Column(db.Float, default=0.0)  # SRS: Time tracking
    due_date = db.Column(db.DateTime)
    labels = db.Column(db.JSON)  # SRS: Labels/Tags support
    custom_fields = db.Column(db.JSON)  # SRS: Custom fields
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='tasks')
    subproject = db.relationship('Subproject', backref='tasks')
    sprint = db.relationship('Sprint', backref='tasks')
    assigned_to = db.relationship('User', backref='assigned_tasks')
    parent_task = db.relationship('Task', remote_side=[task_id], backref='subtasks')
    
class TaskDependency(db.Model):
    """Task dependency model for SRS requirement: Task Dependencies"""
    __tablename__ = 'task_dependency'
    
    dependency_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'), nullable=False)
    depends_on_task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'), nullable=False)
    dependency_type = db.Column(db.String(20), default='blocks')  # blocks, relates_to, duplicates
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', foreign_keys=[task_id], backref='dependencies')
    depends_on_task = db.relationship('Task', foreign_keys=[depends_on_task_id], backref='blocking_for')

class WorkLog(db.Model):
    """Work log model for SRS requirement: Time Tracking"""
    __tablename__ = 'work_log'
    
    log_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'), nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    hours_logged = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    log_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    task = db.relationship('Task', backref='work_logs')
    user = db.relationship('User', backref='work_logs')