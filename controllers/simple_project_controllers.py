from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

# Simple mock project data for testing
mock_projects = [
    {
        'id': 1,
        'title': 'Project Lehsun',
        'description': 'Garlic-powered authentication system - adding that extra punch to security! 🧄',
        'status': 'In Progress',
        'created_at': '2025-01-01',
        'manager': 'Masterchef Admin'
    },
    {
        'id': 2,
        'title': 'Project Haldi',
        'description': 'Golden turmeric dashboard - healing your data visualization woes with natural beauty ✨',
        'status': 'Planning',
        'created_at': '2025-01-02',
        'manager': 'Spice Manager'
    },
    {
        'id': 3,
        'title': 'Project Mirchi',
        'description': 'Hot and spicy notification system - guaranteed to wake up your users! 🌶️',
        'status': 'Completed',
        'created_at': '2024-12-15',
        'manager': 'Chili Champion'
    },
    {
        'id': 4,
        'title': 'Project Adrak',
        'description': 'Ginger-fresh API development - giving your backend that zesty kick it needs! 🫚',
        'status': 'In Progress',
        'created_at': '2025-01-03',
        'manager': 'Ginger Guru'
    },
    {
        'id': 5,
        'title': 'Project Laung',
        'description': 'Clove-scented search engine - aromatic and powerful indexing for your content 🌸',
        'status': 'Testing',
        'created_at': '2025-01-04',
        'manager': 'Clove Captain'
    },
    {
        'id': 6,
        'title': 'Project Elaichi',
        'description': 'Cardamom-infused user experience - sweet, sophisticated, and absolutely delightful 💎',
        'status': 'Planning',
        'created_at': '2025-01-05',
        'manager': 'Cardamom Craftsman'
    }
]

# Mock goals data
mock_goals = [
    {
        'id': 1,
        'title': 'Q1 Spice Garden Expansion',
        'description': 'Grow our project portfolio with 5 new spice-themed modules by March',
        'target_date': '2025-03-31',
        'progress': 60,
        'status': 'In Progress',
        'category': 'Development'
    },
    {
        'id': 2,
        'title': 'Team Masala Certification',
        'description': 'Get entire development team certified in Dhaniya best practices',
        'target_date': '2025-02-28',
        'progress': 25,
        'status': 'Planning',
        'category': 'Training'
    },
    {
        'id': 3,
        'title': 'Organic Code Quality',
        'description': 'Achieve 95% test coverage across all spice projects',
        'target_date': '2025-06-30',
        'progress': 80,
        'status': 'On Track',
        'category': 'Quality'
    },
    {
        'id': 4,
        'title': 'Fresh Harvest Release',
        'description': 'Launch Dhaniya v2.0 with enhanced aromatics and performance',
        'target_date': '2025-04-15',
        'progress': 45,
        'status': 'In Progress',
        'category': 'Product'
    }
]

@login_required
def get_projects():
    """List all projects - simplified for testing"""
    return render_template('list_project.html', projects=mock_projects)

@login_required  
def get_project(project_id):
    """Get single project - simplified for testing"""
    project = next((p for p in mock_projects if p['id'] == int(project_id)), None)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('project.projects'))
    return render_template('detail_project.html', project=project)

@login_required
def create_project():
    """Create new project - simplified for testing"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        
        if title and description:
            # Create mock project
            new_project = {
                'id': len(mock_projects) + 1,
                'title': title,
                'description': description,
                'status': 'Planning',
                'created_at': '2025-01-15',
                'manager': current_user.username if hasattr(current_user, 'username') else 'Current User'
            }
            mock_projects.append(new_project)
            flash('Project created successfully!', 'success')
            return redirect(url_for('project.projects'))
        else:
            flash('Please fill in all fields', 'error')
    
    return render_template('create_project.html')

@login_required
def update_project(project_id):
    """Update project - simplified for testing"""
    project = next((p for p in mock_projects if p['id'] == int(project_id)), None)
    if not project:
        flash('Project not found', 'error')
        return redirect(url_for('project.projects'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        status = request.form.get('status')
        
        if title:
            project['title'] = title
        if description:
            project['description'] = description
        if status:
            project['status'] = status
            
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project.projects'))
    
    return render_template('edit_project.html', project=project)

@login_required
def delete_project(project_id):
    """Delete project - simplified for testing"""
    global mock_projects
    project = next((p for p in mock_projects if p['id'] == int(project_id)), None)
    if project:
        mock_projects = [p for p in mock_projects if p['id'] != int(project_id)]
        flash('Project deleted successfully!', 'success')
    else:
        flash('Project not found', 'error')
    
    return redirect(url_for('project.projects'))

@login_required
def goals():
    """Display goals dashboard"""
    return render_template('goal_list.html', goals=mock_goals)

@login_required
def create_goal():
    """Create a new goal"""
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        target_date = request.form.get('target_date')
        category = request.form.get('category')
        
        if title and description:
            new_goal = {
                'id': len(mock_goals) + 1,
                'title': title,
                'description': description,
                'target_date': target_date,
                'progress': 0,
                'status': 'Planning',
                'category': category or 'General'
            }
            mock_goals.append(new_goal)
            flash('Goal planted successfully! 🌱', 'success')
            return redirect(url_for('project.goals_page'))
        else:
            flash('Please fill in all required fields', 'error')
    
    return render_template('create_goal.html')
