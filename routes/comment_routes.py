from flask import Blueprint
from controllers.comment_controllers import create_comment_task, create_comment_ticket

comment_bp = Blueprint('comment', __name__)

@comment_bp.route('/task/<uuid:task_id>/create', methods=['GET', 'POST'])
def create_on_task(task_id):
    return create_comment_task(task_id)

@comment_bp.route('/ticket/<uuid:ticket_id>/create', methods=['GET', 'POST'])
def create_on_ticket(ticket_id):
    return create_comment_ticket(ticket_id)