from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.audit_log_models import AuditLog
from models.models_models import db, RoleName

@login_required
def get_audit_logs():
    if current_user.role.role_name != RoleName.admin:
        flash('Only admins can view audit logs.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    logs = AuditLog.query.all()
    return render_template('list_audit.html', logs=logs)