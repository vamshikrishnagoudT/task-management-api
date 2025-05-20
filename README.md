Task Management API
  A RESTful API for managing users, projects, and tasks using Flask and PostgreSQL.
Setup Instructions

Clone the Repository:
git clone https://github.com/yourusername/task-management-api.git
cd task-management-api


Set Up Virtual Environment:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt


Set Up PostgreSQL:
sudo -u postgres psql

CREATE DATABASE task_management;
CREATE USER task_user WITH PASSWORD 'password123';
ALTER ROLE task_user SET client_encoding TO 'utf8';
ALTER ROLE task_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE task_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE task_management TO task_user;
\q


Create .env File:
touch .env

Add:
DATABASE_URL=postgresql://task_user:password123@localhost:5432/task_management
SECRET_KEY=your-secret-key


Seed the Database:
python scripts/seed.py


Run the Application:
python run.py


Test with Postman:

Import TaskManagementAPI.postman_collection.json into Postman.
Test endpoints:
Users:
POST /api/users: Create a user (e.g., {"username": "john", "email": "john@example.com"}).
GET /api/users: List all users.
GET /api/users/<id>: Get user by ID.


Projects:
POST /api/projects: Create a project (e.g., {"name": "New Project", "description": "A test project"}).
GET /api/projects: List all projects.
GET /api/projects/<id>: Get project by ID.
GET /api/projects/<id>/tasks: List tasks under a project (returns empty list for now).







Sprint Status

Sprint 1: User endpoints implemented with input validation and error handling.
Sprint 2: Project endpoints implemented, database seed script added, Postman tests updated.

