from flask import Blueprint
from controllers.notification_controllers import create_notification_template, get_notification_templates

notification_bp = Blueprint('notification', __name__)

@notification_bp.route('/create', methods=['GET', 'POST'])
def create():
    return create_notification_template()

@notification_bp.route('/')
def templates():
    return get_notification_templates()