from flask import Blueprint
from controllers.admin_controllers import (
    admin_dashboard,
    admin_users,
    pending_users,
    system_settings,
    toggle_user_status,
    approve_user,
    delete_user,
    create_user,
    bulk_actions,
    save_settings,
    test_email,
    database_optimize,
    database_analyze,
    database_integrity,
    get_user_roles,
    add_user_role,
    remove_user_role,
    set_primary_role
)
from controllers.admin_team_controllers import (
    team_management,
    add_member_to_team,
    remove_member_from_team,
    create_team,
    get_unassigned_users
)

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Main admin route
@admin_bp.route('/')
def admin_home():
    return admin_dashboard()

# Dashboard routes
@admin_bp.route('/dashboard')
def dashboard():
    return admin_dashboard()

# User management routes
@admin_bp.route('/users')
def users():
    return admin_users()

@admin_bp.route('/pending-users')
def pending_users_route():
    return pending_users()

@admin_bp.route('/user/<user_id>/toggle-status', methods=['POST'])
def toggle_status(user_id):
    return toggle_user_status(user_id)

# Multi-role management routes
@admin_bp.route('/user-roles/<user_id>')
def user_roles(user_id):
    return get_user_roles(user_id)

@admin_bp.route('/add-user-role', methods=['POST'])
def add_role():
    return add_user_role()

@admin_bp.route('/remove-user-role', methods=['POST'])
def remove_role():
    return remove_user_role()

@admin_bp.route('/set-primary-role', methods=['POST'])
def set_primary():
    return set_primary_role()

@admin_bp.route('/user/<user_id>/approve')
def approve(user_id):
    return approve_user(user_id)

@admin_bp.route('/user/<user_id>/delete', methods=['DELETE'])
def delete(user_id):
    return delete_user(user_id)

@admin_bp.route('/create-user', methods=['POST'])
def create():
    return create_user()

@admin_bp.route('/bulk-actions', methods=['POST'])
def bulk():
    return bulk_actions()

# System settings routes
@admin_bp.route('/system-settings')
def settings():
    return system_settings()

@admin_bp.route('/system-settings', methods=['POST'])
def save_settings_route():
    return save_settings()

@admin_bp.route('/test-email', methods=['POST'])
def test_email_route():
    return test_email()

@admin_bp.route('/settings')  # Add this route for /admin/settings
def admin_settings():
    return system_settings()

@admin_bp.route('/audit')  # Add this route for /admin/audit
def admin_audit():
    # For now, redirect to audit logs or create simple audit view
    from flask import render_template
    return render_template('admin/audit.html')

# Database management routes
@admin_bp.route('/database/optimize', methods=['POST'])
def db_optimize():
    return database_optimize()

@admin_bp.route('/database/analyze', methods=['POST'])
def db_analyze():
    return database_analyze()

@admin_bp.route('/database/check-integrity', methods=['POST'])
def db_integrity():
    return database_integrity()

# Team management routes
@admin_bp.route('/teams')
def teams():
    return team_management()

@admin_bp.route('/teams/create', methods=['POST'])
def create_team_route():
    return create_team()

@admin_bp.route('/teams/add-member', methods=['POST'])
def add_member():
    return add_member_to_team()

@admin_bp.route('/teams/remove-member', methods=['DELETE'])
def remove_member():
    return remove_member_from_team()

@admin_bp.route('/teams/unassigned-users', methods=['GET'])
def unassigned_users():
    return get_unassigned_users()
