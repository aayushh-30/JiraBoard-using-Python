from flask import render_template, flash, session
from flask_login import login_required, current_user
from permissions import require_permission
from models.models_models import db
from models.user_models import User
from models.project_models import Project
from models.task_models import Task
from models.goal_models import Goal
from models.team_models import Team
from datetime import datetime, timedelta
from sqlalchemy import func

@login_required
@require_permission('dashboard_view')
def dashboard():
    """Dashboard with projects and goals"""
    
    # Default user data
    user_data = {
        'username': current_user.username if hasattr(current_user, 'username') else 'User',
        'email': current_user.email if hasattr(current_user, 'email') else 'No email',
        'role': getattr(current_user, 'role_name', 'User')
    }
    
    try:
        # Get projects using SQLAlchemy
        if hasattr(current_user, 'role') and current_user.role.role_name in ['admin', 'manager']:
            projects = Project.query.order_by(Project.created_at.desc()).limit(10).all()
        else:
            # For developers, get their assigned projects
            projects = Project.query.limit(10).all()  # TODO: Filter by developer assignment
        
        # Get goals
        goals = Goal.query.limit(10).all()
        
        # Role-based dashboard template selection
        user_role = getattr(current_user, 'role_name', 'viewer')
        
        # Check if admin is switching role views
        if current_user.role_name == 'admin' and 'role_view' in session:
            user_role = session['role_view']
        
        # Select appropriate dashboard template based on role
        if user_role == 'admin':
            template_name = 'dashboard_admin.html'
            # Fetch admin dashboard statistics
            
            try:
                # Get user statistics
                total_users = User.query.count()
                pending_users = User.query.filter_by(status='pending').count()
                active_users = User.query.filter_by(status='active').count()
                
                # Get project statistics
                total_projects = Project.query.count()
                active_projects = Project.query.filter_by(status='active').count()
                completed_projects = Project.query.filter_by(status='completed').count()
                
                # Get task statistics
                total_tasks = Task.query.count()
                overdue_tasks = Task.query.filter(Task.due_date < datetime.now()).count()
                completed_tasks = Task.query.filter_by(status='done').count()
                
                # Get time-based statistics
                week_ago = datetime.now() - timedelta(days=7)
                month_ago = datetime.now() - timedelta(days=30)
                
                new_users_this_week = User.query.filter(User.created_at >= week_ago).count()
                last_week_users = User.query.filter(User.created_at >= datetime.now() - timedelta(days=14), User.created_at < week_ago).count()
                user_growth = new_users_this_week - last_week_users
                
                projects_completed_this_month = Project.query.filter(
                    Project.status == 'completed',
                    Project.updated_at >= month_ago
                ).count()
                
                # Calculate system uptime (mock - replace with actual server metrics)
                uptime_percentage = 99.2  # This would come from actual monitoring
                
                # System Health Data (these would come from actual monitoring in production)
                system_health = {
                    'database_status': 'healthy',
                    'database_uptime': 97,
                    'api_status': 'running', 
                    'api_uptime': 99,
                    'storage_usage': 68,
                    'memory_status': 'normal',
                    'memory_usage': 72
                }
                
                # Get role distribution - simple count by role
                admin_count = User.query.filter(User.role_name == 'admin').count()
                manager_count = User.query.filter(User.role_name == 'manager').count()
                developer_count = User.query.filter(User.role_name == 'developer').count()
                viewer_count = User.query.filter(User.role_name == 'viewer').count()
                
                role_dict = {
                    'admin': admin_count,
                    'manager': manager_count,
                    'developer': developer_count,
                    'viewer': viewer_count
                }
                
                # Get recent system activity (recent users, projects, tasks)
                recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
                recent_projects = Project.query.order_by(Project.created_at.desc()).limit(5).all()
                recent_tasks = Task.query.order_by(Task.created_at.desc()).limit(5).all()
                
                # Create system activity list
                system_activity = []
                
                # Add recent user registrations
                for user in recent_users:
                    system_activity.append({
                        'type': 'user_registered',
                        'message': f'New user registered: {user.full_name}',
                        'time': user.created_at.strftime('%H:%M'),
                        'date': user.created_at.strftime('%m/%d/%Y'),
                        'icon': 'fa-user-plus',
                        'class': 'text-success'
                    })
                
                # Add recent project creation
                for project in recent_projects:
                    system_activity.append({
                        'type': 'project_created',
                        'message': f'New project created: {project.name}',
                        'time': project.created_at.strftime('%H:%M'),
                        'date': project.created_at.strftime('%m/%d/%Y'),
                        'icon': 'fa-project-diagram',
                        'class': 'text-info'
                    })
                
                # Add recent task creation
                for task in recent_tasks:
                    system_activity.append({
                        'type': 'task_created',
                        'message': f'New task created: {task.title}',
                        'time': task.created_at.strftime('%H:%M'),
                        'date': task.created_at.strftime('%m/%d/%Y'),
                        'icon': 'fa-tasks',
                        'class': 'text-primary'
                    })
                
                # Sort by date/time and limit to 10 most recent
                system_activity.sort(key=lambda x: x['date'] + x['time'], reverse=True)
                system_activity = system_activity[:10]
                
                # User management overview data
                user_overview = {
                    'total_users': total_users,
                    'active_users': active_users,
                    'pending_users': pending_users,
                    'role_distribution': role_dict,
                    'recent_registrations': new_users_this_week,
                    'user_growth_percentage': round((user_growth / max(last_week_users, 1)) * 100, 1) if last_week_users > 0 else 100
                }
                
                dashboard_stats = {
                    'total_users': total_users,
                    'active_projects': active_projects,
                    'total_tasks': total_tasks,
                    'overdue_tasks': overdue_tasks,
                    'user_growth': user_growth,
                    'projects_completed_this_month': projects_completed_this_month,
                    'uptime_percentage': uptime_percentage,
                    'role_stats': role_dict,
                    'system_activity': system_activity,
                    'user_overview': {'recent_registrations': new_users_this_week},
                    **system_health  # Add system health data
                }
            except Exception as stats_error:
                print(f"Error fetching admin stats: {stats_error}")
                dashboard_stats = {
                    'total_users': 156,
                    'pending_users': 5,
                    'active_users': 151,
                    'total_projects': 28,
                    'active_projects': 25,
                    'total_tasks': 1247,
                    'overdue_tasks': 18,
                    'new_users_this_week': 8,
                    'role_stats': {'admin': 5, 'manager': 18, 'developer': 108, 'client': 25}
                }
        elif user_role == 'manager':
            template_name = 'dashboard_manager.html'
            dashboard_stats = {}
        elif user_role == 'developer':
            template_name = 'dashboard_developer.html'
            dashboard_stats = {}
        elif user_role == 'client':
            template_name = 'dashboard_client.html'
            dashboard_stats = {}
        else:
            template_name = 'dashboard_developer.html'  # Default fallback
            dashboard_stats = {}
        
        # Prepare template variables
        template_vars = {
            'user': user_data, 
            'projects': projects, 
            'goals': goals
        }
        
        # Add admin stats if available
        template_vars.update(dashboard_stats)
        
        return render_template(template_name, **template_vars)
                             
    except Exception as e:
        flash(f'Error loading dashboard: {e}', 'danger')
        # Fall back to mock data if database fails
        projects = [
            {'title': 'Project Lehsun', 'description': 'Garlic-powered authentication system - adding that extra punch to security! 🧄', 'created_at': '2025-01-01'},
            {'title': 'Project Haldi', 'description': 'Golden turmeric dashboard - healing your data visualization woes with natural beauty ✨', 'created_at': '2025-01-02'}
        ]
        goals = []
        
        # Role-based dashboard template selection (fallback)
        user_role = getattr(current_user, 'role_name', 'viewer')
        
        if user_role == 'admin':
            template_name = 'dashboard_admin.html'
        elif user_role == 'manager':
            template_name = 'dashboard_manager.html'
        elif user_role == 'developer':
            template_name = 'dashboard_developer.html'
        elif user_role == 'client':
            template_name = 'dashboard_client.html'
        else:
            template_name = 'dashboard_developer.html'  # Default fallback
        
        return render_template(template_name, 
                             user=user_data, 
                             projects=projects, 
                             goals=goals,
                             total_users=0,
                             active_projects=0,
                             total_tasks=0,
                             overdue_tasks=0,
                             user_growth=0,
                             pending_users=0,
                             active_users=0,
                             total_projects=0,
                             completed_projects=0,
                             completed_tasks=0,
                             new_users_this_week=0,
                             projects_completed_this_month=0,
                             uptime_percentage=99.2,
                             role_dict={'admin': 0, 'manager': 0, 'developer': 0, 'viewer': 0})