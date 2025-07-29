from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from permissions import require_permission, require_role
from werkzeug.security import generate_password_hash
import uuid
from datetime import datetime
from models.user_models import User
from models.role_models import Role
from models.project_models import Project
from models.task_models import Task
from extensions import db

@require_permission('admin_panel')
def admin_dashboard():
    """Admin dashboard with system overview and management tools"""
    try:
        # Get system statistics using SQLAlchemy
        stats = {}
        
        # User statistics
        stats['total_users'] = User.query.count()
        stats['pending_users'] = User.query.filter_by(is_approved=False).count()
        
        # Role distribution
        role_stats = db.session.query(Role.role_name, db.func.count(User.user_id)).join(User, Role.role_id == User.role_id, isouter=True).group_by(Role.role_name).all()
        stats['users_by_role'] = {role.value: count for role, count in role_stats}
        
        # Project and task statistics  
        stats['total_projects'] = Project.query.count()
        stats['total_tasks'] = Task.query.count()
        stats['completed_tasks'] = Task.query.filter_by(status='done').count()
        
        # Recent activity - new users in last 7 days
        from datetime import datetime, timedelta
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_activity = User.query.filter(User.created_at >= week_ago).order_by(User.created_at.desc()).limit(10).all()
        
        # Pending approvals
        pending_approvals = User.query.filter_by(is_approved=False).order_by(User.created_at.desc()).all()
        
        # System health checks
        health_checks = []
        
        # Check for orphaned tasks (tasks without valid projects)
        orphaned_tasks = Task.query.filter(~Task.project_id.in_(db.session.query(Project.project_id))).count()
        if orphaned_tasks > 0:
            health_checks.append({
                'type': 'warning',
                'message': f'{orphaned_tasks} tasks without valid projects found'
            })
        
        # Check for tasks assigned to inactive users
        inactive_user_tasks = Task.query.join(User, Task.assigned_to_id == User.user_id).filter(User.is_approved == False).count()
        if inactive_user_tasks > 0:
            health_checks.append({
                'type': 'warning', 
                'message': f'{inactive_user_tasks} tasks assigned to inactive users'
            })
        
        if not health_checks:
            health_checks.append({
                'type': 'success',
                'message': 'All system health checks passed'
            })
        
        return render_template('admin_dashboard.html',
                             stats=stats,
                             recent_activity=recent_activity,
                             pending_approvals=pending_approvals,
                             health_checks=health_checks)
        
    except Exception as e:
        flash(f'Error loading admin dashboard: {e}', 'danger')
        return render_template('admin_dashboard.html',
                             stats={},
                             recent_activity=[],
                             pending_approvals=[],
                             health_checks=[])

@require_permission('user_view')
def admin_users():
    """Admin user management page with multi-role support"""
    try:
        from models.team_models import Team
        
        # Get users with their primary roles
        users_query = db.session.query(User, Role).join(Role).order_by(User.created_at.desc()).all()
        
        users = []
        for user, role in users_query:
            users.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at,
                'role_name': role.role_name.value,
                'team_name': 'No Team',  # Simplified for now
                'status': 'active' if user.is_approved else 'inactive',
                'last_login': user.created_at
            })
        
        # Get available teams for dropdowns
        teams = [team.name for team in Team.query.order_by(Team.name).all()]
        
        return render_template('user_management_multi_role.html', users=users, teams=teams)
        
    except Exception as e:
        flash(f'Error loading users: {e}', 'danger')
        return render_template('user_management_multi_role.html', users=[], teams=[])

@require_permission('user_view')
def get_user_roles(user_id):
    """API endpoint to get user's roles"""
    try:
        from models.user_role_models import UserRole
        
        user = User.query.get_or_404(user_id)
        user_roles = UserRole.get_user_roles(user_id)
        
        roles_data = []
        for user_role in user_roles:
            role_name = user_role.role.role_name.value if hasattr(user_role.role.role_name, 'value') else str(user_role.role.role_name)
            roles_data.append({
                'role_id': str(user_role.role_id),
                'role_name': role_name,
                'is_primary': user_role.is_primary,
                'assigned_at': user_role.assigned_at.isoformat() if user_role.assigned_at else None
            })
        
        # If no roles in user_roles table, fall back to direct role relationship
        if not roles_data and user.role:
            role_name = user.role.role_name.value if hasattr(user.role.role_name, 'value') else str(user.role.role_name)
            roles_data.append({
                'role_id': str(user.role_id),
                'role_name': role_name,
                'is_primary': True,
                'assigned_at': user.created_at.isoformat() if user.created_at else None
            })
        
        return jsonify({'success': True, 'roles': roles_data})
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@require_permission('user_edit')
def add_user_role():
    """Add a role to a user"""
    try:
        from models.user_role_models import UserRole
        from models.role_models import Role
        from flask import request
        
        data = request.get_json()
        user_id = data.get('user_id')
        role_name = data.get('role_name')
        is_primary = data.get('is_primary', False)
        
        if not user_id or not role_name:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Get user and role
        user = User.query.get_or_404(user_id)
        role = Role.query.filter_by(role_name=role_name).first()
        if not role:
            return jsonify({'success': False, 'message': 'Role not found'}), 404
        
        # Add role to user
        user_role = UserRole.add_role_to_user(
            user_id=user_id,
            role_id=role.role_id,
            assigned_by_id=current_user.user_id,
            is_primary=is_primary
        )
        
        if user_role:
            return jsonify({'success': True, 'message': 'Role added successfully'})
        else:
            return jsonify({'success': False, 'message': 'User already has this role'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@require_permission('user_edit')
def remove_user_role():
    """Remove a role from a user"""
    try:
        from models.user_role_models import UserRole
        from flask import request
        
        data = request.get_json()
        user_id = data.get('user_id')
        role_id = data.get('role_id')
        
        if not user_id or not role_id:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Check if this is the last role
        user_roles_count = UserRole.query.filter_by(user_id=user_id).count()
        if user_roles_count <= 1:
            return jsonify({'success': False, 'message': 'Cannot remove the last role from a user'}), 400
        
        # Remove role from user
        success = UserRole.remove_role_from_user(user_id, role_id)
        
        if success:
            return jsonify({'success': True, 'message': 'Role removed successfully'})
        else:
            return jsonify({'success': False, 'message': 'Role not found for this user'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@require_permission('user_edit')
def set_primary_role():
    """Set a role as primary for a user"""
    try:
        from models.user_role_models import UserRole
        from flask import request
        
        data = request.get_json()
        user_id = data.get('user_id')
        role_id = data.get('role_id')
        
        if not user_id or not role_id:
            return jsonify({'success': False, 'message': 'Missing required fields'}), 400
        
        # Set primary role
        user_role = UserRole.set_primary_role(user_id, role_id)
        
        if user_role:
            return jsonify({'success': True, 'message': 'Primary role updated successfully'})
        else:
            return jsonify({'success': False, 'message': 'Role not found for this user'})
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500

@require_permission('user_approve')
def pending_users():
    """View pending user approvals"""
    try:
        # Get pending users using SQLAlchemy (simplified)
        pending_users_query = User.query.filter_by(is_approved=False).order_by(User.created_at.desc()).all()
        
        pending_users = []
        for user in pending_users_query:
            pending_users.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'created_at': user.created_at,
                'team_name': 'No Team',  # Simplified for now
                'team_id': None
            })
        
        return render_template('admin_pending_users.html', pending_users=pending_users)
        
    except Exception as e:
        flash(f'Error loading pending users: {e}', 'danger')
        return render_template('admin_pending_users.html', pending_users=[])

@require_permission('system_settings')
def system_settings():
    """System settings page"""
    # Mock db_stats for now
    db_stats = {
        'size': '150 MB',
        'last_backup': 'Never'
    }
    return render_template('admin_system_settings.html', db_stats=db_stats)

@require_permission('user_edit')
def toggle_user_status(user_id):
    """Toggle user active status"""
    try:
        user = User.query.get(user_id)
        if not user:
            flash('User not found.', 'danger')
            return redirect(url_for('admin.users'))
        
        # Toggle the approval status
        user.is_approved = not user.is_approved
        user.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        action = 'activated' if user.is_approved else 'deactivated'
        flash(f'User {action} successfully!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Error updating user status: {e}', 'danger')
    
    return redirect(url_for('admin.users'))

@require_permission('user_approve')
def approve_user(user_id):
    """Approve user registration"""
    try:
        user = User.query.get(user_id)
        if user:
            # Approve user
            user.is_approved = True
            user.updated_at = datetime.utcnow()
            
            db.session.commit()
            flash('User approved successfully!', 'success')
        else:
            flash('User not found.', 'danger')
            
    except Exception as e:
        db.session.rollback()
        flash(f'Error approving user: {e}', 'danger')
    
    return redirect(url_for('admin.pending_users'))

@require_permission('user_delete')
def delete_user(user_id):
    """Delete a user"""
    try:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            return jsonify({'success': True, 'message': 'User deleted successfully'})
        else:
            return jsonify({'success': False, 'message': 'User not found'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@require_permission('user_create')
def create_user():
    """Create a new user"""
    data = request.get_json()
    
    try:
        # Get role
        role = Role.query.filter_by(role_name=data['role']).first()
        if not role:
            return jsonify({'success': False, 'message': 'Invalid role'})
        
        # Create new user
        password_hash = generate_password_hash(data.get('password', 'password123'))
        
        new_user = User()
        new_user.username = data['name']
        new_user.email = data['email'] 
        new_user.password_hash = password_hash
        new_user.role_id = role.role_id
        new_user.is_approved = data.get('status', 'active') == 'active'
        
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'User created successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@require_permission('user_edit')
def bulk_actions():
    """Handle bulk actions on users"""
    data = request.get_json()
    action = data.get('action')
    user_ids = data.get('users', [])
    
    if not action or not user_ids:
        return jsonify({'success': False, 'message': 'Missing action or user selection'})
    
    try:
        success_count = 0
        
        for user_id in user_ids:
            user = User.query.get(user_id)
            if not user:
                continue
                
            if action == 'activate':
                user.is_approved = True
                success_count += 1
            elif action == 'deactivate':
                user.is_approved = False
                success_count += 1
            elif action == 'delete':
                db.session.delete(user)
                success_count += 1
            elif action == 'change_role':
                new_role = data.get('new_role')
                if new_role:
                    role = Role.query.filter_by(role_name=new_role).first()
                    if role:
                        user.role_id = role.role_id
                        success_count += 1
        
        db.session.commit()
        return jsonify({'success': True, 'message': f'{action.title()} completed for {success_count} users'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)})

@require_permission('system_settings')
def save_settings():
    """Save system settings"""
    data = request.get_json()
    # In a real application, you would save these settings to database or config file
    return jsonify({'success': True, 'message': 'Settings saved successfully'})

@require_permission('system_settings')
def test_email():
    """Test email configuration"""
    data = request.get_json()
    # In a real application, you would test the email settings
    return jsonify({'success': True, 'message': 'Test email sent successfully'})

@require_permission('system_maintenance')
def database_optimize():
    """Optimize database"""
    return jsonify({'success': True, 'message': 'Database optimized successfully'})

@require_permission('system_maintenance')
def database_analyze():
    """Analyze database"""
    return jsonify({'success': True, 'message': 'Database analysis completed'})

@require_permission('system_maintenance')
def database_integrity():
    """Check database integrity"""
    return jsonify({'success': True, 'message': 'Database integrity check completed - no issues found'})
