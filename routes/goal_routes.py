from flask import Blueprint
from controllers.goal_controllers import (
    get_goals, create_goal, get_goal, update_goal, 
    delete_goal, update_goal_progress, get_goal_stats
)

# Create the goal blueprint
goal_bp = Blueprint('goal', __name__, url_prefix='/goals')

# Main goal routes
goal_bp.route('/', methods=['GET', 'POST'])(get_goals)
goal_bp.route('/create', methods=['GET', 'POST'])(create_goal)
goal_bp.route('/<goal_id>', methods=['GET'])(get_goal)
goal_bp.route('/<goal_id>/edit', methods=['GET', 'POST'])(update_goal)
goal_bp.route('/<goal_id>/delete', methods=['POST'])(delete_goal)
goal_bp.route('/<goal_id>/progress', methods=['GET', 'POST'])(update_goal_progress)

# API routes for goal data
goal_bp.route('/stats', methods=['GET'])(get_goal_stats)

# Additional route names for convenience
goal_bp.add_url_rule('/', endpoint='goals', view_func=get_goals, methods=['GET', 'POST'])
goal_bp.add_url_rule('/create', endpoint='create', view_func=create_goal, methods=['GET', 'POST'])
goal_bp.add_url_rule('/<goal_id>', endpoint='detail', view_func=get_goal, methods=['GET'])
goal_bp.add_url_rule('/<goal_id>/edit', endpoint='edit', view_func=update_goal, methods=['GET', 'POST'])
goal_bp.add_url_rule('/<goal_id>/delete', endpoint='delete', view_func=delete_goal, methods=['POST'])
goal_bp.add_url_rule('/<goal_id>/progress', endpoint='progress', view_func=update_goal_progress, methods=['GET', 'POST'])
goal_bp.add_url_rule('/api/stats', endpoint='api_stats', view_func=get_goal_stats, methods=['GET'])
