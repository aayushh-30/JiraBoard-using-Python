from .models_models import db, UUID, TicketStatus, TicketPriority
import uuid
from datetime import datetime

class Ticket(db.Model):
    __tablename__ = 'ticket'
    ticket_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    status = db.Column(db.Enum(TicketStatus), nullable=False, default='open')
    priority = db.Column(db.Enum(TicketPriority), nullable=False, default='medium')
    raised_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)