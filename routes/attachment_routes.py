from flask import Blueprint
from controllers.attachment_controllers import upload_attachment_task, upload_attachment_ticket

attachment_bp = Blueprint('attachment', __name__)

@attachment_bp.route('/task/<uuid:task_id>/upload', methods=['GET', 'POST'])
def upload_to_task(task_id):
    return upload_attachment_task(task_id)

@attachment_bp.route('/ticket/<uuid:ticket_id>/upload', methods=['GET', 'POST'])
def upload_to_ticket(ticket_id):
    return upload_attachment_ticket(ticket_id)