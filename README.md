# JiraBoard using Python

A web application to simulate/implement a Jira‑style board using Python. It includes user roles & permissions, project/task management, and a UI for viewing and interacting with boards.

---

## Table of Contents

- [Features](#features)  
- [Project Structure](#project-structure)  
- [Installation](#installation)  
- [Configuration](#configuration)  
- [Database Schema & Sample Data](#database-schema--sample-data)  
- [Usage](#usage)  
- [Error Handling](#error-handling)  
- [Permissions](#permissions)  
- [Contributing](#contributing)  
- [License](#license)  

---

## Features

- Role‑based access control and permissions  
- Create, update, delete projects/tasks/boards  
- Web interface (HTML/CSS/JavaScript)  
- Backend in Python (Flask)  
- Error handling  
- Static assets & templates support  
- Sample data for testing  

---

## Project Structure

```
JiraBoard-using-Python/
├── app.py
├── config.py
├── extensions.py
├── error_handling.py
├── permissions.py
├── controllers/
├── forms/
├── models/
├── routes/
├── static/
├── templates/
├── requirements.txt
├── jira_board_schema.sql
├── sample_data.sql
├── credentials.txt
└── docs/
    ├── project_structure.md
    ├── role_permissions.md
    └── Permissions_Refactoring_Guide.md
```

- `app.py`: Main application entry point  
- `config.py`: Configuration settings  
- `extensions.py`: Initialization of extensions (database, etc.)  
- `controllers / routes / models / forms`: MVC‑style separation of concerns  
- `static` & `templates`: Frontend assets and HTML templates  
- `jira_board_schema.sql`: SQL script to create the schema  
- `sample_data.sql`: Sample data for populating the database  
- `credentials.txt`: Contains credentials (Ensure **NOT** to commit real credentials to public repos.)  

---

## Installation

1. Clone the repository:  
   ```bash
   git clone https://github.com/aayushh-30/JiraBoard-using-Python.git
   cd JiraBoard-using-Python
   ```

2. Create a virtual environment (optional, but recommended):  
   ```bash
   python3 -m venv venv
   source venv/bin/activate     # On Linux/Mac
   venv\Scripts\activate        # On Windows
   ```

3. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

---

## Configuration

- Edit `config.py` for settings (database URI, secret keys, etc.)  
- `credentials.txt` is used for storing user/passwords — for dev/test only. Do **not** use in production without securing properly.  
- If needed, set environment variables for configuration overrides.

---

## Database Schema & Sample Data

- Run `jira_board_schema.sql` on your database to create the necessary tables.  
- Use `sample_data.sql` to insert test/sample data.  
- Ensure your database connection matches what's in `config.py`.

---

## Usage

1. After installation & database setup, start the application:  
   ```bash
   python app.py
   ```

2. Open a browser and navigate to the local server (e.g. `http://localhost:5000` or whatever port is configured).  

3. Log in as a user (create via sample data or via CLI/forms, depending on what's implemented).  

4. Use the UI to create projects, tasks, work with boards etc., according to your permissions.

---

## Error Handling

- The module `error_handling.py` provides mechanisms to catch and manage application errors.  
- The UI may show user‑friendly messages on failures; logs or console will have more info.  

---

## Permissions

- Roles & permissions logic is handled in `permissions.py` and relevant guides in the `role_permissions.md` file.  
- The `Permissions_Refactoring_Guide.md` contains ideas/plans/code rules to refactor or extend the permissions setup.

---

## Contributing

If you’d like to contribute:

1. Fork the repo  
2. Create a new branch (e.g. `feature/my-feature`)  
3. Make sure linting/tests etc. pass  
4. Open a pull request, describing the changes.

---

## License

Specify your license here (MIT, GPL, etc.). If there’s no license yet, consider adding one to clarify usage.

---

## Contact / Acknowledgements

- Author: *[aayushh‑30]*  
- Thank you to contributors, feedback, etc.
