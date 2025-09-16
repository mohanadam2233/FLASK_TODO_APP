from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Todo model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean, default=False)

# Home route
@app.route("/")
def index():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos, edit_id=None)

# Show edit input
@app.route("/edit/<int:todo_id>")
def edit(todo_id):
    todos = Todo.query.all()
    return render_template("index.html", todos=todos, edit_id=todo_id)

# Add new todo
@app.route("/add", methods=["POST"])
def add():
    title = request.form.get("title")
    if title:
        new_todo = Todo(title=title)
        db.session.add(new_todo)
        db.session.commit()
    return redirect(url_for("index"))

# Toggle complete/uncomplete
@app.route("/complete/<int:todo_id>")
def toggle_complete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        todo.complete = not todo.complete
        db.session.commit()
    return redirect(url_for("index"))

# Delete todo
@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
    return redirect(url_for("index"))

# Update todo
@app.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id):
    todo = Todo.query.get(todo_id)
    if todo:
        title = request.form.get("title")
        if title:
            todo.title = title
            db.session.commit()
    return redirect(url_for("index"))

# Cancel edit
@app.route("/cancel")
def cancel():
    return redirect(url_for("index"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
