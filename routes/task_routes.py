from flask import Blueprint
from controllers.task_controllers import create_task, update_task, delete_task, update_task_status, get_project_tasks

task_bp = Blueprint('task', __name__)

@task_bp.route('/project/<uuid:project_id>/create', methods=['GET', 'POST'])
def create(project_id):
    return create_task(project_id)

@task_bp.route('/<uuid:task_id>/edit', methods=['GET', 'POST'])
def edit(task_id):
    return update_task(task_id)

@task_bp.route('/<uuid:task_id>/delete', methods=['POST'])
def delete(task_id):
    return delete_task(task_id)

# API Routes for Kanban Board
@task_bp.route('/<uuid:task_id>/status', methods=['PUT'])
def update_status(task_id):
    return update_task_status(task_id)

@task_bp.route('/api/projects/<uuid:project_id>/tasks', methods=['GET'])
def get_tasks(project_id):
    return get_project_tasks(project_id)