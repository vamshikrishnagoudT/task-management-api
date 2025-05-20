from flask import Blueprint, request, jsonify
from app import db
from app.models.task import Task
from app.models.project import Project
from app.models.user import User
from app.utils.auth import token_required

task_bp = Blueprint('task', __name__)

@task_bp.route('/', methods=['POST'])
@token_required
def create_task(current_user):
    data = request.get_json()
    if not data or not data.get('title') or not data.get('project_id'):
        return jsonify({'error': 'Title and project_id are required'}), 400

    project = db.session.get(Project, data['project_id'])
    if not project:
        return jsonify({'error': 'Project not found'}), 404

    user = db.session.get(User, data.get('user_id')) if data.get('user_id') else None
    if data.get('user_id') and not user:
        return jsonify({'error': 'User not found'}), 404

    task = Task(
        title=data['title'],
        description=data.get('description'),
        status=data.get('status', 'pending'),
        project_id=data['project_id'],
        user_id=data.get('user_id')
    )

    max_id = db.session.query(db.func.max(Task.id)).scalar() or 0
    new_task_id = max_id + 1

    dependency_ids = data.get('dependencies', [])
    for dep_id in dependency_ids:
        dep = db.session.get(Task, dep_id)
        if not dep:
            return jsonify({'error': f'Dependency task {dep_id} not found'}), 404
        if task.has_circular_dependency(dep_id, new_task_id):
            return jsonify({'error': f'Circular dependency detected with task {dep_id}'}), 400
        task.dependencies.append(dep)

    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

@task_bp.route('/<int:task_id>', methods=['GET'])
@token_required
def get_task(current_user, task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task.to_dict()), 200

@task_bp.route('/<int:task_id>/status', methods=['PUT'])
@token_required
def update_task_status(current_user, task_id):
    task = db.session.get(Task, task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
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
@token_required
def list_user_tasks(current_user, user_id):
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tasks = Task.query.filter_by(user_id=user_id).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'tasks': [task.to_dict() for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'page': page
    }), 200

@task_bp.route('/status/<status>', methods=['GET'])
@token_required
def list_tasks_by_status(current_user, status):
    if status not in ['pending', 'in_progress', 'completed']:
        return jsonify({'error': 'Invalid status'}), 400
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tasks = Task.query.filter_by(status=status).paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'tasks': [task.to_dict() for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'page': page
    }), 200