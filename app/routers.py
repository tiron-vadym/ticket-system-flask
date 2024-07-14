from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from app import app, db
from app.models import User, Ticket, Role
from app.forms import LoginForm, RegistrationForm, TicketForm


@app.route("/")
@login_required
def index():
    if current_user.role == Role.ADMIN:
        tickets = Ticket.query.all()
    else:
        tickets = Ticket.query.filter_by(group=current_user.group).all()
    return render_template("index.html", title="Home", tickets=tickets)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, role=Role.ANALYST)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("index"))
    return render_template("register.html", title="Register", form=form)


@app.route("/ticket", methods=["GET", "POST"])
@login_required
def ticket():
    form = TicketForm()
    if form.validate_on_submit():
        ticket = Ticket(
            status=form.status.data,
            group=current_user.group,
            note=form.note.data,
        )
        if current_user.role == Role.MANAGER:
            ticket.user_id = current_user.id
        db.session.add(ticket)
        db.session.commit()
        flash("Your ticket is now live!")
        return redirect(url_for("index"))
    return render_template(
        "create_ticket.html",
        title="Create Ticket",
        form=form
    )


@app.route("/update_ticket/<int:id>", methods=["GET", "POST"])
@login_required
def update_ticket(id):
    ticket = Ticket.query.get_or_404(id)
    form = TicketForm(obj=ticket)
    if form.validate_on_submit():
        ticket.status = form.status.data
        ticket.note = form.note.data
        db.session.commit()
        flash("Ticket has been updated.")
        return redirect(url_for("index"))
    return render_template(
        "edit_ticket.html",
        title="Update Ticket",
        form=form
    )
