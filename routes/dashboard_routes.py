from flask import Blueprint, render_template
from controllers.dashboard_controllers import dashboard

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def landing():
    """Landing page - no login required"""
    return render_template('landing.html')

@dashboard_bp.route('/dashboard')
def dashboard_page():
    """Dashboard page - login required"""
    return dashboard()