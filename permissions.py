"""
Permission-based access control system for Jira Board Application
Handles role-based permissions and feature-level access control
"""

from functools import wraps
from flask import abort, flash, redirect, url_for, request
from flask_login import current_user

# Define all available permissions/features in the system
AVAILABLE_PERMISSIONS = {
    # Team Management
    'team_create': 'Create new teams',
    'team_edit': 'Edit team details', 
    'team_delete': 'Delete teams',
    'team_view': 'View team information',
    'team_assign_users': 'Assign users to teams',
    
    # Project Management
    'project_create': 'Create new projects',
    'project_edit': 'Edit project details',
    'project_delete': 'Delete projects',
    'project_view': 'View projects',
    'project_list': 'List all projects',
    'project_assign': 'Assign projects to teams',
    
    # Task Management
    'task_create': 'Create tasks',
    'task_edit': 'Edit tasks',
    'task_delete': 'Delete tasks',
    'task_view': 'View tasks',
    'task_assign': 'Assign tasks to users',
    
    # Epic Management
    'epic_create': 'Create epics',
    'epic_edit': 'Edit epics',
    'epic_delete': 'Delete epics',
    'epic_view': 'View epics',
    
    # Story Management
    'story_create': 'Create stories',
    'story_edit': 'Edit stories', 
    'story_delete': 'Delete stories',
    'story_view': 'View stories',
    
    # Bug Management
    'bug_create': 'Report bugs',
    'bug_edit': 'Edit bug reports',
    'bug_delete': 'Delete bug reports',
    'bug_view': 'View bugs',
    'bug_assign': 'Assign bugs to users',
    
    # User Management
    'user_create': 'Create new users',
    'user_edit': 'Edit user details',
    'user_delete': 'Delete users',
    'user_view': 'View user profiles',
    'user_approve': 'Approve user registrations',
    'user_role_request': 'Request role changes',
    'user_role_approve': 'Approve role change requests',
    
    # Dashboard & Reports
    'dashboard_view': 'View dashboard',
    'reports_view': 'View reports',
    'reports_create': 'Create custom reports',
    
    # Admin Functions
    'admin_panel': 'Access admin panel',
    'system_settings': 'Modify system settings',
    'database_manage': 'Database management',
    
    # Sprint Management
    'sprint_create': 'Create sprints',
    'sprint_edit': 'Edit sprints',
    'sprint_delete': 'Delete sprints',
    'sprint_view': 'View sprints',
    
    # Board Management
    'board_create': 'Create boards',
    'board_edit': 'Edit boards',
    'board_delete': 'Delete boards',
    'board_view': 'View boards',
    
    # Workflow Management
    'workflow_create': 'Create workflows',
    'workflow_edit': 'Edit workflows',
    'workflow_delete': 'Delete workflows',
    'workflow_view': 'View workflows',
    
    # Ticket Management
    'ticket_create': 'Create tickets',
    'ticket_edit': 'Edit tickets',
    'ticket_delete': 'Delete tickets',
    'ticket_view': 'View tickets',
    'ticket_assign': 'Assign tickets to users',
    
    # Goal Management
    'goal_create': 'Create goals',
    'goal_edit': 'Edit goals',
    'goal_delete': 'Delete goals',
    'goal_view': 'View goals',
    'goal_assign': 'Assign goals to users'
}

# Role-based permission mapping
ROLE_PERMISSIONS = {
    'admin': [
        # Admin has ALL permissions
        'team_create', 'team_edit', 'team_delete', 'team_view', 'team_assign_users',
        'project_create', 'project_edit', 'project_delete', 'project_view', 'project_list', 'project_assign',
        'task_create', 'task_edit', 'task_delete', 'task_view', 'task_assign',
        'epic_create', 'epic_edit', 'epic_delete', 'epic_view',
        'story_create', 'story_edit', 'story_delete', 'story_view',
        'bug_create', 'bug_edit', 'bug_delete', 'bug_view', 'bug_assign',
        'user_create', 'user_edit', 'user_delete', 'user_view', 'user_approve', 'user_role_approve',
        'dashboard_view', 'reports_view', 'reports_create',
        'admin_panel', 'system_settings', 'database_manage',
        'sprint_create', 'sprint_edit', 'sprint_delete', 'sprint_view',
        'board_create', 'board_edit', 'board_delete', 'board_view',
        'workflow_create', 'workflow_edit', 'workflow_delete', 'workflow_view',
        'ticket_create', 'ticket_edit', 'ticket_delete', 'ticket_view', 'ticket_assign',
        'goal_create', 'goal_edit', 'goal_delete', 'goal_view', 'goal_assign'
    ],
    
    'manager': [
        # Manager permissions - can manage teams and projects, approve users
        'team_edit', 'team_view', 'team_assign_users',
        'project_create', 'project_edit', 'project_view', 'project_list', 'project_assign',
        'task_create', 'task_edit', 'task_view', 'task_assign',
        'epic_create', 'epic_edit', 'epic_view',
        'story_create', 'story_edit', 'story_view',
        'bug_create', 'bug_edit', 'bug_view', 'bug_assign',
        'user_view', 'user_approve', 'user_role_approve',
        'dashboard_view', 'reports_view', 'reports_create',
        'sprint_create', 'sprint_edit', 'sprint_view',
        'board_create', 'board_edit', 'board_view',
        'workflow_create', 'workflow_edit', 'workflow_view',
        'ticket_create', 'ticket_edit', 'ticket_view', 'ticket_assign',
        'goal_create', 'goal_edit', 'goal_view', 'goal_assign'
    ],
    
    'developer': [
        # Developer permissions - can work on tasks and create content
        'team_view',
        'project_view', 'project_list',
        'task_create', 'task_edit', 'task_view',
        'epic_view',
        'story_create', 'story_edit', 'story_view',
        'bug_create', 'bug_edit', 'bug_view',
        'user_view', 'user_role_request',
        'dashboard_view',
        'sprint_view',
        'board_view',
        'goal_create', 'goal_edit', 'goal_view'
    ],
    
    'client': [
        # Client permissions - limited to viewing and commenting
        'team_view',
        'project_view',
        'task_view',
        'epic_view',
        'story_view',
        'bug_create', 'bug_view',
        'user_view',
        'dashboard_view',
        'sprint_view',
        'board_view',
        'ticket_create', 'ticket_view',
        'goal_view'
    ],
    
    'viewer': [
        # Viewer permissions - read-only access
        'team_view',
        'project_view',
        'task_view',
        'epic_view',
        'story_view',
        'bug_view',
        'user_view',
        'dashboard_view',
        'sprint_view',
        'board_view',
        'goal_view'
    ]
}

def has_permission(user, permission):
    """
    Check if a user has a specific permission based on their role
    
    Args:
        user: Current user object with role_name attribute
        permission: Permission string to check
        
    Returns:
        bool: True if user has permission, False otherwise
    """
    if not user or not user.is_authenticated:
        return False
    
    user_role = getattr(user, 'role_name', None)
    
    if not user_role:
        # Try alternative role attribute names
        alt_role = getattr(user, 'role', None)
        if alt_role:
            user_role = getattr(alt_role, 'role_name', None)
            if hasattr(alt_role, 'value'):
                user_role = alt_role.value
        
        if not user_role:
            return False
    
    # Get permissions for user's role
    if user_role and isinstance(user_role, str):
        role_permissions = ROLE_PERMISSIONS.get(user_role, [])
        return permission in role_permissions
    
    return False

def require_permission(permission):
    """
    Decorator to require specific permission for a route
    
    Usage:
        @require_permission('project_create')
        def create_project():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            if not has_permission(current_user, permission):
                flash(f'Access denied. You do not have permission to {AVAILABLE_PERMISSIONS.get(permission, permission)}.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_any_permission(permissions):
    """
    Decorator to require ANY of the specified permissions for a route
    
    Usage:
        @require_any_permission(['team_view', 'team_edit'])
        def team_function():
            pass
    """
    if isinstance(permissions, str):
        permissions = [permissions]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            # Check if user has any of the required permissions
            has_any = any(has_permission(current_user, perm) for perm in permissions)
            
            if not has_any:
                permission_names = [AVAILABLE_PERMISSIONS.get(p, p) for p in permissions]
                flash(f'Access denied. You need one of these permissions: {", ".join(permission_names)}.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_all_permissions(permissions):
    """
    Decorator to require ALL of the specified permissions for a route
    
    Usage:
        @require_all_permissions(['team_edit', 'user_assign'])
        def assign_user_to_team():
            pass
    """
    if isinstance(permissions, str):
        permissions = [permissions]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            # Check if user has all required permissions
            missing_permissions = [p for p in permissions if not has_permission(current_user, p)]
            
            if missing_permissions:
                permission_names = [AVAILABLE_PERMISSIONS.get(p, p) for p in missing_permissions]
                flash(f'Access denied. You are missing these permissions: {", ".join(permission_names)}.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def require_role(roles):
    """
    Decorator to require specific role(s) for a route
    
    Usage:
        @require_role(['admin', 'manager'])
        def admin_function():
            pass
    """
    if isinstance(roles, str):
        roles = [roles]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            user_role = getattr(current_user, 'role_name', None)
            if user_role not in roles:
                flash(f'Access denied. This page requires {" or ".join(roles)} role.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def can_user_access_team(user, team_id):
    """
    Check if user can access a specific team
    
    Args:
        user: Current user object
        team_id: Team ID to check access for
        
    Returns:
        bool: True if user can access team
    """
    if not user or not user.is_authenticated:
        return False
    
    # Admin and manager can access all teams
    if getattr(user, 'role_name', None) in ['admin', 'manager']:
        return True
    
    # TODO: Check if user is member of the team
    # This would require a database query to check team membership
    return True  # For now, allow access

def can_user_access_project(user, project_id):
    """
    Check if user can access a specific project
    
    Args:
        user: Current user object
        project_id: Project ID to check access for
        
    Returns:
        bool: True if user can access project
    """
    if not user or not user.is_authenticated:
        return False
    
    # Admin and manager can access all projects
    if getattr(user, 'role_name', None) in ['admin', 'manager']:
        return True
    
    # TODO: Check if user is assigned to the project
    # This would require a database query to check project assignment
    return True  # For now, allow access

def get_user_permissions(user):
    """
    Get all permissions for a user based on their role
    
    Args:
        user: User object with role_name attribute
        
    Returns:
        list: List of permissions the user has
    """
    if not user or not user.is_authenticated:
        return []
    
    user_role = getattr(user, 'role_name', None)
    if user_role is None:
        return []
    
    return ROLE_PERMISSIONS.get(str(user_role), [])

def get_available_roles():
    """
    Get list of all available roles in the system
    
    Returns:
        list: List of role names
    """
    return list(ROLE_PERMISSIONS.keys())

# Default teams that should be created in the database
DEFAULT_TEAMS = [
    {
        'name': 'Frontend Development',
        'description': 'Responsible for user interface and user experience development',
        'department': 'Engineering'
    },
    {
        'name': 'Backend Development', 
        'description': 'Responsible for server-side logic and database management',
        'department': 'Engineering'
    },
    {
        'name': 'DevOps',
        'description': 'Responsible for deployment, infrastructure, and CI/CD',
        'department': 'Engineering'
    },
    {
        'name': 'Quality Assurance',
        'description': 'Responsible for testing and quality control',
        'department': 'Engineering'
    },
    {
        'name': 'UI/UX Design',
        'description': 'Responsible for user interface and experience design',
        'department': 'Design'
    },
    {
        'name': 'Product Management',
        'description': 'Responsible for product strategy and requirements',
        'department': 'Product'
    },
    {
        'name': 'Data Science',
        'description': 'Responsible for data analysis and machine learning',
        'department': 'Engineering'
    },
    {
        'name': 'Security',
        'description': 'Responsible for application and infrastructure security',
        'department': 'Engineering'
    },
    {
        'name': 'Mobile Development',
        'description': 'Responsible for mobile application development',
        'department': 'Engineering'
    },
    {
        'name': 'Support',
        'description': 'Responsible for customer support and issue resolution',
        'department': 'Operations'
    }
]

def require_permission_or_ownership(permission, ownership_check_func=None):
    """
    Decorator that allows access if user has permission OR owns the resource
    
    Usage:
        @require_permission_or_ownership('task_edit', lambda task_id: current_user.user_id == get_task_owner(task_id))
        def edit_task(task_id):
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            # Check permission first
            if has_permission(current_user, permission):
                return f(*args, **kwargs)
            
            # If no permission, check ownership
            if ownership_check_func and ownership_check_func(*args, **kwargs):
                return f(*args, **kwargs)
            
            flash(f'Access denied. You do not have permission to {AVAILABLE_PERMISSIONS.get(permission, permission)} or own this resource.', 'danger')
            return redirect(url_for('dashboard.dashboard_page'))
        
        return decorated_function
    return decorator

def conditional_permission(condition_func, permission):
    """
    Decorator that applies permission check only if condition is met
    
    Usage:
        @conditional_permission(lambda: request.method == 'POST', 'task_create')
        def task_endpoint():
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            # Apply permission check only if condition is met
            if condition_func() and not has_permission(current_user, permission):
                flash(f'Access denied. You do not have permission to {AVAILABLE_PERMISSIONS.get(permission, permission)}.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def resource_permission(permission, resource_access_func):
    """
    Decorator for resource-specific permission checks
    
    Usage:
        @resource_permission('project_edit', lambda project_id: can_user_access_project(current_user, project_id))
        def edit_project(project_id):
            pass
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login', next=request.url))
            
            # Check basic permission
            if not has_permission(current_user, permission):
                flash(f'Access denied. You do not have permission to {AVAILABLE_PERMISSIONS.get(permission, permission)}.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            # Check resource-specific access
            if not resource_access_func(*args, **kwargs):
                flash('Access denied. You do not have access to this resource.', 'danger')
                return redirect(url_for('dashboard.dashboard_page'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

# Convenience decorators for common permission patterns
def admin_required(f):
    """Shortcut decorator for admin-only access"""
    return require_role('admin')(f)

def manager_or_admin_required(f):
    """Shortcut decorator for manager or admin access"""
    return require_role(['admin', 'manager'])(f)

def authenticated_required(f):
    """Basic authentication decorator"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Team and project specific decorators
def team_access_required(f):
    """Decorator to check team access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Extract team_id from args or kwargs
        team_id = kwargs.get('team_id') or (args[0] if args else None)
        
        if not can_user_access_team(current_user, team_id):
            flash('Access denied. You do not have access to this team.', 'danger')
            return redirect(url_for('dashboard.dashboard_page'))
        
        return f(*args, **kwargs)
    return decorated_function

def project_access_required(f):
    """Decorator to check project access"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login', next=request.url))
        
        # Extract project_id from args or kwargs
        project_id = kwargs.get('project_id') or (args[0] if args else None)
        
        if not can_user_access_project(current_user, project_id):
            flash('Access denied. You do not have access to this project.', 'danger')
            return redirect(url_for('dashboard.dashboard_page'))
        
        return f(*args, **kwargs)
    return decorated_function

# Template context processors for permissions
def register_permission_context_processors(app):
    """Register template context processors for permissions"""
    
    @app.context_processor
    def inject_permissions():
        """Make permission functions available in templates"""
        return {
            'has_permission': lambda permission: has_permission(current_user, permission) if current_user.is_authenticated else False,
            'user_permissions': get_user_permissions(current_user) if current_user.is_authenticated else [],
            'available_permissions': AVAILABLE_PERMISSIONS,
            'user_role': getattr(current_user, 'role_name', None) if current_user.is_authenticated else None
        }

# Permission checking utility functions
def check_permission_ajax(permission):
    """
    Check permission for AJAX requests
    Returns JSON response
    """
    from flask import jsonify
    
    if not current_user.is_authenticated:
        return jsonify({'error': 'Authentication required', 'status': 401}), 401
    
    if not has_permission(current_user, permission):
        return jsonify({
            'error': f'Permission denied: {AVAILABLE_PERMISSIONS.get(permission, permission)}',
            'status': 403
        }), 403
    
    return None  # No error

def require_permission_ajax(permission):
    """
    Decorator for AJAX endpoints requiring permissions
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            error_response = check_permission_ajax(permission)
            if error_response:
                return error_response
            return f(*args, **kwargs)
        return decorated_function
    return decorator
