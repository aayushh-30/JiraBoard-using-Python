from flask import Blueprint
from controllers.report_controllers import create_report, get_reports

report_bp = Blueprint('report', __name__)

@report_bp.route('/project/<uuid:project_id>/create', methods=['GET', 'POST'])
def create(project_id):
    return create_report(project_id)

@report_bp.route('/')
def reports():
    return get_reports()