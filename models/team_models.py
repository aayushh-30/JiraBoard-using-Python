from .models_models import db, UUID
import uuid
from datetime import datetime

class Team(db.Model):
    __tablename__ = 'team'
    team_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(100), nullable=False)
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    manager = db.relationship('User', backref='managed_teams')