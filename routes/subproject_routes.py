from flask import Blueprint
from controllers.subproject_controllers import create_subproject, get_subproject

subproject_bp = Blueprint('subproject', __name__)

@subproject_bp.route('/project/<uuid:project_id>/create', methods=['GET', 'POST'])
def create(project_id):
    return create_subproject(project_id)

@subproject_bp.route('/<uuid:subproject_id>')
def detail(subproject_id):
    return get_subproject(subproject_id)