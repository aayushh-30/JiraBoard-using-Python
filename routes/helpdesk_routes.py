from flask import Blueprint
from controllers.helpdesk_controllers import submit_helpdesk_request, get_helpdesk_requests, update_helpdesk_request

helpdesk_bp = Blueprint('helpdesk', __name__)

@helpdesk_bp.route('/create', methods=['GET', 'POST'])
def create():
    return submit_helpdesk_request()

@helpdesk_bp.route('/')
def requests():
    return get_helpdesk_requests()

@helpdesk_bp.route('/<uuid:ticket_id>/edit', methods=['GET', 'POST'])
def edit(ticket_id):
    return update_helpdesk_request(ticket_id)