from flask import Blueprint
from controllers.profile_controllers import profile, update_profile, request_role

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile')
def profile_page():
    return profile()

@profile_bp.route('/profile/update', methods=['POST'])
def update_profile_page():
    return update_profile()

@profile_bp.route('/profile/request-role', methods=['POST'])
def request_role_page():
    return request_role()

@profile_bp.route('/switch-role/<role_name>')
def switch_role_view(role_name):
    """Switch role view for users with multiple roles"""
    from flask import session, redirect, url_for, flash
    from flask_login import current_user
    
    if not current_user.is_authenticated:
        flash('Please log in to switch roles.', 'error')
        return redirect(url_for('auth.login'))
    
    # Check if user has this role
    if not current_user.has_role(role_name):
        flash('You do not have permission to switch to this role.', 'error')
        return redirect(url_for('dashboard.dashboard_page'))
    
    # Store the active role in session
    if current_user.switch_active_role(role_name):
        flash(f'Switched to {role_name.title()} role.', 'success')
    else:
        flash('Failed to switch role.', 'error')
    
    return redirect(url_for('dashboard.dashboard_page'))

@profile_bp.route('/get-user-roles')
def get_user_roles():
    """API endpoint to get current user's roles"""
    from flask import jsonify
    from flask_login import current_user
    
    if not current_user.is_authenticated:
        return jsonify({'error': 'Not authenticated'}), 401
        
    roles = current_user.get_all_roles()
    active_role = current_user.get_active_role_name()
    
    return jsonify({
        'roles': roles,
        'active_role': active_role,
        'can_switch': len(roles) > 1
    })

@profile_bp.route('/admin-switch-role/<role_name>')
def admin_switch_role_view(role_name):
    """Admin-only role view switching (for testing/demo purposes)"""
    from flask import session, redirect, url_for, flash
    from flask_login import current_user
    
    # Only admins can use this feature
    if not current_user.is_authenticated or not current_user.has_role('admin'):
        flash('Access denied. Only administrators can use role view switching.', 'error')
        return redirect(url_for('dashboard.dashboard_page'))
    
    # Valid roles for switching
    valid_roles = ['admin', 'manager', 'developer', 'client', 'viewer']
    if role_name not in valid_roles:
        flash('Invalid role specified.', 'error')
        return redirect(url_for('dashboard.dashboard_page'))
    
    # Store the role view in session (this is for UI testing, not actual role switching)
    session['role_view'] = role_name
    flash(f'Switched to {role_name.title()} view mode.', 'success')
    
    return redirect(url_for('dashboard.dashboard_page'))

@profile_bp.route('/debug-user')
def debug_user():
    """Debug route to check current user info"""
    from flask_login import current_user
    from flask import session, jsonify
    
    user_info = {
        'authenticated': current_user.is_authenticated if current_user else False,
        'username': getattr(current_user, 'username', 'None'),
        'role_name': getattr(current_user, 'role_name', 'None'),
        'user_id': getattr(current_user, 'user_id', 'None'),
        'session_role_view': session.get('role_view', 'None'),
        'session_keys': list(session.keys())
    }
    
    return f"<pre>{user_info}</pre>"
