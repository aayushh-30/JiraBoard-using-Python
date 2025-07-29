from .models_models import db, UUID
import uuid
from datetime import datetime

class Attachment(db.Model):
    __tablename__ = 'attachment'
    attachment_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_name = db.Column(db.String(100), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'))
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.ticket_id'))
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)