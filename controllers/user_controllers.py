from flask import render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from permissions import require_permission, require_role
from datetime import datetime
from werkzeug.security import generate_password_hash
from models.user_models import User
from models.role_models import Role
from extensions import db

@login_required
@require_permission('profile_edit')
def update_profile():
    """Update user profile"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        contact_no = request.form.get('contact_no')
        password = request.form.get('password')
        
        try:
            # Check if email already exists (excluding current user)
            existing_user = User.query.filter(
                User.email == email, 
                User.user_id != current_user.user_id
            ).first()
            
            if existing_user:
                flash('Email already in use.', 'danger')
                return render_template('user_profile.html')
            
            # Update user profile
            user = User.query.get(current_user.user_id)
            if user:
                user.username = username
                user.email = email
                user.contact_no = contact_no
                user.updated_at = datetime.utcnow()
                
                if password:
                    user.password_hash = generate_password_hash(password)
                
                db.session.commit()
                flash('Profile updated successfully!', 'success')
                return redirect('/admin/users')
            else:
                flash('User not found.', 'danger')
                
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating profile: {e}', 'danger')
    
    return render_template('user_profile.html')

@login_required
@require_permission('user_view')
def get_user(user_id):
    """View user details with properly formatted role"""
    user = User.query.get_or_404(user_id)
    
    # Format role name properly
    role_name = user.role.role_name.value if hasattr(user.role.role_name, 'value') else str(user.role.role_name)
    role_name = role_name.replace('RoleName.', '').title()  # Remove prefix and capitalize
    
    # Create user data with formatted role
    user_data = {
        'user_id': user.user_id,
        'username': user.username,
        'email': user.email,
        'contact_no': user.contact_no,
        'created_at': user.created_at,
        'updated_at': user.updated_at,
        'is_approved': user.is_approved,
        'role_name': role_name,
        'status': 'Approved' if user.is_approved else 'Pending'
    }
    
    return render_template('user_detail.html', user=user_data)

def update_user(user_id):
    """Edit user details"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.role = request.form.get('role', user.role)
        user.is_approved = request.form.get('is_approved') == 'on'
        
        try:
            db.session.commit()
            flash(f'User {user.username} updated successfully!', 'success')
            return redirect(f'/users/{user_id}')
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {str(e)}', 'error')
    
    return render_template('user_edit.html', user=user)

def create_user():
    """Create a new user"""
    from forms.user_forms import UserForm
    
    form = UserForm()
    
    if form.validate_on_submit():
        try:
            # Check if email already exists
            existing_user = User.query.filter_by(email=form.email.data).first()
            if existing_user:
                flash('Email already exists!', 'error')
                return render_template('user_create.html', form=form)
            
            # Create new user
            new_user = User()
            new_user.username = form.username.data
            new_user.email = form.email.data
            new_user.contact_no = form.contact_no.data
            new_user.role_id = form.role.data
            new_user.is_approved = form.is_approved.data
            new_user.set_password(form.password.data)
            
            db.session.add(new_user)
            db.session.commit()
            flash(f'User {new_user.username} created successfully!', 'success')
            return redirect('/users/')
            
        except Exception as e:
            db.session.rollback()
            flash(f'Error creating user: {str(e)}', 'error')
    
    return render_template('user_create.html', form=form)

@login_required
@require_role('admin')
@login_required
@require_permission('user_view')
def get_users():
    """Enhanced user management with role statistics (admin only)"""
    try:
        # Get all users with their roles using SQLAlchemy
        users = db.session.query(User, Role).join(Role).order_by(User.created_at.desc()).all()
        
        user_list = []
        role_stats = {}
        
        for user, role in users:
            # Fix role display format
            role_name = role.role_name.value if hasattr(role.role_name, 'value') else str(role.role_name)
            role_name = role_name.replace('RoleName.', '').title()  # Remove prefix and capitalize
            
            user_list.append({
                'user_id': user.user_id,
                'username': user.username,
                'email': user.email,
                'contact_no': user.contact_no,
                'created_at': user.created_at,
                'updated_at': user.updated_at,
                'is_approved': user.is_approved,
                'role_name': role_name,
                'status': 'Approved' if user.is_approved else 'Pending'
            })
            
            # Count roles for statistics
            if role_name not in role_stats:
                role_stats[role_name] = 0
            role_stats[role_name] += 1
        
        # Calculate total users
        total_users = len(user_list)
        
        # Add total to role stats
        role_stats['Total'] = total_users
        
        return render_template('user_list.html', users=user_list, role_stats=role_stats)
        
    except Exception as e:
        flash(f'Error loading users: {e}', 'danger')
        return render_template('user_list.html', users=[], role_stats={})

@login_required
@require_permission('user_approve')
def approve_user():
    """Approve a user"""
    user_id = request.form.get('user_id')
    
    try:
        user = User.query.get(user_id)
        if user:
            user.is_approved = True
            user.updated_at = datetime.utcnow()
            db.session.commit()
            return jsonify({'success': True, 'message': 'User approved successfully'})
        else:
            return jsonify({'success': False, 'message': 'User not found'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': f'Error: {e}'})

@login_required
@require_permission('user_delete')
def delete_user():
    """Delete a user"""
    user_id = request.form.get('user_id')
    
    if str(user_id) == str(current_user.user_id):
        return jsonify({'success': False, 'message': 'Cannot delete your own account'})
    
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
        return jsonify({'success': False, 'message': f'Error: {e}'})