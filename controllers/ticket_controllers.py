from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from permissions import require_permission, require_permission_or_ownership
from models.ticket_models import Ticket
from models.models_models import db, RoleName
from forms.ticket_forms import TicketForm
from datetime import datetime
import uuid

@login_required
@require_permission('ticket_create')
def create_ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            ticket_id=uuid.uuid4(),
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            priority=form.priority.data,
            raised_by_id=current_user.user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(ticket)
        db.session.commit()
        flash('Ticket created successfully!', 'success')
        return redirect(url_for('ticket.tickets'))
    return render_template('create_ticket.html', form=form)

@login_required
@require_permission('ticket_view')
def get_tickets():
    # Show tickets based on user role and permissions
    user_role = getattr(current_user, 'role_name', None)
    
    if user_role in ['admin', 'manager']:
        tickets = Ticket.query.all()
    else:
        # For other roles, show only their own tickets
        tickets = Ticket.query.filter_by(raised_by_id=current_user.user_id).all()
    
    return render_template('list_ticket.html', tickets=tickets)

def check_ticket_ownership(ticket_id):
    """Helper function to check if current user owns the ticket"""
    ticket = Ticket.query.get(ticket_id)
    return ticket and ticket.raised_by_id == current_user.user_id

@login_required
@require_permission_or_ownership('ticket_edit', check_ticket_ownership)
def update_ticket(ticket_id):
    ticket = Ticket.query.get_or_404(ticket_id)
    
    form = TicketForm(obj=ticket)
    if form.validate_on_submit():
        ticket.title = form.title.data
        ticket.description = form.description.data
        ticket.status = form.status.data
        ticket.priority = form.priority.data
        ticket.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Ticket updated successfully!', 'success')
        return redirect(url_for('ticket.tickets'))
    return render_template('edit_ticket.html', form=form, ticket=ticket)