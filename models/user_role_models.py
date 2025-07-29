"""
User Role models for handling multi-role assignments
"""

from .models_models import db, UUID
from datetime import datetime
import uuid

class UserRole(db.Model):
    """Junction table for user-role many-to-many relationship"""
    __tablename__ = 'user_roles'
    
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'), primary_key=True)
    role_id = db.Column(UUID(as_uuid=True), db.ForeignKey('role.role_id'), primary_key=True)
    assigned_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    assigned_by_id = db.Column(UUID(as_uuid=True), db.ForeignKey('user.user_id'))
    is_primary = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='user_roles')
    role = db.relationship('Role', backref='user_assignments')
    assigned_by = db.relationship('User', foreign_keys=[assigned_by_id])

    def __repr__(self):
        return f'<UserRole user_id={self.user_id} role_id={self.role_id} primary={self.is_primary}>'
    
    @classmethod
    def get_user_roles(cls, user_id):
        """Get all roles for a user"""
        return cls.query.filter_by(user_id=user_id).all()
    
    @classmethod
    def get_primary_role(cls, user_id):
        """Get the primary role for a user"""
        return cls.query.filter_by(user_id=user_id, is_primary=True).first()
    
    @classmethod
    def set_primary_role(cls, user_id, role_id):
        """Set a role as primary for a user"""
        # First, unset any existing primary role
        cls.query.filter_by(user_id=user_id, is_primary=True).update({'is_primary': False})
        
        # Set the new primary role
        user_role = cls.query.filter_by(user_id=user_id, role_id=role_id).first()
        if user_role:
            user_role.is_primary = True
            db.session.commit()
            return user_role
        return None
    
    @classmethod
    def add_role_to_user(cls, user_id, role_id, assigned_by_id=None, is_primary=False):
        """Add a role to a user"""
        # Check if user already has this role
        existing = cls.query.filter_by(user_id=user_id, role_id=role_id).first()
        if existing:
            return existing
            
        # If this is the first role for the user, make it primary
        user_role_count = cls.query.filter_by(user_id=user_id).count()
        if user_role_count == 0:
            is_primary = True
            
        # If setting as primary, unset any existing primary role
        if is_primary:
            cls.query.filter_by(user_id=user_id, is_primary=True).update({'is_primary': False})
        
        user_role = cls(
            user_id=user_id,
            role_id=role_id,
            assigned_by_id=assigned_by_id,
            is_primary=is_primary
        )
        
        db.session.add(user_role)
        db.session.commit()
        return user_role
    
    @classmethod
    def remove_role_from_user(cls, user_id, role_id):
        """Remove a role from a user"""
        user_role = cls.query.filter_by(user_id=user_id, role_id=role_id).first()
        if user_role:
            was_primary = user_role.is_primary
            db.session.delete(user_role)
            
            # If this was the primary role, set another role as primary
            if was_primary:
                remaining_role = cls.query.filter_by(user_id=user_id).first()
                if remaining_role:
                    remaining_role.is_primary = True
            
            db.session.commit()
            return True
        return False
