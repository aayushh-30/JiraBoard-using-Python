from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.task_models import Task
from models.project_models import Project
from models.manager_project_models import ManagerProject
from models.models_models import db, RoleName
from forms.task_forms import TaskForm
from datetime import datetime
import uuid

@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=project_id).first():
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            task_id=uuid.uuid4(),
            title=form.title.data,
            description=form.description.data,
            status=form.status.data,
            type=form.type.data,
            project_id=project_id,
            subproject_id=form.subproject_id.data or None,
            sprint_id=form.sprint_id.data or None,
            assigned_to_id=form.assigned_to.data or None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.session.add(task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=project_id))
    return render_template('create_task.html', form=form, project=project)

@login_required
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    if current_user.role.role_name not in [RoleName.manager, RoleName.developer] or (current_user.role.role_name == RoleName.manager and not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=project.project_id).first()) or (current_user.role.role_name == RoleName.developer and task.assigned_to_id != current_user.user_id):
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    form = TaskForm(obj=task)
    if form.validate_on_submit():
        task.title = form.title.data
        task.description = form.description.data
        task.status = form.status.data
        task.type = form.type.data
        task.subproject_id = form.subproject_id.data or None
        task.sprint_id = form.sprint_id.data or None
        task.assigned_to_id = form.assigned_to.data or None
        task.updated_at = datetime.utcnow()
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('project.get_project', project_id=task.project_id))
    return render_template('edit_task.html', form=form, task=task)

@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    project = task.project
    if current_user.role.role_name != RoleName.manager or not ManagerProject.query.filter_by(manager_id=current_user.manager.manager_id, project_id=project.project_id).first():
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('dashboard.dashboard_page'))
    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('project.get_project', project_id=project.project_id))

# API Endpoints for Kanban Board
@login_required
def update_task_status(task_id):
    """API endpoint to update task status for drag-and-drop functionality"""
    if request.method != 'PUT':
        return jsonify({'error': 'Method not allowed'}), 405
    
    task = Task.query.get_or_404(task_id)
    
    # Check permissions
    user_role = getattr(current_user, 'role_name', None)
    if user_role not in ['admin', 'manager', 'developer']:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # For developers, check if they're assigned to the task
    if user_role == 'developer' and task.assigned_to_id != current_user.user_id:
        return jsonify({'error': 'You can only update tasks assigned to you'}), 403
    
    # For managers, check if they manage the project
    if user_role == 'manager':
        manager_project = ManagerProject.query.filter_by(
            manager_id=current_user.manager.manager_id, 
            project_id=task.project_id
        ).first()
        if not manager_project:
            return jsonify({'error': 'You do not manage this project'}), 403
    
    data = request.get_json()
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400
    
    # Valid statuses
    valid_statuses = ['to_do', 'in_progress', 'review', 'done']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    try:
        task.status = new_status
        task.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Task status updated to {new_status}',
            'task_id': task_id,
            'new_status': new_status
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Failed to update task status'}), 500

@login_required
def get_project_tasks(project_id):
    """API endpoint to get all tasks for a project"""
    project = Project.query.get_or_404(project_id)
    
    # Check if user has access to this project
    from permissions import can_user_access_project
    if not can_user_access_project(current_user, project_id):
        return jsonify({'error': 'Access denied'}), 403
    
    try:
        tasks = getattr(project, 'tasks', [])
        tasks_data = []
        
        for task in tasks:
            task_data = {
                'task_id': str(task.task_id),
                'title': task.title,
                'description': task.description,
                'status': getattr(task, 'status', 'to_do'),
                'priority': getattr(task, 'priority', 'medium'),
                'type': getattr(task, 'type', 'task'),
                'assigned_to': task.assigned_to.full_name if task.assigned_to else None,
                'created_at': task.created_at.isoformat() if task.created_at else None,
                'updated_at': task.updated_at.isoformat() if task.updated_at else None
            }
            tasks_data.append(task_data)
        
        return jsonify(tasks_data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch tasks'}), 500