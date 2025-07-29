from .models_models import db, UUID
import uuid
from datetime import datetime

class Manager(db.Model):
    __tablename__ = 'manager'
    manager_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False, unique=True)
    contact_no = db.Column(db.String(15))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)