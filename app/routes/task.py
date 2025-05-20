from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User

task_bp = Blueprint('task', __name__)

@task_bp.route('/', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('project_id'):
        return jsonify({'error': 'Title and project_id are required'}), 400

    project = Project.query.get(data['project_id'])
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    user = User.query.get(data.get('user_id')) if data.get('user_id') else None
    if data.get('user_id') and not user:
        return jsonify({'error': 'User not found'}), 404

    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'pending'),
        project_id=data['project_id'],
        user_id=data.get('user_id')
    )

    # Handle dependencies
    dependency_ids = data.get('dependencies', [])
    for dep_id in dependency_ids:
        dep = Task.query.get(dep_id)
        if not dep:
            return jsonify({'error': f'Dependency task {dep_id} not found'}), 404
        if task.has_circular_dependency(dep_id):
            return jsonify({'error': f'Circular dependency detected with task {dep_id}'}), 400
        task.dependencies.append(dep)

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route('/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
def update_task_status(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json()
    if not data or not data.get('status'):
        return jsonify({'error': 'Status is required'}), 400

    new_status = data['status']
    if new_status not in ['pending', 'in_progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400

    if new_status == 'completed' and not task.are_dependencies_completed():
        return jsonify({'error': 'Cannot complete task until all dependencies are completed'}), 400

    task.status = new_status
    db.session.commit()
    return jsonify(task.to_dict()), 200

@task_bp.route('/user/<int:user_id>', methods=['GET'])
def list_user_tasks(user_id):
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user_id).all()
    return jsonify([task.to_dict() for task in tasks]), 200

@task_bp.route('/status/<status>', methods=['GET'])
def list_tasks_by_status(status):
    if status not in ['pending', 'in_progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400
    tasks = Task.query.filter_by(status=status).all()
    return jsonify([task.to_dict() for task in tasks]), 200