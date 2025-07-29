from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.user_models import User
from models.role_models import Role
from models.models_models import db, RoleName
from forms.auth_forms import RoleAssignmentForm

@login_required
def list_pending_users():
    if current_user.role.role_name != RoleName.admin:
        flash('Only admins can view pending users.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    pending_role = Role.query.filter_by(role_name=RoleName.pending).first()
    users = User.query.filter_by(role_id=pending_role.role_id).all()
    return render_template('pending_users_role.html', users=users)