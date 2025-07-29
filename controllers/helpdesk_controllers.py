from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.ticket_models import Ticket
from models.models_models import db, RoleName, TicketStatus, TicketPriority
from forms.ticket_forms import HelpdeskForm
from datetime import datetime
import uuid

@login_required
def submit_helpdesk_request():
    form = HelpdeskForm()
    if form.validate_on_submit():
        ticket = Ticket(
            ticket_id=uuid.uuid4(),
            title=form.title.data,
            description=form.description.data,
            status=TicketStatus.open,
            priority=TicketPriority.medium,
            raised_by_id=current_user.user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Helpdesk request submitted successfully!', 'success')
        return redirect(url_for('helpdesk.requests'))
    return render_template('create_helpdesk.html', form=form)
    
@login_required
def get_helpdesk_requests():
    if current_user.role.role_name == RoleName.admin:
        requests = db.session.query(Ticket).all()
    else:
        requests = db.session.query(Ticket).filter_by(raised_by_id=current_user.user_id).all()
    return render_template('list_helpdesk.html', requests=requests)
    
@login_required
def update_helpdesk_request(ticket_id):
    ticket = db.session.query(Ticket).get_or_404(ticket_id)
    if current_user.role.role_name != RoleName.admin and ticket.raised_by_id != current_user.user_id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = HelpdeskForm(obj=ticket)
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.updated_at = datetime.utcnow()
        if current_user.role.role_name == RoleName.admin:
            ticket.status = form.status.data
            ticket.priority = form.priority.data
        db.session.commit()
        flash('Helpdesk request updated successfully!', 'success')
        return redirect(url_for('helpdesk.requests'))
    return render_template('edit_helpdesk.html', form=form, ticket=ticket)