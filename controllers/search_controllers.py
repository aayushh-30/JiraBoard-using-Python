from flask import render_template, request
from flask_login import login_required

# Mock search data
search_data = {
    'projects': [
        {'id': 1, 'title': 'Project Lehsun', 'description': 'Garlic-powered authentication system', 'type': 'project'},
        {'id': 2, 'title': 'Project Haldi', 'description': 'Golden turmeric dashboard', 'type': 'project'},
        {'id': 3, 'title': 'Project Mirchi', 'description': 'Hot and spicy notification system', 'type': 'project'},
    ],
    'tasks': [
        {'id': 1, 'title': 'Setup Authentication', 'description': 'Implement login system', 'type': 'task'},
        {'id': 2, 'title': 'Design Dashboard', 'description': 'Create user dashboard layout', 'type': 'task'},
        {'id': 3, 'title': 'Notification Service', 'description': 'Build notification delivery system', 'type': 'task'},
    ],
    'users': [
        {'id': 1, 'title': 'Masterchef Admin', 'description': 'System Administrator', 'type': 'user'},
        {'id': 2, 'title': 'Spice Manager', 'description': 'Project Manager', 'type': 'user'},
        {'id': 3, 'title': 'Chili Champion', 'description': 'Lead Developer', 'type': 'user'},
    ]
}

@login_required
def search():
    """Handle search requests"""
    query = request.args.get('q', '').strip()
    filter_type = request.args.get('type', 'all')
    page = int(request.args.get('page', 1))
    
    results = []
    
    if query:
        # Simple search through all data
        for category, items in search_data.items():
            if filter_type == 'all' or filter_type == category:
                for item in items:
                    if (query.lower() in item['title'].lower() or 
                        query.lower() in item['description'].lower()):
                        results.append(item)
    
    # Simple pagination (6 items per page)
    items_per_page = 6
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_results = results[start_idx:end_idx]
    
    total_pages = (len(results) + items_per_page - 1) // items_per_page
    
    return render_template('search_results.html', 
                         results=paginated_results,
                         query=query,
                         filter_type=filter_type,
                         total_results=len(results),
                         current_page=page,
                         total_pages=total_pages)
