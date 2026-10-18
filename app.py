from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone, timedelta, date


app = Flask(__name__)


app.config['SECRET_KEY'] = "the-secret"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, default="")
    priority = db.Column(db.String(20), default="Média")
    due_date = db.Column(db.String(10), default="")
    done = db.Column(db.Boolean, default=False, nullable=False)
    status = db.Column(db.String(20), default="A fazer", nullable=False)

    created_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    contact_id = db.Column(
        db.Integer,
        db.ForeignKey('contact.id'),
        nullable=True
    )

    contact = db.relationship('Contact', backref='tasks')


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(20))


with app.app_context():
    db.create_all()

    with db.engine.connect() as connection:
        result = connection.execute(db.text("PRAGMA table_info(task)"))
        columns = [row[1] for row in result]

        if "contact_id" not in columns:
            connection.execute(
                db.text(
                    "ALTER TABLE task ADD COLUMN contact_id INTEGER REFERENCES contact(id)"
                    )
                )
        connection.commit()

        if "status" not in columns:
            connection.execute(
                db.text(
                    "ALTER TABLE task ADD COLUMN status VARCHAR(20) DEFAULT 'A fazer'"
                )
            )
            connection.commit()
        
        connection.execute(
                db.text(
                    "UPDATE task SET status = 'Concluída' "
                    "WHERE done = 1 AND status = 'A fazer'"
                )
            )
        connection.commit()

        if "description" not in columns:
            connection.execute(
                db.text(
                    "ALTER TABLE task ADD COLUMN description TEXT"
                )
            )
            connection.commit()

        if "priority" not in columns:
            connection.execute(
                db.text(
                    "ALTER TABLE task ADD COLUMN priority VARCHAR(20) DEFAULT 'Média'"
                )
            )
            connection.commit()

        if "due_date" not in columns:
            connection.execute(
                db.text(
                    "ALTER TABLE task ADD COLUMN due_date VARCHAR(10)"
                )
            )
            connection.commit()


@app.get("/")
def home():
    tasks = Task.query.order_by(
        Task.done.asc(),
        Task.created_at.desc()
    ).all()

    hoje = datetime.now().date()
    alterou_status = False

    for task in tasks:
        if not task.due_date or task.done or task.status == "Concluída":
            continue

        try:
            prazo = datetime.strptime(task.due_date, "%d/%m/%Y").date()
        except ValueError:
            continue

        if prazo < hoje and task.status != "Atrasada":
            task.status = "Atrasada"
            alterou_status = True

    if alterou_status:
        db.session.commit()

    grupos = {
    "atrasadas": [],
    "hoje": [],
    "semana": [],
    "depois": [],
    "sem_prazo": [],
    "concluidas": [],
    }

    prazos = {}
    ordem_prioridade = {"Alta": 0, "Média": 1, "Baixa": 2}

    for task in tasks:
        try:
            prazo = (
                datetime.strptime(task.due_date, "%d/%m/%Y").date()
                if task.due_date else None
            )
        except ValueError:
            prazo = None

        prazos[task.id] = prazo

        if task.done or task.status == "Concluída":
            grupos["concluidas"].append(task)
        elif task.status == "Atrasada" or (prazo and prazo < hoje):
            grupos["atrasadas"].append(task)
        elif prazo is None:
            grupos["sem_prazo"].append(task)
        elif prazo == hoje:
            grupos["hoje"].append(task)
        elif prazo <= hoje + timedelta(days=7):
            grupos["semana"].append(task)
        else:
            grupos["depois"].append(task)

    for itens in grupos.values():
        itens.sort(key=lambda task: task.created_at, reverse=True)
        itens.sort(key=lambda task: ordem_prioridade.get(task.priority, 3))
        itens.sort(key=lambda task: prazos[task.id] or date.max)

    total = len(tasks)
    concluidas = len(grupos["concluidas"])

    resumo = {
        "total": total,
        "concluidas": concluidas,
        "atrasadas": len(grupos["atrasadas"]),
        "percentual": round(concluidas * 100 / total) if total else 0,
    }

    filtro = request.args.get("filtro", "todas")
    if filtro not in ("todas", "hoje", "semana", "atrasadas", "concluidas"):
        filtro = "todas"

    contacts = Contact.query.order_by(Contact.name).all()

    return render_template(
        "index.html",
        tasks=tasks,
        contacts=contacts,
        grupos=grupos,
        resumo=resumo,
        filtro=filtro,
        hoje=hoje
    )

@app.get("/contacts")
def contacts():
    contact_list = Contact.query.order_by(Contact.name).all()
    return render_template("contacts.html", contacts=contact_list)


@app.get("/ad_atv")
def ad_atv():
    contacts = Contact.query.order_by(Contact.name).all()
    return render_template("ad_atv.html", contacts=contacts)


@app.post("/contacts/add")
def add_contact():
    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    phone = request.form.get("phone", "").strip()

    if not name:
        flash("Informe o nome do contato.")
        return redirect(url_for("contacts"))

    db.session.add(
        Contact(
            name=name,
            email=email,
            phone=phone
        )
    )

    db.session.commit()

    flash("Contato adicionado.")

    return redirect(url_for("contacts"))


@app.post("/add")
def add():
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Média")
    due_date = request.form.get("due_date", "").strip()

    if due_date:
        try:
            due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%d/%m/%Y")
        except ValueError:
            flash("Prazo inválido.")
            return redirect(url_for("ad_atv"))

    contact_id = request.form.get("contact_id")

    if not title:
        flash("Informe o título da atividade.")
        return redirect(url_for("home"))

    contact = None

    if contact_id:
        contact = db.session.get(Contact, int(contact_id))

        if contact is None:
            flash("Contato responsável inválido.")
            return redirect(url_for("home"))

    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date,
        contact=contact
    )

    db.session.add(task)
    db.session.commit()

    flash("Atividade adicionada.")

    return redirect(url_for("home"))


@app.post("/delete/<int:task_id>")
def delete(task_id):
    task = Task.query.get_or_404(task_id)

    db.session.delete(task)
    db.session.commit()

    flash("Atividade deletada.")

    return redirect(url_for("home"))


@app.post("/toggle/<int:task_id>")
def toggle(task_id):
    task = Task.query.get_or_404(task_id)

    task.done = not task.done
 
    task.status = "Concluída" if task.done else "A fazer"

    db.session.commit()

    flash(
        "Marcado como concluído"
        if task.done
        else "Ativo"
    )

    return redirect(url_for("home"))


@app.post("/status/<int:task_id>")
def change_status(task_id):
    task = Task.query.get_or_404(task_id)

    status = request.form.get("status")

    if status in ["A fazer", "Fazendo", "Concluída", "Atrasada"]:
        task.status = status
        task.done = status == "Concluída"

        db.session.commit()

    return redirect(url_for("home"))

@app.post("/priority/<int:task_id>")
def change_priority(task_id):
    task = Task.query.get_or_404(task_id)

    priority = request.form.get("priority")

    if priority in ["Baixa", "Média", "Alta"]:
        task.priority = priority
        db.session.commit()

    return redirect(url_for("home"))

if __name__ == '__main__':
    app.run(debug=True)