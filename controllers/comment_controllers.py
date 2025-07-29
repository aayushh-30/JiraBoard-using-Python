from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.comment_models import Comment
from models.task_models import Task
from models.ticket_models import Ticket
from models.models_models import db, RoleName
from forms.comment_forms import CommentForm
from datetime import datetime
import uuid

@login_required
def create_comment_task(task_id):
    task = Task.query.get_or_404(task_id)
    if current_user.role.role_name not in [RoleName.manager, RoleName.developer] or (current_user.role.role_name == RoleName.developer and task.assigned_to_id != current_user.user_id):
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment_id=uuid.uuid4(),
            content=form.content.data,
            type='task',
            task_id=task_id,
            created_by_id=current_user.user_id,
            created_at=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=task.project_id))
    return render_template('create_task_comment.html', form=form, task=task)

@login_required
def create_comment_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    if current_user.role.role_name not in [RoleName.client, RoleName.manager] or ticket.raised_by_id != current_user.user_id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(
            comment_id=uuid.uuid4(),
            content=form.content.data,
            type='ticket',
            ticket_id=ticket_id,
            created_by_id=current_user.user_id,
            created_at=datetime.utcnow()
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
        return redirect(url_for('ticket.tickets'))
    return render_template('create_ticket_comment.html', form=form, ticket=ticket)