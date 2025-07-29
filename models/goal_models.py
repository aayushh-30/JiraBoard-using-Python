from .models_models import db, UUID
from sqlalchemy import Enum
from datetime import datetime
import uuid

# Define ENUM types to match database schema
from enum import Enum as PyEnum

class GoalStatus(PyEnum):
    PENDING = 'pending'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'
    CANCELLED = 'cancelled'

class GoalPriority(PyEnum):
    LOW = 'low'
    MEDIUM = 'medium'
    HIGH = 'high'
    URGENT = 'urgent'

class GoalCategory(PyEnum):
    PERSONAL = 'personal'
    TEAM = 'team'
    PROJECT = 'project'
    ORGANIZATIONAL = 'organizational'

class Goal(db.Model):
    __tablename__ = 'goal'
    goal_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    priority = db.Column(Enum(GoalPriority), default=GoalPriority.MEDIUM, nullable=False)
    status = db.Column(Enum(GoalStatus), default=GoalStatus.PENDING, nullable=False)
    target_date = db.Column(db.DateTime)
    completion_date = db.Column(db.DateTime)
    progress_percentage = db.Column(db.Float, default=0.0)
    category = db.Column(Enum(GoalCategory), default=GoalCategory.PERSONAL, nullable=False)
    is_milestone = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='goals')
    user = db.relationship('User', backref='goals')
    
    def mark_as_completed(self):
        """Mark goal as completed"""
        self.status = GoalStatus.COMPLETED
        self.completion_date = datetime.utcnow()
        self.progress_percentage = 100.0
        db.session.commit()
    
    def update_progress(self, percentage):
        """Update goal progress"""
        self.progress_percentage = max(0, min(100, percentage))
        if self.progress_percentage == 100:
            self.status = GoalStatus.COMPLETED
            self.completion_date = datetime.utcnow()
        elif self.progress_percentage > 0:
            self.status = GoalStatus.IN_PROGRESS
        db.session.commit()
    
    def is_overdue(self):
        """Check if goal is overdue"""
        if self.target_date and self.status not in [GoalStatus.COMPLETED, GoalStatus.CANCELLED]:
            return datetime.utcnow() > self.target_date
        return False
    
    def to_dict(self):
        """Convert goal to dictionary for JSON serialization"""
        return {
            'goal_id': str(self.goal_id),
            'title': self.title,
            'description': self.description,
            'project_id': str(self.project_id) if self.project_id else None,
            'user_id': str(self.user_id),
            'priority': self.priority.value if self.priority else None,
            'status': self.status.value if self.status else None,
            'target_date': self.target_date.isoformat() if self.target_date else None,
            'completion_date': self.completion_date.isoformat() if self.completion_date else None,
            'progress_percentage': self.progress_percentage,
            'category': self.category.value if self.category else None,
            'is_milestone': self.is_milestone,
            'is_overdue': self.is_overdue(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
