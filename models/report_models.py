from .models_models import db, UUID
import uuid
from datetime import datetime

class Report(db.Model):
    __tablename__ = 'report'
    report_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    task_id = db.Column(UUID(as_uuid=True), db.ForeignKey('task.task_id'))
    project_id = db.Column(UUID(as_uuid=True), db.ForeignKey('project.project_id'))
    manager_id = db.Column(UUID(as_uuid=True), db.ForeignKey('manager.manager_id'))
    client_id = db.Column(UUID(as_uuid=True), db.ForeignKey('client.client_id'))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)