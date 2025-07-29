from .models_models import db, UUID, RoleName
import uuid

class Role(db.Model):
    __tablename__ = 'role'
    role_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name = db.Column(db.Enum(RoleName), nullable=False, unique=True)