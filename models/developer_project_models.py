from .models_models import db, UUID
import uuid

class DeveloperProject(db.Model):
    __tablename__ = 'developer_project'
    developer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), primary_key=True)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), primary_key=True)
    
    # Relationships
    developer = db.relationship('User', backref='project_assignments')
    project = db.relationship('Project', backref='developer_assignments')