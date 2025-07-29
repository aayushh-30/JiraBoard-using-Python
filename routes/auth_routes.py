from flask import Blueprint, render_template
from controllers.auth_controllers import (
    register as register_controller,
    login as login_controller, 
    logout as logout_controller
)

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    return register_controller()

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return login_controller()

@auth_bp.route('/logout')
def logout():
    return logout_controller()