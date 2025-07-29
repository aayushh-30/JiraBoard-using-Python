from .models_models import db, UUID
import uuid
from datetime import datetime

class Subproject(db.Model):
    __tablename__ = 'subproject'
    subproject_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    project = db.relationship('Project', backref='subprojects')