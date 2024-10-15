from flask import Flask, jsonify, request
from flask_cors import CORS
from tinydb import Query, TinyDB

app = Flask(__name__)

# Initialize TinyDB and specify the JSON file for storage
db = TinyDB("tasks.json")
Task = Query()

CORS(
    app,
    origins="*",
    methods=["GET", "POST", "PUT", "DELETE"],
    supports_credentials=True,
    allow_headers=["Content-Type", "Authorization", "test"],
)
app.config["CORS_HEADERS"] = "Content-Type"


# Route to insert a new task
@app.route("/task", methods=["POST"])
def add_task():
    new_task = {
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "completed": False,
    }
    task_id = db.insert(new_task)  # Insert task and return its ID
    new_task["id"] = task_id  # Add the ID to the task
    return jsonify(new_task), 201


# Route to edit a task
@app.route("/task/<int:task_id>", methods=["PUT"])
def edit_task(task_id):
    tasks = db.all()  # Retrieve all tasks
    task = db.get(doc_id=task_id)  # Find the task by its doc_id

    if task:
        # Update the task with new values if provided
        db.update(
            {
                "title": request.json.get("title", task["title"]),
                "description": request.json.get("description", task["description"]),
                "completed": request.json.get("completed", task["completed"]),
            },
            doc_ids=[task_id],
        )
        updated_task = db.get(doc_id=task_id)
        return jsonify(updated_task), 200

    return jsonify({"error": "Task not found"}), 404


# Route to delete a task
@app.route("/task/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = db.get(doc_id=task_id)

    if task:
        db.remove(doc_ids=[task_id])
        return jsonify({"message": "Task deleted"}), 200

    return jsonify({"error": "Task not found"}), 404


@app.route("/tasks", methods=["GET"])
def get_tasks():
    tasks = db.all()  # Get all tasks from TinyDB
    # Add 'id' to each task, corresponding to its doc_id
    tasks_with_id = []
    for task in tasks:
        task_id = task.doc_id  # Get the task's doc_id
        task_with_id = task.copy()  # Create a copy of the task to avoid modifying the original
        task_with_id["id"] = task_id  # Add the 'id' field
        tasks_with_id.append(task_with_id)  # Append the task with id to the list

    return jsonify(tasks_with_id), 200

if __name__ == "__main__":
    app.run(debug=True)
