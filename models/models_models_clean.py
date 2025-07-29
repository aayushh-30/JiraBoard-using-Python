from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID, ENUM, JSONB
import uuid
import enum
from datetime import datetime

db = SQLAlchemy()

# ENUM types
class TaskStatus(enum.Enum):
    todo = 'todo'
    in_progress = 'in_progress'
    done = 'done'

class TaskType(enum.Enum):
    bug = 'bug'
    feature = 'feature'
    task = 'task'

class TicketStatus(enum.Enum):
    open = 'open'
    in_progress = 'in_progress'
    closed = 'closed'

class TicketPriority(enum.Enum):
    low = 'low'
    medium = 'medium'
    high = 'high'

class RoleName(enum.Enum):
    admin = 'admin'
    manager = 'manager'
    developer = 'developer'
    client = 'client'
    viewer = 'viewer'
    pending = 'pending'

class CommentType(enum.Enum):
    task = 'task'
    ticket = 'ticket'

# Note: Individual model imports are handled by each model file to avoid circular imports
# Models define their own relationships within their respective files
