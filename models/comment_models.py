from .models_models import db, UUID, CommentType
import uuid
from datetime import datetime

class Comment(db.Model):
    __tablename__ = 'comment'
    comment_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    content = db.Column(db.Text, nullable=False)
    type = db.Column(db.Enum(CommentType), nullable=False)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'))
    ticket_id = db.Column(UUID(as_uuid=True), db.ForeignKey('ticket.ticket_id'))
    created_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)