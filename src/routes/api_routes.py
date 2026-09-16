"""JSON REST API for tasks."""
from flask import Blueprint, jsonify, request, current_app
from src.services.business_logic import TaskService

api_bp = Blueprint("api", __name__)


def _service():
    return TaskService(current_app.config["DATA_FILE"])


@api_bp.route("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.route("/tasks", methods=["GET"])
def list_tasks():
    done_param = request.args.get("done")
    done = None
    if done_param is not None:
        done = done_param.lower() == "true"
    return jsonify([t.to_dict() for t in _service().list_all(done=done)])


@api_bp.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json(silent=True) or {}
    title = (data.get("title") or "").strip()
    if not title:
        return jsonify({"error": "title is required"}), 400
    try:
        task = _service().add(title, data.get("priority", "medium"))
        return jsonify(task.to_dict()), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@api_bp.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    try:
        return jsonify(_service().get(task_id).to_dict())
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


@api_bp.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    try:
        return jsonify(_service().complete(task_id).to_dict())
    except KeyError as e:
        return jsonify({"error": str(e)}), 404


@api_bp.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    try:
        _service().delete(task_id)
        return "", 204
    except KeyError as e:
        return jsonify({"error": str(e)}), 404
