from flask import Blueprint, request, jsonify
from app import db
from app.models.project import Project

project_bp = Blueprint('project', __name__)

@project_bp.route('/', methods=['POST'])
def create_project():
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
def list_projects():
    projects = Project.query.all()
    return jsonify([project.to_dict() for project in projects]), 200

@project_bp.route('/<int:project_id>', methods=['GET'])
def get_project(project_id):
    project = Project.query.get_or_404(project_id)
    return jsonify(project.to_dict()), 200

@project_bp.route('/<int:project_id>/tasks', methods=['GET'])
def list_project_tasks(project_id):
    project = Project.query.get_or_404(project_id)
    # Since tasks aren't implemented yet, return empty list
    return jsonify([]), 200