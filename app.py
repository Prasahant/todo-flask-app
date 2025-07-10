from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# SQLite database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(200), nullable=False)
    due = db.Column(db.String(20), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(20), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.task}>"

# Initialize the database
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    tasks = Task.query.order_by(Task.id.desc()).all()
    return render_template('index.html', tasks=tasks)

# Add a new task
@app.route('/add', methods=['POST'])
def add():
    task_text = request.form['task']
    due_date = request.form['due']
    category = request.form['category']
    priority = request.form['priority']

    new_task = Task(
        task=task_text,
        due=due_date,
        category=category,
        priority=priority
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('index'))

# Delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect(url_for('index'))

# Toggle task status
@app.route('/toggle/<int:id>')
def toggle(id):
    task = Task.query.get_or_404(id)
    task.done = not task.done
    db.session.commit()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
