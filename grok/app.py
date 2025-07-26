from flask import Flask, request, render_template, jsonify
from grok.tasks import check_attendance
import os
from celery.result import AsyncResult
from tabulate import tabulate

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("login.html")

@app.route("/attendance", methods=["POST"])
def attendance():
    username = request.form.get("username")
    password = request.form.get("password")

    if not username or not password:
        return "Missing credentials", 400

    task = check_attendance.delay({"username": username, "password": password})
    return jsonify({"task_id": task.id}), 202

@app.route("/status/<task_id>")
def task_status(task_id):
    task_result = AsyncResult(task_id)
    if task_result.state == "PENDING":
        return jsonify({"status": "pending"}), 202
    elif task_result.state == "SUCCESS":
        result = task_result.result
        table_html = tabulate(result["data"], headers="keys", tablefmt="html")
        return render_template("attendance.html", table_html=table_html, overall=result["overall"])
    else:
        return jsonify({"status": task_result.state}), 500

@app.route("/ping")
def ping():
    return jsonify({"message": "Attendance API is live"})
