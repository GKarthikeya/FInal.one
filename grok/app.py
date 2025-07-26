from flask import Flask, request, jsonify
from celery.result import AsyncResult
from grok.tasks import check_attendance  # celery task

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Attendance API is live"}), 200

@app.route("/check", methods=["POST"])
def check():
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return jsonify({"error": "Missing 'username' or 'password'"}), 400

        task = check_attendance.delay(username, password)
        return jsonify({"task_id": task.id}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/result/<task_id>", methods=["GET"])
def result(task_id):
    try:
        result = AsyncResult(task_id)

        if result.state == "PENDING":
            return jsonify({"status": "Pending"}), 202
        elif result.state == "STARTED":
            return jsonify({"status": "In Progress"}), 202
        elif result.state == "SUCCESS":
            return jsonify({"status": "Done", "data": result.result}), 200
        elif result.state == "FAILURE":
            return jsonify({"status": "Failed", "error": str(result.result)}), 500
        else:
            return jsonify({"status": result.state}), 202

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/ping", methods=["GET"])
def ping():
    return "pong", 200

if __name__ == "__main__":
    app.run(debug=True)
