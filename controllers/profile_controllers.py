from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from permissions import ROLE_PERMISSIONS, AVAILABLE_PERMISSIONS

# Mock data for roles and profile
available_roles = ['viewer', 'developer', 'manager', 'client']
admin_contact = {
    'email': 'admin@dhaniya.com',
    'phone': '+91-9876543210'
}

def get_user_permissions(user_role):
    """Get actual permissions for a user role"""
    return ROLE_PERMISSIONS.get(user_role, [])

def get_permission_descriptions(permissions):
    """Get human-readable descriptions for permissions"""
    return {perm: AVAILABLE_PERMISSIONS.get(perm, perm) for perm in permissions}

# Mock user profiles data
user_profiles = {
    "1": {
        'phone': '',
        'address': '',
        'bio': '',
        'organization': '',
        'experience': '',
        'education': '',
        'location': '',
        'current_roles': ['viewer'],
        'requested_roles': []
    }
}

@login_required
def profile():
    """Display user profile"""
    user_id = current_user.get_id()
    profile_data = user_profiles.get(user_id, user_profiles["1"])
    
    # Get actual user permissions based on their role
    user_role = getattr(current_user, 'role_name', 'viewer')
    user_permissions = get_user_permissions(user_role)
    permission_descriptions = get_permission_descriptions(user_permissions)
    
    return render_template('profile.html', 
                         profile=profile_data, 
                         available_roles=available_roles,
                         admin_contact=admin_contact,
                         user=current_user,
                         user_permissions=user_permissions,
                         permission_descriptions=permission_descriptions)

@login_required
def update_profile():
    """Update user profile"""
    if request.method == 'POST':
        user_id = current_user.get_id()
        
        # Update profile data
        user_profiles[user_id] = {
            'phone': request.form.get('phone', ''),
            'address': request.form.get('address', ''),
            'bio': request.form.get('bio', ''),
            'organization': request.form.get('organization', ''),
            'experience': request.form.get('experience', ''),
            'education': request.form.get('education', ''),
            'location': request.form.get('location', ''),
            'current_roles': user_profiles.get(user_id, {}).get('current_roles', ['viewer']),
            'requested_roles': user_profiles.get(user_id, {}).get('requested_roles', [])
        }
        
        flash('Profile updated successfully! 🌿', 'success')
        return redirect(url_for('profile.profile'))
    
    return redirect(url_for('profile.profile'))

@login_required
def request_role():
    """Request a new role from admin"""
    if request.method == 'POST':
        requested_role = request.form.get('role')
        user_id = current_user.get_id()
        
        if requested_role and requested_role in available_roles:
            if user_id not in user_profiles:
                user_profiles[user_id] = user_profiles["1"].copy()
            
            if requested_role not in user_profiles[user_id]['requested_roles']:
                user_profiles[user_id]['requested_roles'].append(requested_role)
                flash(f'Role request for "{requested_role}" submitted! Admin will review soon. 🌱', 'success')
            else:
                flash(f'You have already requested "{requested_role}" role! ⏳', 'info')
        else:
            flash('Invalid role selected! 🚫', 'error')
    
    return redirect(url_for('profile.profile_page'))
