from flask import Blueprint
from controllers.user_controllers import update_profile, get_users, approve_user, delete_user, get_user, update_user, create_user

user_bp = Blueprint('user', __name__)

@user_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    return update_profile()

@user_bp.route('/')
def users():
    return get_users()

@user_bp.route('/create', methods=['GET', 'POST'])
def create():
    return create_user()

@user_bp.route('/<uuid:user_id>')
def detail(user_id):
    return get_user(user_id)

@user_bp.route('/<uuid:user_id>/edit', methods=['GET', 'POST'])
def edit(user_id):
    return update_user(user_id)

@user_bp.route('/approve', methods=['POST'])
def approve():
    return approve_user()

@user_bp.route('/delete', methods=['POST'])
def delete():
    return delete_user()