from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models.user_models import User
from models.role_models import Role
from models.models_models import RoleName
from models.team_models import Team
from extensions import db
from permissions import require_role
import uuid
from datetime import datetime

# Try to import optional models
try:
    from models.team_member_models import TeamMember
except ImportError:
    TeamMember = None

try:
    from models.manager_models import Manager
except ImportError:
    Manager = None

try:
    from models.developer_models import Developer
except ImportError:
    Developer = None

@login_required
@require_role('admin')
def team_management():
    """Admin interface for team management"""
    teams = Team.query.all()
    users = User.query.all()
    
    # Get team members for each team (if TeamMember model exists)
    team_data = []
    for team in teams:
        if TeamMember:
            try:
                members = db.session.query(User, TeamMember).join(
                    TeamMember, User.user_id == TeamMember.user_id
                ).filter(TeamMember.team_id == team.team_id).all()
            except Exception:
                members = []
        else:
            members = []
        
        team_data.append({
            'team': team,
            'members': members
        })
    
    return render_template('admin/team_management.html', 
                         team_data=team_data, 
                         all_users=users)

@login_required
@require_role('admin')
def add_member_to_team():
    """API endpoint to add member to team"""
    if request.method != 'POST':
        return jsonify({'error': 'Method not allowed'}), 405
    
    return jsonify({'error': 'Team member management not available - models not configured'}), 501

@login_required
@require_role('admin')
def remove_member_from_team():
    """API endpoint to remove member from team"""
    if request.method != 'DELETE':
        return jsonify({'error': 'Method not allowed'}), 405
    
    return jsonify({'error': 'Team member management not available - models not configured'}), 501

@login_required
@require_role('admin')
def create_team():
    """Create new team"""
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description', '')
        
        if not name:
            return jsonify({'error': 'Team name is required'}), 400
        
        try:
            team = Team(
                team_id=uuid.uuid4(),
                name=name,
                description=description,
                created_at=datetime.utcnow()
            )
            db.session.add(team)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Team created successfully',
                'team_id': str(team.team_id)
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': 'Failed to create team'}), 500
    
    return jsonify({'error': 'Method not allowed'}), 405

@login_required
@require_role('admin')
def get_unassigned_users():
    """Get users not assigned to any team"""
    try:
        # Simple implementation - return all users for now
        users = User.query.filter(
            User.role.has(Role.role_name.in_([RoleName.manager, RoleName.developer]))
        ).all()
        
        users_data = [{
            'user_id': str(user.user_id),
            'username': user.username,
            'email': user.email,
            'role': user.role.role_name.value if user.role else 'unknown'
        } for user in users]
        
        return jsonify(users_data)
        
    except Exception as e:
        return jsonify({'error': 'Failed to fetch users'}), 500
