# JIRA Board Project Structure

## Directory Tree Structure

```
jira_board_shreyas_edited/
├── app.py                            # Main Flask application
├── config.py                         # Application configuration
├── extensions.py                     # Flask extensions initialization
├── error_handling.py                 # Global error handlers
├── permissions.py                    # Role-based access control
├── requirements.txt                  # Python dependencies
├── jira_board_schema.sql             # PostgreSQL database schema
├── sample_data.sql                   # Sample data for testing
│
├── controllers/                      # Business logic controllers (naming: {feature}_controllers.py)
│   ├── admin_controllers.py
│   ├── attachment_controllers.py
│   ├── audit_controllers.py
│   ├── auth_controllers.py
│   ├── board_controllers.py
│   └── ...
│
├── forms/                            # WTForms validation (naming: {feature}_forms.py)
│   ├── attachment_forms.py
│   ├── auth_forms.py
│   ├── board_forms.py
│   ├── comment_forms.py
│   ├── integration_forms.py
│   └── ...
│
├── models/                           # SQLAlchemy data models (naming: {feature}_models.py)
│   ├── admin_models.py
│   ├── advanced_models.py
│   ├── attachment_models.py
│   ├── audit_log_models.py
│   ├── board_models.py
│   └── ...
│
├── routes/                           # Flask route definitions (naming: {feature}_routes.py)
│   ├── admin_routes.py
│   ├── auth_routes.py
│   ├── board_routes.py
│   ├── comment_routes.py
│   ├── dashboard_routes.py
│   └── ...
│
├── static/                           # Static web assets (does not follow naming scheme)
│   ├── css/
│   ├── js/
│   ├── images/
│   └── uploads/
│
└── templates/                        # Jinja2 HTML templates (naming: {feature}/ folders)
    ├── base.html
    ├── index.html
    ├── auth/
    ├── admin/
    ├── projects/
    └── ...
```

## File Organization

### Core Files (Root Directory)
- **app.py**: Main Flask application entry point
- **config.py**: Application configuration settings
- **extensions.py**: Flask extensions initialization
- **error_handling.py**: Global error handlers
- **permissions.py**: Role-based access control decorators
- **requirements.txt**: Python package dependencies
- **jira_board_schema.sql**: PostgreSQL database schema
- **sample_data.sql**: Sample data for testing and development

### Naming Schemes

#### Controllers (controllers/)
**Pattern**: `{feature}_controllers.py`
- Contains business logic for specific features
- Examples: `auth_controllers.py`, `project_controllers.py`, `task_controllers.py`

#### Forms (forms/)
**Pattern**: `{feature}_forms.py`
- WTForms validation classes for specific features
- Examples: `auth_forms.py`, `project_forms.py`, `user_forms.py`

#### Models (models/)
**Pattern**: `{feature}_models.py`
- SQLAlchemy data models for specific entities
- Examples: `user_models.py`, `project_models.py`, `task_models.py`

#### Routes (routes/)
**Pattern**: `{feature}_routes.py`
- Flask blueprint route definitions for specific features
- Examples: `auth_routes.py`, `dashboard_routes.py`, `admin_routes.py`

#### Templates (templates/)
**Pattern**: `{feature}/` folders and feature-specific HTML files
- Jinja2 HTML templates organized by feature
- Examples: `auth/`, `admin/`, `projects/`, plus shared templates

#### Static Assets (static/)
**Note**: This folder does not follow the naming scheme
- Traditional web asset organization
- Contains: `css/`, `js/`, `images/`, `uploads/`
