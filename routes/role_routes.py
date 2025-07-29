from flask import Blueprint
from controllers.role_controllers import list_pending_users

role_bp = Blueprint('role', __name__)

@role_bp.route('/pending-users')
def pending_users():
    return list_pending_users()