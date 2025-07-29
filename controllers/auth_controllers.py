from flask import request, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from permissions import require_permission
from models.user_models import User
from models.role_models import Role
from models.models_models import db, RoleName
import uuid

def load_user(user_id):
    """Load user for Flask-Login - SIMPLE VERSION"""
    try:
        import psycopg2
        
        conn = psycopg2.connect(
            host="localhost",
            database="dhaniya_db", 
            user="postgres",
            password="ShrK.postgres"
        )
        
        cur = conn.cursor()
        cur.execute('''
            SELECT u.user_id, u.username, u.email, u.role_id, r.role_name 
            FROM "user" u 
            JOIN "role" r ON u.role_id = r.role_id 
            WHERE u.user_id = %s;
        ''', (user_id,))
        user_data = cur.fetchone()
        
        if user_data:
            class SimpleUser:
                def __init__(self, user_id, username, email, role_id, role_name):
                    self.user_id = str(user_id)
                    self.username = username
                    self.email = email
                    self.role_id = str(role_id)
                    # Convert role_name to string if it's an enum or other type
                    self.role_name = str(role_name) if role_name else 'viewer'
                    self.is_authenticated = True
                    self.is_active = True
                    self.is_anonymous = False
                    self.is_approved = True  # Add is_approved attribute
                    
                    # Create a simple role object for compatibility
                    class SimpleRole:
                        def __init__(self, role_name):
                            self.role_name = role_name
                    
                    self.role = SimpleRole(self.role_name)
                
                def get_id(self):
                    return self.user_id
            
            # print(f"🔍 LOAD_USER: role_name from DB = '{user_data[4]}'")
            user = SimpleUser(user_data[0], user_data[1], user_data[2], user_data[3], user_data[4])
            # print(f"🔍 LOAD_USER: user.role_name = '{user.role_name}'")
            cur.close()
            conn.close()
            return user
            
        cur.close()
        conn.close()
        return None
        
    except Exception:
        return None

def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_page'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Remove debug output for production
        # print(f"🔍 LOGIN ATTEMPT: email='{email}', password='{'*' * len(password) if password else 'None'}'")
        
        if email and password:
            try:
                # Clear any aborted transactions before query
                try:
                    db.session.rollback()
                except:
                    pass
                    
                user = User.query.filter_by(email=email).first()
                # print(f"🔍 USER FOUND: {user is not None}")
                
                if user:
                    # print(f"🔍 USER DETAILS: {user.username} ({user.email})")
                    password_match = user.check_password(password)
                    # print(f"🔍 PASSWORD MATCH: {password_match}")
                    
                    if password_match:
                        login_user(user, remember=bool(request.form.get('remember')))
                        # print("✅ LOGIN_USER CALLED")
                        flash('Login successful!', 'success')
                        
                        next_page = request.args.get('next')
                        redirect_url = next_page if next_page else url_for('dashboard.dashboard_page')
                        # print(f"🔄 REDIRECTING TO: {redirect_url}")
                        return redirect(redirect_url)
                    else:
                        # print("❌ PASSWORD MISMATCH")
                        flash('Invalid email or password.', 'danger')
                else:
                    # print("❌ USER NOT FOUND")
                    flash('Invalid email or password.', 'danger')
            except Exception as e:
                # Handle aborted transactions with user-friendly message
                # print(f"❌ LOGIN EXCEPTION: {e}")
                try:
                    db.session.rollback()
                except:
                    pass
                flash('Login temporarily unavailable. Please try again.', 'warning')
        else:
            # print("❌ MISSING EMAIL OR PASSWORD")
            flash('Please enter both email and password.', 'danger')
    
    return render_template('auth_login.html')

def register():
    """User registration"""
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.dashboard_page'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('auth_register.html')
        
        if not all([username, email, password]):
            flash('Please fill all fields.', 'danger')
            return render_template('auth_register.html')
        
        try:
            # Clear any aborted transactions before queries
            try:
                db.session.rollback()
            except:
                pass
                
            # Check if user already exists
            if User.query.filter_by(email=email).first():
                flash('Email already exists.', 'danger')
                return render_template('auth_register.html')
            
            if User.query.filter_by(username=username).first():
                flash('Username already exists.', 'danger')
                return render_template('auth_register.html')
            
            # Get default developer role
            role = Role.query.filter_by(role_name=RoleName.developer).first()
            if not role:
                flash('Registration system error. Please contact administrator.', 'danger')
                return render_template('auth_register.html')
            
            # Create user
            user = User()
            user.user_id = uuid.uuid4()
            user.username = username
            user.email = email
            user.role_id = role.role_id
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            flash('Registration successful! You can now login.', 'success')
            return redirect(url_for('auth.login'))
            
        except Exception as e:
            try:
                db.session.rollback()
            except:
                pass
            flash('Registration failed. Please try again.', 'danger')
            print(f"Registration error: {e}")  # Log for debugging only
            return render_template('auth_register.html')
    
    return render_template('auth_register.html')

def logout():
    """User logout"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))