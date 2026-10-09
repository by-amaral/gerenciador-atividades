from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone


app=Flask(__name__)


app.config['SECRET_KEY'] = "the-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))


with app.app_context():
    db.create_all()


@app.get("/")
def home():
    tasks = Task.query.order_by(Task.done.asc(), Task.created_at.desc()).all()
    return render_template("index.html", tasks=tasks)


@app.get("/contacts")
def contacts():
    contact_list = Contact.query.order_by(Contact.name).all()
    return render_template("contacts.html", contacts=contact_list)


@app.post("/contacts/add")
def add_contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    if not name:
        flash("Informe o nome do contato.")
        return redirect(url_for("contacts"))

    db.session.add(Contact(name=name, email=email, phone=phone))
    db.session.commit()
    flash("Contato adicionado.")
    return redirect(url_for("contacts"))

@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    if not title:
        flash("Please write something")
        return redirect(url_for("home"))
    db.session.add(Task(title=title))
    db.session.commit()
    flash("Atividade adicionada")
    return redirect(url_for("home"))


@app.post("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    flash("Atividade deletada ")
    return redirect(url_for("home"))


@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    task = Task.query.get_or_404(task_id)
    task.done = not task.done
    db.session.commit()
    flash("Marcado como concluído" if task.done else "Ativo")
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)