from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.goal_models import Goal, GoalStatus, GoalPriority, GoalCategory
from models.project_models import Project
from models.user_models import User
from models.manager_project_models import ManagerProject
from models.models_models import db
from forms.goal_forms import GoalForm, GoalFilterForm, GoalProgressForm
from datetime import datetime
from permissions import require_permission, require_role
import uuid

@login_required
@require_permission('goal_view')
def get_goals():
    """Display goals with filtering options"""
    try:
        filter_form = GoalFilterForm()
        
        # Populate project choices for filter
        projects = Project.query.all()
        filter_form.project_id.choices = [('', 'All Projects')] + [(str(p.project_id), p.title) for p in projects]
    except Exception as e:
        flash(f'Error loading projects: {str(e)}', 'warning')
        filter_form = GoalFilterForm()
        filter_form.project_id.choices = [('', 'All Projects')]
    
    # Build query based on user role and filters
    try:
        query = Goal.query
        user_role = getattr(current_user, 'role_name', None)
        
        # Role-based filtering
        if user_role == 'admin':
            # Admin can see all goals
            pass
        elif user_role == 'manager':
            # Manager can see team goals and project goals they manage
            if hasattr(current_user, 'manager'):
                managed_projects = Project.query.join(ManagerProject).filter(
                    ManagerProject.manager_id == current_user.manager.manager_id
                ).all()
                managed_project_ids = [p.project_id for p in managed_projects]
                
                query = query.filter(
                    (Goal.user_id == current_user.user_id) |
                    (Goal.project_id.in_(managed_project_ids)) |
                    (Goal.category.in_([GoalCategory.TEAM, GoalCategory.ORGANIZATIONAL]))
                )
            else:
                query = query.filter(Goal.user_id == current_user.user_id)
        else:
            # Developer, client, viewer see only their own goals
            query = query.filter(Goal.user_id == current_user.user_id)
        
        # Apply filters if form submitted
        if filter_form.filter.data and filter_form.validate():
            if filter_form.status.data:
                query = query.filter(Goal.status == filter_form.status.data)
            if filter_form.priority.data:
                query = query.filter(Goal.priority == filter_form.priority.data)
            if filter_form.category.data:
                query = query.filter(Goal.category == filter_form.category.data)
            if filter_form.project_id.data:
                query = query.filter(Goal.project_id == filter_form.project_id.data)
        
        # Order by priority, status, and target date
        goals = query.order_by(
            Goal.priority.desc(),
            Goal.status,
            Goal.target_date.asc()
        ).all()
        
        # Calculate statistics
        stats = {
            'total': len(goals),
            'completed': len([g for g in goals if g.status == GoalStatus.COMPLETED]),
            'in_progress': len([g for g in goals if g.status == GoalStatus.IN_PROGRESS]),
            'overdue': len([g for g in goals if g.is_overdue()]),
            'milestones': len([g for g in goals if g.is_milestone])
        }
        
    except Exception as e:
        # If goal table doesn't exist or other database errors
        flash(f'Database error: {str(e)}. Goal table may not exist.', 'danger')
        goals = []
        stats = {
            'total': 0,
            'completed': 0,
            'in_progress': 0,
            'overdue': 0,
            'milestones': 0
        }
    
    return render_template('goal_list.html', goals=goals, filter_form=filter_form, stats=stats)

@login_required
@require_permission('goal_create')
def create_goal():
    """Create a new goal"""
    form = GoalForm()
    
    # Populate project choices
    projects = Project.query.all()
    form.project_id.choices = [('', 'No Project')] + [(str(p.project_id), p.title) for p in projects]
    
    if form.validate_on_submit():
        try:
            goal = Goal(
                goal_id=uuid.uuid4(),
                title=form.title.data,
                description=form.description.data,
                project_id=form.project_id.data if form.project_id.data else None,
                user_id=current_user.user_id,
                priority=GoalPriority(form.priority.data),
                status=GoalStatus(form.status.data),
                target_date=form.target_date.data,
                progress_percentage=form.progress_percentage.data,
                category=GoalCategory(form.category.data),
                is_milestone=form.is_milestone.data,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            
            db.session.add(goal)
            db.session.commit()
            
            flash('Goal created successfully!', 'success')
            return redirect(url_for('goal.goals'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating goal: {str(e)}', 'danger')
    else:
        # Show form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'danger')
    
    return render_template('goal_create.html', form=form)

@login_required
@require_permission('goal_view')
def get_goal(goal_id):
    """View goal details"""
    goal = Goal.query.get_or_404(goal_id)
    
    # Check if user can view this goal
    if not can_user_access_goal(current_user, goal):
        flash('Access denied. You do not have access to this goal.', 'danger')
        return redirect(url_for('goal.goals'))
    
    # Get related project info if exists
    project = goal.project if goal.project_id else None
    
    return render_template('goal_detail.html', goal=goal, project=project)

@login_required
@require_permission('goal_edit')
def update_goal(goal_id):
    """Update a goal"""
    goal = Goal.query.get_or_404(goal_id)
    
    # Check if user can edit this goal
    if not can_user_edit_goal(current_user, goal):
        flash('Access denied. You cannot edit this goal.', 'danger')
        return redirect(url_for('goal.goals'))
    
    form = GoalForm(obj=goal)
    
    # Populate project choices
    projects = Project.query.all()
    form.project_id.choices = [('', 'No Project')] + [(str(p.project_id), p.title) for p in projects]
    
    # Set current values
    if goal.project_id:
        form.project_id.data = str(goal.project_id)
    if goal.priority:
        form.priority.data = goal.priority.value
    if goal.status:
        form.status.data = goal.status.value
    if goal.category:
        form.category.data = goal.category.value
    
    if form.validate_on_submit():
        goal.title = form.title.data
        goal.description = form.description.data
        goal.project_id = form.project_id.data if form.project_id.data else None
        goal.priority = GoalPriority(form.priority.data)
        goal.status = GoalStatus(form.status.data)
        goal.target_date = form.target_date.data
        goal.progress_percentage = form.progress_percentage.data
        goal.category = GoalCategory(form.category.data)
        goal.is_milestone = form.is_milestone.data
        goal.updated_at = datetime.utcnow()
        
        # Update completion date if status changed to completed
        if goal.status == GoalStatus.COMPLETED and not goal.completion_date:
            goal.completion_date = datetime.utcnow()
        elif goal.status != GoalStatus.COMPLETED:
            goal.completion_date = None
        
        db.session.commit()
        
        flash('Goal updated successfully!', 'success')
        return redirect(url_for('goal.detail', goal_id=goal_id))
    
    return render_template('goal_edit.html', form=form, goal=goal)

@login_required
@require_permission('goal_delete')
def delete_goal(goal_id):
    """Delete a goal"""
    goal = Goal.query.get_or_404(goal_id)
    
    # Check if user can delete this goal
    if not can_user_edit_goal(current_user, goal):
        flash('Access denied. You cannot delete this goal.', 'danger')
        return redirect(url_for('goal.goals'))
    
    db.session.delete(goal)
    db.session.commit()
    
    flash('Goal deleted successfully!', 'success')
    return redirect(url_for('goal.goals'))

@login_required
@require_permission('goal_edit')
def update_goal_progress(goal_id):
    """Update goal progress"""
    goal = Goal.query.get_or_404(goal_id)
    
    # Check if user can edit this goal
    if not can_user_edit_goal(current_user, goal):
        flash('Access denied. You cannot update this goal.', 'danger')
        return redirect(url_for('goal.goals'))
    
    form = GoalProgressForm()
    
    if form.validate_on_submit():
        goal.progress_percentage = form.progress_percentage.data
        goal.status = GoalStatus(form.status.data)
        goal.updated_at = datetime.utcnow()
        
        # Update completion date if status changed to completed
        if goal.status == GoalStatus.COMPLETED and not goal.completion_date:
            goal.completion_date = datetime.utcnow()
        elif goal.status != GoalStatus.COMPLETED:
            goal.completion_date = None
        
        db.session.commit()
        
        flash('Goal progress updated successfully!', 'success')
        return redirect(url_for('goal.detail', goal_id=goal_id))
    
    # Pre-populate form with current values
    form.progress_percentage.data = goal.progress_percentage
    form.status.data = goal.status.value if goal.status else GoalStatus.PENDING.value
    
    return render_template('goal_progress.html', form=form, goal=goal)

@login_required
def get_goal_stats():
    """Get goal statistics for dashboard"""
    user_role = getattr(current_user, 'role_name', None)
    
    # Build query based on user role
    query = Goal.query
    if user_role != 'admin':
        if user_role == 'manager' and hasattr(current_user, 'manager'):
            # Manager can see team goals and project goals they manage
            managed_projects = Project.query.join(ManagerProject).filter(
                ManagerProject.manager_id == current_user.manager.manager_id
            ).all()
            managed_project_ids = [p.project_id for p in managed_projects]
            
            query = query.filter(
                (Goal.user_id == current_user.user_id) |
                (Goal.project_id.in_(managed_project_ids)) |
                (Goal.category.in_([GoalCategory.TEAM, GoalCategory.ORGANIZATIONAL]))
            )
        else:
            query = query.filter(Goal.user_id == current_user.user_id)
    
    goals = query.all()
    
    stats = {
        'total_goals': len(goals),
        'completed_goals': len([g for g in goals if g.status == GoalStatus.COMPLETED]),
        'in_progress_goals': len([g for g in goals if g.status == GoalStatus.IN_PROGRESS]),
        'overdue_goals': len([g for g in goals if g.is_overdue()]),
        'milestones': len([g for g in goals if g.is_milestone]),
        'avg_progress': sum(g.progress_percentage for g in goals) / len(goals) if goals else 0
    }
    
    return jsonify(stats)

# Helper functions
def can_user_access_goal(user, goal):
    """Check if user can access a goal"""
    user_role = getattr(user, 'role_name', None)
    
    if user_role == 'admin':
        return True
    if goal.user_id == user.user_id:
        return True
    if user_role == 'manager' and hasattr(user, 'manager'):
        # Manager can access team/organizational goals and project goals they manage
        if goal.category in [GoalCategory.TEAM, GoalCategory.ORGANIZATIONAL]:
            return True
        if goal.project_id:
            managed_project = ManagerProject.query.filter_by(
                manager_id=user.manager.manager_id,
                project_id=goal.project_id
            ).first()
            return managed_project is not None
    
    return False

def can_user_edit_goal(user, goal):
    """Check if user can edit a goal"""
    user_role = getattr(user, 'role_name', None)
    
    if user_role == 'admin':
        return True
    if goal.user_id == user.user_id:
        return True
    if user_role == 'manager' and hasattr(user, 'manager'):
        # Manager can edit team goals and project goals they manage
        if goal.category == GoalCategory.TEAM:
            return True
        if goal.project_id:
            managed_project = ManagerProject.query.filter_by(
                manager_id=user.manager.manager_id,
                project_id=goal.project_id
            ).first()
            return managed_project is not None
    
    return False
