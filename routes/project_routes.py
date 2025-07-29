from flask import Blueprint
from controllers.project_controllers import (
    create_project, 
    list_projects, 
    get_project, 
    update_project, 
    delete_project
)
from controllers.simple_project_controllers import (
    goals,
    create_goal
)

project_bp = Blueprint('project', __name__)

@project_bp.route('/')
@project_bp.route('/projects')
def projects():
    return list_projects()

@project_bp.route('/create', methods=['GET', 'POST'])
def create():
    return create_project()

@project_bp.route('/<uuid:project_id>')
def detail(project_id):
    return get_project(project_id)

@project_bp.route('/<uuid:project_id>/edit', methods=['GET', 'POST'])
def edit(project_id):
    return update_project(project_id)

@project_bp.route('/<uuid:project_id>/delete', methods=['POST'])
def delete(project_id):
    return delete_project(project_id)

# Goals routes
@project_bp.route('/goals')
def goals_page():
    return goals()

@project_bp.route('/goals/create', methods=['GET', 'POST'])
def create_goal_page():
    return create_goal()