from flask import Flask, request, jsonify, render_template, redirect, url_for
from celery.result import AsyncResult
from .tasks import check_attendance
import os

app = Flask(__name__)

@app.route("/")
def index():
    return jsonify({"message": "Attendance API is live"})

@app.route("/attendance", methods=["POST"])
def attendance():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return jsonify({"error": "Missing credentials"}), 400

    # Start background task
    task = check_attendance.delay({"username": username, "password": password})
    return redirect(url_for("loading", task_id=task.id))

@app.route("/loading/<task_id>")
def loading(task_id):
    return f"Task {task_id} is in progress. Please wait or refresh to check status."

@app.route("/result/<task_id>")
def result(task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return jsonify({"status": "Pending"})
    elif task_result.state == "SUCCESS":
        return jsonify(task_result.result)
    elif task_result.state == "FAILURE":
        return jsonify({"status": "Failed", "error": str(task_result.info)}), 500
    else:
        return jsonify({"status": task_result.state})
