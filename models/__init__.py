# Import all models to ensure they're registered with SQLAlchemy
from .models_models import db
from .role_models import Role
from .user_models import User
from .login_models import Login
from .team_models import Team
from .project_models import Project
from .subproject_models import Subproject
from .sprint_models import Sprint
from .epic_models import Epic
from .developer_team_models import DeveloperTeam
from .developer_project_models import DeveloperProject
from .manager_project_models import ManagerProject

# Add other model imports as needed
try:
    from .task_models import Task
except ImportError:
    pass

try:
    from .ticket_models import Ticket
except ImportError:
    pass

try:
    from .comment_models import Comment
except ImportError:
    pass

# Export commonly used models
__all__ = [
    'db', 'Role', 'User', 'Login', 'Team', 'Project', 'Subproject', 'Sprint', 'Epic',
    'DeveloperTeam', 'DeveloperProject', 'ManagerProject'
]
