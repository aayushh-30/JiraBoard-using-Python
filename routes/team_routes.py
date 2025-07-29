from flask import Blueprint
from controllers.team_controllers import create_team, get_teams, add_team_member, get_team, update_team

team_bp = Blueprint('team', __name__)

@team_bp.route('/create', methods=['GET', 'POST'])
def create():
    return create_team()

@team_bp.route('/')
def teams():
    return get_teams()

@team_bp.route('/<uuid:team_id>/add-member', methods=['GET', 'POST'])
def add_member(team_id):
    return add_team_member(team_id)

@team_bp.route('/<uuid:team_id>')
def detail(team_id):
    return get_team(team_id)

@team_bp.route('/<uuid:team_id>/edit', methods=['GET', 'POST'])
def edit(team_id):
    return update_team(team_id)