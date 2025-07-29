from .models_models import db, UUID
import uuid

class ManagerProject(db.Model):
    __tablename__ = 'manager_project'
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), primary_key=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), primary_key=True)
    
    # Relationships
    manager = db.relationship('User', backref='managed_project_assignments')
    project = db.relationship('Project', backref='manager_assignments')