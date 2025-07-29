from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.attachment_models import Attachment
from models.task_models import Task
from models.ticket_models import Ticket
from models.models_models import db, RoleName
from forms.attachment_forms import AttachmentForm
from datetime import datetime
import uuid
import os

@login_required
def upload_attachment_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role.role_name not in [RoleName.manager, RoleName.developer] or (current_user.role.role_name == RoleName.developer and task.assigned_to_id != current_user.user_id):
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = AttachmentForm()
    if form.validate_on_submit():
        file = form.file.data
        file_name = file.filename
        file_path = os.path.join('static/uploads', file_name)
        file.save(file_path)
        attachment = Attachment(
            attachment_id=uuid.uuid4(),
            file_name=file_name,
            file_path=file_path,
            task_id=task_id,
            created_by_id=current_user.user_id,
            created_at=datetime.utcnow()
        )
        db.session.add(attachment)
        db.session.commit()
        flash('Attachment uploaded successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=task.project_id))
    return render_template('upload_task_attachment.html', form=form, task=task)

@login_required
def upload_attachment_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role.role_name not in [RoleName.client, RoleName.manager] or ticket.raised_by_id != current_user.user_id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = AttachmentForm()
    if form.validate_on_submit():
        file = form.file.data
        file_name = file.filename
        file_path = os.path.join('static/uploads', file_name)
        file.save(file_path)
        attachment = Attachment(
            attachment_id=uuid.uuid4(),
            file_name=file_name,
            file_path=file_path,
            ticket_id=ticket_id,
            created_by_id=current_user.user_id,
            created_at=datetime.utcnow()
        )
        db.session.add(attachment)
        db.session.commit()
        flash('Attachment uploaded successfully!', 'success')
        return redirect(url_for('ticket.tickets'))
    return render_template('upload_ticket_attachment.html', form=form, ticket=ticket)