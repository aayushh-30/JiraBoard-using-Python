from flask import Blueprint
from controllers.search_controllers import search

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search_page():
    return search()
