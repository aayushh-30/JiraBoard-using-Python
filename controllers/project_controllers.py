from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from models.project_models import Project
from models.manager_project_models import ManagerProject
from models.models_models import db, RoleName
from forms.project_forms import ProjectForm
from datetime import datetime
from permissions import (
    require_permission, 
    require_role, 
    manager_or_admin_required, 
    project_access_required,
    can_user_access_project
)
import uuid

@login_required
@require_permission('project_create')
def create_project():
    """Create new project - Now using decorator-based permissions"""
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            project_id=uuid.uuid4(),
            title=form.title.data,
            description=form.description.data,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(project)
        
        # Only create manager-project relationship if user is manager
        if getattr(current_user, 'role_name', None) == 'manager' and hasattr(current_user, 'manager'):
            manager_project = ManagerProject(
                manager_id=current_user.manager.manager_id,
                project_id=project.project_id
            )
            db.session.add(manager_project)
        
        db.session.commit()
        
        # Calculate initial health score if method exists
        if hasattr(project, 'calculate_health_score'):
            project.calculate_health_score()
        
        flash('Project created successfully!', 'success')
        return redirect(url_for('project.projects'))
    return render_template('project_create.html', form=form)

@login_required
@require_permission('project_list')
def list_projects():
    """List projects with role-based filtering - Now using decorator-based permissions"""
    user_role = getattr(current_user, 'role_name', None)
    print(f"🔍 DEBUG: User role: {user_role}")
    
    if user_role == 'admin':
        # Admin can see all projects
        projects = Project.query.all()
        print(f"🔍 DEBUG: Admin - Found {len(projects)} projects")
    elif user_role == 'manager' and hasattr(current_user, 'manager'):
        # Manager can see only assigned projects
        try:
            from models.manager_project_models import ManagerProject
            projects = Project.query.join(ManagerProject).filter(
                ManagerProject.manager_id == current_user.manager.manager_id
            ).all()
            print(f"🔍 DEBUG: Manager - Found {len(projects)} projects")
        except Exception as e:
            print(f"🔍 DEBUG: Manager query failed: {e}")
            # Fallback: show no projects for managers to maintain role-based access
            projects = []
            print(f"🔍 DEBUG: Manager fallback - Showing 0 projects for security")
    elif user_role == 'developer' and hasattr(current_user, 'developer'):
        # Developer can see only assigned projects
        try:
            from models.developer_project_models import DeveloperProject
            projects = Project.query.join(DeveloperProject).filter(
                DeveloperProject.developer_id == current_user.developer.developer_id
            ).all()
            print(f"🔍 DEBUG: Developer - Found {len(projects)} projects")
        except Exception as e:
            print(f"🔍 DEBUG: Developer query failed: {e}")
            # Fallback: show no projects for developers to maintain role-based access
            projects = []
            print(f"🔍 DEBUG: Developer fallback - Showing 0 projects for security")
    else:
        # Clients and other roles see no projects by default
        projects = []
        print(f"🔍 DEBUG: Other role - Showing 0 projects for security")
    
    # Debug: Print project details
    for project in projects:
        print(f"🔍 DEBUG: Project {project.project_id} - {project.title}")
    
    return render_template('project_list.html', projects=projects)

@login_required
@require_permission('project_view')
def get_project(project_id):
    """Get project details with role-based data - Now using decorator-based permissions"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this specific project
    if not can_user_access_project(current_user, project_id):
        flash('Access denied. You do not have access to this project.', 'danger')
        return redirect(url_for('project.projects'))
    
    # Calculate and update health score if method exists
    health_score = None
    if hasattr(project, 'calculate_health_score'):
        health_score = project.calculate_health_score()
    
    # Get project data based on user role
    user_role = getattr(current_user, 'role_name', None)
    context = {
        'project': project,
        'health_score': health_score
    }
    
    if user_role in ['admin', 'manager']:
        # Full access to all project data
        tasks = getattr(project, 'tasks', [])
        context.update({
            'tasks': tasks,
            'subprojects': getattr(project, 'subprojects', []),
            'sprints': getattr(project, 'sprints', []),
            'boards': getattr(project, 'boards', []),
            'epics': getattr(project, 'epics', []),
            'team_stats': True
        })
    elif user_role == 'developer':
        # Developer sees limited project info
        tasks = getattr(project, 'tasks', [])
        context.update({
            'tasks': tasks,
            'subprojects': getattr(project, 'subprojects', []),
            'sprints': getattr(project, 'sprints', [])
        })
    else:
        # Client/Viewer sees limited public data
        tasks = []
        context.update({
            'tasks': tasks,
            'public_boards': []
        })
    
    # Organize tasks by status for Kanban board
    todo_tasks = [task for task in tasks if getattr(task, 'status', None) in ['to_do', 'pending', None]]
    in_progress_tasks = [task for task in tasks if getattr(task, 'status', None) == 'in_progress']
    review_tasks = [task for task in tasks if getattr(task, 'status', None) in ['review', 'testing']]
    completed_tasks = [task for task in tasks if getattr(task, 'status', None) in ['done', 'completed']]
    
    context.update({
        'todo_tasks': todo_tasks,
        'in_progress_tasks': in_progress_tasks,
        'review_tasks': review_tasks,
        'completed_tasks': completed_tasks
    })
    
    return render_template('project_detail.html', **context)

@login_required
@require_permission('project_edit')
def update_project(project_id):
    """Update project - Now using decorator-based permissions"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this specific project
    if not can_user_access_project(current_user, project_id):
        flash('Access denied. You do not have access to this project.', 'danger')
        return redirect(url_for('project.projects'))
    
    form = ProjectForm(obj=project)
    
    if form.validate_on_submit():
        project.title = form.title.data
        project.description = form.description.data
        project.updated_at = datetime.utcnow()
        
        # Update health score if method exists
        if hasattr(project, 'calculate_health_score'):
            project.calculate_health_score()
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project.detail', project_id=project_id))
    
    return render_template('project_edit.html', form=form, project=project)

@login_required
@require_permission('project_delete')
def delete_project(project_id):
    """Delete project - Now using decorator-based permissions"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this specific project
    if not can_user_access_project(current_user, project_id):
        flash('Access denied. You do not have access to this project.', 'danger')
        return redirect(url_for('project.projects'))
    
    # Create backup before deletion if system supports it
    try:
        from models.system_models import Backup
        backup = Backup(
            project_id=project_id,
            created_by_id=current_user.user_id,
            backup_type='pre_delete',
            status='completed'
        )
        db.session.add(backup)
    except ImportError:
        # System backup model not available
        pass
    
    db.session.delete(project)
    db.session.commit()
    
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('project.projects'))