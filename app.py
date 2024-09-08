from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

DATABASE = "todolist.db"
def init_sql_db():
    conn = sqlite3.connect(DATABASE)
    print("opened database successfully")
    conn.execute("CREATE TABLE IF NOT EXISTS tasks(id INTEGER PRIMARY KEY, task TEXT)")
    print("table created")
    conn.close()

init_sql_db()


@app.route("/", methods = ["GET", "POST"])
def index():
    task_list = []
    task_id = []
    task_name = request.args.get("task")
    print(task_id)
    if task_name and task_name.strip():
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task_name,))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    conn = sqlite3.connect(DATABASE);
    cursor = conn.cursor()
    cursor.execute("SELECT id, task FROM tasks")
    tasks = cursor.fetchall()
    for task in tasks:
        task_list.append(task)

    if request.method == "POST":
        task_id = request.form.getlist("taskID")
        print(task_id)
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        for id in task_id:
            cursor.execute("DELETE FROM tasks WHERE id = ?", (id))
        conn.commit()
        conn.close()
        return redirect(url_for("index"))

    return render_template("index.html", tasks = task_list)