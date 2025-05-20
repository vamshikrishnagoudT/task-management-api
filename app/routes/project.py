from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project
from app.utils.auth import token_required

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['POST'])
@token_required
def create_project(current_user):
    data = request.get_json()
    if not data or not data.get('name'):
        return jsonify({'error': 'Project name is required'}), 400

    project = Project(
        name=data['name'],
        description=data.get('description')
    )
    db.session.add(project)
    db.session.commit()
    return jsonify(project.to_dict()), 201

@project_bp.route('/', methods=['GET'])
@token_required
def list_projects(current_user):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    projects = Project.query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'projects': [project.to_dict() for project in projects.items],
        'total': projects.total,
        'pages': projects.pages,
        'page': page
    }), 200

@project_bp.route('/<int:project_id>', methods=['GET'])
@token_required
def get_project(current_user, project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict()), 200

@project_bp.route('/<int:project_id>/tasks', methods=['GET'])
@token_required
def list_project_tasks(current_user, project_id):
    project = Project.query.get_or_404(project_id)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    tasks = project.tasks.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        'tasks': [task.to_dict() for task in tasks.items],
        'total': tasks.total,
        'pages': tasks.pages,
        'page': page
    }), 200