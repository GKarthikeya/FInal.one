# File: grok/app.py

from flask import Flask, request, render_template
from celery.result import AsyncResult
from grok.tasks import check_attendance
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return render_template("login.html")

@app.route("/attendance", methods=["POST"])
def handle_attendance():
    username = request.form.get("username")
    password = request.form.get("password")
    if not username or not password:
        return "Missing credentials", 400

    task = check_attendance.delay({"username": username, "password": password})
    return render_template("loading.html", task_id=task.id)

@app.route("/result/<task_id>", methods=["GET"])
def get_result(task_id):
    task = AsyncResult(task_id)
    if task.state == "PENDING":
        return render_template("loading.html", task_id=task_id)
    elif task.state == "SUCCESS":
        result = task.result
        return render_template("attendance.html", table_html=result["table"], overall=result["overall"])
    elif task.state == "FAILURE":
        return "Failed to fetch attendance", 500
    else:
        return "Task in progress...", 202
