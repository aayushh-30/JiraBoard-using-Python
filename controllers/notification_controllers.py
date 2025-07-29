from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.notification_template_models import NotificationTemplate
from models.models_models import db, RoleName
from forms.notification_forms import NotificationTemplateForm
from datetime import datetime
import uuid

@login_required
def create_notification_template():
    if current_user.role.role_name != RoleName.admin:
        flash('Only admins can create notification templates.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = NotificationTemplateForm()
    if form.validate_on_submit():
        template = NotificationTemplate(
            template_id=uuid.uuid4(),
            name=form.name.data,
            content=form.content.data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(template)
        db.session.commit()
        flash('Notification template created successfully!', 'success')
        return redirect(url_for('notification.templates'))
    return render_template('create_notification.html', form=form)

@login_required
def get_notification_templates():
    if current_user.role.role_name != RoleName.admin:
        flash('Only admins can view notification templates.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    templates = NotificationTemplate.query.all()
    return render_template('list_notification.html', templates=templates)