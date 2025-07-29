from .models_models import db, UUID
import uuid

class DeveloperTeam(db.Model):
    __tablename__ = 'developer_team'
    developer_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), primary_key=True)
    team_id = db.Column(UUID(as_uuid=True), db.ForeignKey('team.team_id'), primary_key=True)
    
    # Relationships
    developer = db.relationship('User', backref='team_memberships')
    team = db.relationship('Team', backref='developer_memberships')