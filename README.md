Task Management API
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

 5. **Run the Application**:
    ```bash
    python run.py
    ```

 6. **Test with Postman**:
    - Import the Postman collection (to be provided).
    - Test endpoints:
      - `POST /api/users`: Create a user (e.g., `{"username": "xxx", "email": "xxx@gmail.com"}`).
      - `GET /api/users`: List all users.
      - `GET /api/users/<id>`: Get user by ID.

 ## Sprint 1 Status
 - User endpoints implemented.
 - Basic error handling and input validation added.

