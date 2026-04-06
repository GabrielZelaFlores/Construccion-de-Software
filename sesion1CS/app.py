from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return """
    <h1> API Flask - Homework Session 1</h1>
    <p>Servidor funcionando correctamente.</p>
    <h2>Rutas disponibles:</h2>
    <ul>
        <li><b>GET</b> /tasks</li>
        <li><b>POST</b> /tasks</li>
        <li><b>GET</b> /tasks/&lt;int:task_id&gt;</li>
        <li><b>PUT</b> /tasks/&lt;int:task_id&gt;</li>
        <li><b>DELETE</b> /tasks/&lt;int:task_id&gt;</li>
        <br>
        <li><b>GET</b> /users</li>
        <li><b>POST</b> /users</li>
        <li><b>GET</b> /users/&lt;int:user_id&gt;</li>
        <li><b>PUT</b> /users/&lt;int:user_id&gt;</li>
        <li><b>DELETE</b> /users/&lt;int:user_id&gt;</li>
    </ul>
    </body>
    """

tasks = []

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    return jsonify({"task": tasks[task_id]})

@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.get_json()
    if not data or not data.get("content") or not str(data.get("content")).strip():
        return jsonify({"error": "Content is required and cannot be empty"}), 400
    
    task = {
        "id": len(tasks),
        "content": str(data["content"]).strip(),
        "done": data.get("done", False)
    }
    tasks.append(task)
    return jsonify({"message": "Task created successfully", "task": task}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if "content" in data and str(data["content"]).strip():
        tasks[task_id]["content"] = str(data["content"]).strip()
    if "done" in data:
        tasks[task_id]["done"] = bool(data["done"])
    
    return jsonify({"message": "Task updated", "task": tasks[task_id]})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id < 0 or task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    removed = tasks.pop(task_id)
    for i, t in enumerate(tasks):
        t["id"] = i
    return jsonify({"message": "Task deleted", "task": removed})

users = []

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})

@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    if user_id < 0 or user_id >= len(users):
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": users[user_id]})

@app.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    if not data or not data.get("name") or not data.get("lastname"):
        return jsonify({"error": "Name and lastname are required"}), 400
    
    user = {
        "id": len(users),
        "name": str(data.get("name")).strip(),
        "lastname": str(data.get("lastname")).strip(),
        "address": data.get("address", {})
    }
    users.append(user)
    return jsonify({"message": "User created successfully", "user": user}), 201

@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id < 0 or user_id >= len(users):
        return jsonify({"error": "User not found"}), 404
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if "name" in data and str(data["name"]).strip():
        users[user_id]["name"] = str(data["name"]).strip()
    if "lastname" in data and str(data["lastname"]).strip():
        users[user_id]["lastname"] = str(data["lastname"]).strip()
    if "address" in data:
        users[user_id]["address"] = data["address"]
    
    return jsonify({"message": "User updated", "user": users[user_id]})

@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id < 0 or user_id >= len(users):
        return jsonify({"error": "User not found"}), 404
    removed = users.pop(user_id)
    for i, u in enumerate(users):
        u["id"] = i
    return jsonify({"message": "User deleted", "user": removed})


if __name__ == "__main__":
    print("Servidor Flask corriendo en http://127.0.0.1:5000")
    print("Abre tu navegador en esa dirección para ver la página de bienvenida")
    app.run(debug=True)