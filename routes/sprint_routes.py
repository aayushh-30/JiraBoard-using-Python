from flask import Blueprint
from controllers.sprint_controllers import create_sprint, get_sprint

sprint_bp = Blueprint('sprint', __name__)

@sprint_bp.route('/project/<uuid:project_id>/create', methods=['GET', 'POST'])
def create(project_id):
    return create_sprint(project_id)

@sprint_bp.route('/<uuid:sprint_id>')
def detail(sprint_id):
    return get_sprint(sprint_id)