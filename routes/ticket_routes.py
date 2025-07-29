from flask import Blueprint
from controllers.ticket_controllers import create_ticket, get_tickets, update_ticket

ticket_bp = Blueprint('ticket', __name__)

@ticket_bp.route('/create', methods=['GET', 'POST'])
def create():
    return create_ticket()

@ticket_bp.route('/')
def tickets():
    return get_tickets()

@ticket_bp.route('/<uuid:ticket_id>/edit', methods=['GET', 'POST'])
def edit(ticket_id):
    return update_ticket(ticket_id)