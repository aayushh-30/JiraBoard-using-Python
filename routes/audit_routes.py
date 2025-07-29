from flask import Blueprint
from controllers.audit_controllers import get_audit_logs

audit_bp = Blueprint('audit', __name__)

@audit_bp.route('/')
def logs():
    return get_audit_logs()