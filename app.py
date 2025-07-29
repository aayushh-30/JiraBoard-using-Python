from flask import Flask
from flask_login import LoginManager
from config import Config
from extensions import db, login_manager
from error_handling import register_error_handlers
import os
from sqlalchemy import text

# Import all models to ensure they're registered with SQLAlchemy
import models

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    
    # Configure login manager  
    setattr(login_manager, 'login_view', 'auth.login')
    setattr(login_manager, 'login_message', 'Please log in to access this page.')
    setattr(login_manager, 'login_message_category', 'info')
    
    @login_manager.user_loader
    def load_user(user_id):
        from controllers.auth_controllers import load_user as auth_load_user
        return auth_load_user(user_id)
    
    # Add middleware to handle aborted transactions
    @app.before_request
    def clear_db_session():
        """Clear any aborted database transactions before each request"""
        try:
            if db.session.is_active:
                db.session.rollback()
        except Exception:
            pass
    
    @app.teardown_appcontext
    def close_db_session(error):
        """Ensure database session is properly closed after each request"""
        try:
            if error:
                db.session.rollback()
            db.session.remove()
        except Exception:
            pass
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register blueprints
    try:
        from routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp, url_prefix='/auth')
        print("✅ Auth routes registered")
    except ImportError as e:
        print(f"❌ Auth routes failed: {e}")

    try:
        from routes.dashboard_routes import dashboard_bp
        app.register_blueprint(dashboard_bp)
        print("✅ Dashboard routes registered")
    except ImportError as e:
        print(f"❌ Dashboard routes failed: {e}")

    try:
        from routes.project_routes import project_bp
        app.register_blueprint(project_bp, url_prefix='/projects')
        print("✅ Project routes registered")
    except ImportError as e:
        print(f"❌ Project routes failed: {e}")

    try:
        from routes.team_routes import team_bp
        app.register_blueprint(team_bp, url_prefix='/teams')
        print("✅ Team routes registered")
    except ImportError as e:
        print(f"❌ Team routes failed: {e}")

    try:
        from routes.admin_routes import admin_bp
        app.register_blueprint(admin_bp)  # admin_bp already has url_prefix='/admin'
        print("✅ Admin routes registered")
    except ImportError as e:
        print(f"❌ Admin routes failed: {e}")

    try:
        from routes.user_routes import user_bp
        app.register_blueprint(user_bp, url_prefix='/users')
        print("✅ User routes registered")
    except ImportError as e:
        print(f"❌ User routes failed: {e}")

    try:
        from routes.task_routes import task_bp
        app.register_blueprint(task_bp, url_prefix='/tasks')
        print("✅ Task routes registered")
    except ImportError as e:
        print(f"❌ Task routes failed: {e}")

    try:
        from routes.report_routes import report_bp
        app.register_blueprint(report_bp, url_prefix='/reports')
        print("✅ Report routes registered")
    except ImportError as e:
        print(f"❌ Report routes failed: {e}")

    try:
        from routes.profile_routes import profile_bp
        app.register_blueprint(profile_bp)
        print("✅ Profile routes registered")
    except ImportError as e:
        print(f"❌ Profile routes failed: {e}")

    try:
        from routes.goal_routes import goal_bp
        app.register_blueprint(goal_bp, url_prefix='/goals')
        print("✅ Goal routes registered")
    except ImportError as e:
        print(f"❌ Goal routes failed: {e}")

    # Register permissions context processor
    from permissions import register_permission_context_processors
    register_permission_context_processors(app)
    
    # Add direct goals route
    @app.route('/goals')
    def direct_goals():
        """Direct goals route - redirect to new goal system"""
        from flask import redirect, url_for
        return redirect(url_for('goal.goals'))

    return app

def execute_sql_file(file_path):
    """Execute SQL commands from a file"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            sql_content = file.read()
        
        # Always start with a clean transaction
        try:
            db.session.rollback()
        except:
            pass
            
        sql_commands = sql_content.split(';')
        
        for command in sql_commands:
            command = command.strip()
            if command and not command.startswith('--'):
                try:
                    db.session.execute(text(command))
                except Exception:
                    # Rollback and start fresh after each error
                    try:
                        db.session.rollback()
                    except:
                        pass
                    continue
        
        # Try to commit, if it fails, rollback
        try:
            db.session.commit()
            print(f"✅ Successfully executed SQL file: {file_path}")
            return True
        except Exception as e:
            print(f"❌ Commit failed: {e}")
            try:
                db.session.rollback()
            except:
                pass
            return False
            
    except Exception as e:
        print(f"❌ Error executing SQL file: {e}")
        try:
            db.session.rollback()
        except:
            pass
        return False

def init_database():
    """Initialize database with sample data"""
    print("🔄 Initializing database...")
    
    # Always start with a clean transaction state
    try:
        db.session.rollback()
    except:
        pass
    
    # Create tables
    try:
        db.create_all()
        print("✅ Database tables created")
    except Exception as e:
        print(f"⚠️  Table creation warning: {e}")
        # Clear any failed transaction
        try:
            db.session.rollback()
        except:
            pass
    
    # Load sample data if file exists
    sample_data_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sample_data.sql')
    if os.path.exists(sample_data_file):
        print("🔄 Loading sample data...")
        execute_sql_file(sample_data_file)
        print("ℹ️  Run 'python update_passwords.py' to set passwords for sample users")
    
    # Ensure we end with a clean transaction state
    try:
        db.session.commit()
    except:
        try:
            db.session.rollback()
        except:
            pass
    
    print("✅ Database initialization complete!")

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        # Clear any aborted transactions first
        try:
            db.session.rollback()
            print("🔄 Cleared any pending transactions")
        except:
            pass
            
        try:
            init_database()
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            # Try to clear the failed transaction
            try:
                db.session.rollback()
            except:
                pass
    
    app.run(debug=True)
