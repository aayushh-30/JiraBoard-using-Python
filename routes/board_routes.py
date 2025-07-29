from flask import Blueprint
from controllers.board_controllers import create_board, get_board

board_bp = Blueprint('board', __name__)

@board_bp.route('/project/<uuid:project_id>/create', methods=['GET', 'POST'])
def create(project_id):
    return create_board(project_id)

@board_bp.route('/<uuid:board_id>')
def detail(board_id):
    return get_board(board_id)