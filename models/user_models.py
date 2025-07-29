from .models_models import db, UUID
from datetime import datetime
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import session

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.role_id'), nullable=False)
    contact_no = db.Column(db.String(15))
    company_name = db.Column(db.String(100))
    is_approved = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    role = db.relationship('Role', backref='users')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_id(self):
        """Required for Flask-Login"""
        return str(self.user_id)
    
    @property
    def role_name(self):
        """Get the role name as a string for template access"""
        # Check for active role in session (for role switching)
        active_role = session.get('active_role')
        if active_role:
            return active_role
            
        if self.role and hasattr(self.role, 'role_name'):
            return self.role.role_name.value if hasattr(self.role.role_name, 'value') else str(self.role.role_name)
        return None
    
    @property
    def primary_role(self):
        """Get the primary role from user_roles table"""
        from .user_role_models import UserRole
        primary_user_role = UserRole.get_primary_role(self.user_id)
        if primary_user_role:
            return primary_user_role.role
        return self.role  # Fallback to direct role relationship
    
    def get_all_roles(self):
        """Get all roles assigned to this user"""
        from .user_role_models import UserRole
        user_roles = UserRole.get_user_roles(self.user_id)
        roles = []
        for user_role in user_roles:
            role_name = user_role.role.role_name.value if hasattr(user_role.role.role_name, 'value') else str(user_role.role.role_name)
            roles.append({
                'role_id': user_role.role_id,
                'role_name': role_name,
                'is_primary': user_role.is_primary,
                'assigned_at': user_role.assigned_at
            })
        
        # If no roles in user_roles table, fall back to direct role relationship
        if not roles and self.role:
            role_name = self.role.role_name.value if hasattr(self.role.role_name, 'value') else str(self.role.role_name)
            roles.append({
                'role_id': self.role_id,
                'role_name': role_name,
                'is_primary': True,
                'assigned_at': self.created_at
            })
            
        return roles
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        user_roles = self.get_all_roles()
        return any(role['role_name'] == role_name for role in user_roles)
    
    def get_active_role_name(self):
        """Get the currently active role (from session or primary role)"""
        active_role = session.get('active_role')
        if active_role and self.has_role(active_role):
            return active_role
        return self.primary_role.role_name.value if self.primary_role else None
    
    def switch_active_role(self, role_name):
        """Switch the active role in session"""
        if self.has_role(role_name):
            session['active_role'] = role_name
            return True
        return False
    
    def has_permission(self, permission):
        """Check if user has specific permission based on active role"""
        role_permissions = {
            'admin': ['all'],
            'manager': ['create_project', 'manage_team', 'assign_tasks', 'view_reports'],
            'developer': ['create_task', 'update_task', 'add_viewer'],
            'client': ['view_assigned', 'comment_on_assigned'],
            'viewer': ['view_assigned_issues']
        }
        
        active_role = self.get_active_role_name()
        user_permissions = role_permissions.get(active_role or '', [])
        return 'all' in user_permissions or permission in user_permissions