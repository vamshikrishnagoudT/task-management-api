 A RESTful API for managing users, projects, and tasks using Flask and PostgreSQL.

 ## Setup Instructions

 1. **Clone the Repository**:
    ```bash
    git clone https://github.com/yourusername/task-management-api.git
    cd task-management-api
    ```

 2. **Set Up Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

 3. **Set Up PostgreSQL**:
    ```bash
    sudo -u postgres psql
    ```
    ```sql
    CREATE DATABASE task_management;
    CREATE USER task_user WITH PASSWORD 'password123';
    ALTER ROLE task_user SET client_encoding TO 'utf8';
    ALTER ROLE task_user SET default_transaction_isolation TO 'read committed';
    ALTER ROLE task_user SET timezone TO 'UTC';
    GRANT ALL PRIVILEGES ON DATABASE task_management TO task_user;
    \q
    ```

 4. **Create .env File**:
    ```bash
    touch .env
    ```
    Add:
    ```
    DATABASE_URL=postgresql://task_user:password123@localhost:5432/task_management
    SECRET_KEY=your-secret-key
    ```

 5. **Seed the Database**:
    ```bash
    python scripts/seed.py
    ```

 6. **Run the Application**:
    ```bash
    python run.py
    ```

 7. **Test with Postman**:
    - Import `TaskManagementAPI.postman_collection.json` into Postman.
    - Test endpoints:
      - **Users**:
        - `POST /api/users`: Create a user (e.g., `{"username": "john", "email": "john@example.com"}`).
        - `GET /api/users`: List all users.
        - `GET /api/users/<id>`: Get user by ID.
      - **Projects**:
        - `POST /api/projects`: Create a project (e.g., `{"name": "New Project", "description": "A test project"}`).
        - `GET /api/projects`: List all projects.
        - `GET /api/projects/<id>`: Get project by ID.
        - `GET /api/projects/<id>/tasks`: List tasks under a project.
      - **Tasks**:
        - `POST /api/tasks`: Create a task (e.g., `{"title": "Deploy App", "project_id": 1, "user_id": 1, "dependencies": [1]}`).
        - `GET /api/tasks/<id>`: Get task by ID.
        - `PUT /api/tasks/<id>/status`: Update task status (e.g., `{"status": "completed"}`).
        - `GET /api/tasks/user/<user_id>`: List tasks for a user.
        - `GET /api/tasks/status/<status>`: List tasks by status (e.g., `pending`).

 ## Sprint Status
 - **Sprint 1**: User endpoints implemented with input validation and error handling.
 - **Sprint 2**: Project endpoints implemented, database seed script added, Postman tests updated.
 - **Sprint 3**: Task endpoints implemented with dependency logic (circular dependency prevention, status update constraints).