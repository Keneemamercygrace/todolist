from flask import Flask, redirect, render_template, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired, URL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keneema'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///To-do-list.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
Bootstrap(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(80), unique=True, nullable=False)
    Description = db.Column(db.String(120), nullable=False)
    Date = db.Column(db.String(120), nullable=False)
    Time = db.Column(db.String(120), nullable=False)
    Completed = db.Column(db.String(120), nullable=False)


class Todo_list(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    date = StringField("Date to be completed(dd/mm/yy)", validators=[DataRequired()])
    Time = StringField("Time to be completed", validators=[DataRequired()])
    completed = SelectField("Completed status", choices=['✗', '✔️'])
    submit = SubmitField("Submit")


db.create_all()


@app.route("/")
def Home():
    return render_template('index.html')


@app.route("/todo", methods=["GET", "POST"])
def todo():
    form = Todo_list()
    if form.validate_on_submit():
        data = form.data
        print("we did it")
        new_todo = Todo(
            Title=data['title'],
            Description=data['description'],
            Date=data['date'],
            Time=data['Time'],
            Completed=data['completed']
        )
        db.session.add(new_todo)
        db.session.commit()
        return redirect(url_for("my_to_dos"))
    return render_template("mytodo.html", form=form)


@app.route("/mytodos")
def my_to_dos():
    my_todos = Todo.query.all()
    return render_template("todolist.html", todos=my_todos)


@app.route("/completed")
def completed():
    todo_list = Todo.query.all()
    return render_template("completed.html", completed=todo_list)


@app.route("/edit/", methods=["GET", "POST"])
def edit():
    form = Todo_list()
    item_id = request.args.get("id")
    item = Todo.query.get(item_id)
    if form.validate_on_submit():
        # item.Title = form.title.data
        # item.Description = form.description.data
        item.Date = form.date.data
        item.Time = form.Time.data
        item.Completed = form.completed.data
        db.session.commit()
        return redirect(url_for('my_to_dos'))
    return render_template("edit.html", to=item, form=form)


if __name__ == '__main__':
    app.run(debug=True)
