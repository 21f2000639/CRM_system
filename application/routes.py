from flask import Blueprint, app, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from application.models import db, User, Admin, Ticket
import random
import json
import re

routes = Blueprint("routes", __name__)

EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

@app.route("/health")
def health():
    print("HEALTH ROUTE HIT")
    return "OK"


@routes.route("/")
def entry():
    
    
    return render_template("entry.html")


# =========================================================
# USER REGISTER
# =========================================================

@routes.route("/register", methods=["GET", "POST"])
def register():

    error = None

    if request.method == "POST":

        name = request.form.get("name").strip()
        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        if not re.match(EMAIL_REGEX, email):

            error = "Enter a valid email address"

            return render_template(
                "register.html",
                error=error
            )

        if len(password) < 6:

            error = "Password must be at least 6 characters"

            return render_template(
                "register.html",
                error=error
            )

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:

            error = "Email already registered"

            return render_template(
                "register.html",
                error=error
            )

        user = User(
            name=name,
            email=email,
            password=generate_password_hash(password)
        )

        db.session.add(user)

        db.session.commit()

        return redirect(url_for("routes.user_login"))

    return render_template(
        "register.html",
        error=error
    )


# =========================================================
# USER LOGIN
# =========================================================

@routes.route("/login", methods=["GET", "POST"])
def user_login():

    error = None

    if request.method == "POST":

        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        user = User.query.filter_by(email=email).first()

        if not user:

            error = "User does not exist"

            return render_template(
                "login.html",
                error=error
            )

        if not check_password_hash(user.password, password):

            error = "Incorrect password"

            return render_template(
                "login.html",
                error=error
            )

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["user_email"] = user.email

        return redirect(url_for("routes.home"))

    return render_template(
        "login.html",
        error=error
    )


# =========================================================
# USER HOME DASHBOARD
# =========================================================

@routes.route("/home")
def home():

    if "user_id" not in session:

        return redirect(url_for("routes.user_login"))

    tickets = Ticket.query.filter_by(
        user_id=session["user_id"]
    ).order_by(Ticket.created_at.desc()).all()

    tickets_data = []

    for ticket in tickets:

        tickets_data.append({
            "id": ticket.id,
            "ticket_id": ticket.ticket_id,
            "title": ticket.title,
            "description": ticket.description,
            "status": str(ticket.status),
            "priority": str(ticket.priority),
            "created_at": ticket.created_at.strftime("%d %b %Y %I:%M %p")
        })

    return render_template(
        "home.html",
        tickets_data=json.dumps(tickets_data),
        user_name=session["user_name"]
    )


# =========================================================
# CREATE TICKET
# =========================================================

@routes.route("/create-ticket", methods=["POST"])
def create_ticket():

    if "user_id" not in session:

        return redirect(url_for("routes.user_login"))

    title = request.form.get("title")
    description = request.form.get("description")
    priority = request.form.get("priority")

    ticket = Ticket(
        ticket_id=f"TICK{random.randint(1000,9999)}",
        title=title,
        description=description,
        priority=priority,
        user_id=session["user_id"]
    )

    db.session.add(ticket)

    db.session.commit()

    return redirect(url_for("routes.home"))


# =========================================================
# UPDATE TICKET
# =========================================================

@routes.route("/update-ticket/<int:id>", methods=["POST"])
def update_ticket(id):

    if "user_id" not in session:

        return {"error": "Unauthorized"}, 401

    ticket = Ticket.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not ticket:

        return {"error": "Ticket not found"}, 404

    data = request.get_json()

    ticket.title = data.get("title", ticket.title)
    ticket.description = data.get("description", ticket.description)
    ticket.priority = data.get("priority", ticket.priority)

    db.session.commit()

    return {"status": "success", "message": "Ticket updated successfully"}


# =========================================================
# VIEW TICKET
# =========================================================

@routes.route("/view-ticket/<int:id>")
def view_ticket(id):

    if "user_id" not in session:

        return redirect(url_for("routes.user_login"))

    ticket = Ticket.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not ticket:

        return redirect(url_for("routes.home"))

    return render_template(
        "view_ticket.html",
        ticket=ticket
    )


# =========================================================
# EDIT TICKET
# =========================================================

@routes.route("/edit-ticket/<int:id>", methods=["GET", "POST"])
def edit_ticket(id):

    if "user_id" not in session:

        return redirect(url_for("routes.user_login"))

    ticket = Ticket.query.filter_by(
        id=id,
        user_id=session["user_id"]
    ).first()

    if not ticket:

        return redirect(url_for("routes.home"))

    if request.method == "POST":

        ticket.title = request.form.get("title")
        ticket.description = request.form.get("description")
        ticket.priority = request.form.get("priority")

        db.session.commit()

        return redirect(url_for("routes.home"))

    return render_template(
        "edit_ticket.html",
        ticket=ticket
    )


# =========================================================
# USER LOGOUT
# =========================================================

@routes.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("routes.entry"))


# =========================================================
# ADMIN LOGIN
# =========================================================

@routes.route("/admin/login", methods=["GET", "POST"])
def admin_login():

    error = None

    if request.method == "POST":

        email = request.form.get("email").strip()
        password = request.form.get("password").strip()

        admin = Admin.query.filter_by(email=email).first()

        if not admin:

            error = "Admin does not exist"

            return render_template(
                "admin_login.html",
                error=error
            )

        if not check_password_hash(admin.password, password):

            error = "Incorrect password"

            return render_template(
                "admin_login.html",
                error=error
            )

        session["admin_id"] = admin.id
        session["admin_name"] = admin.name

        return redirect(url_for("routes.admin_dashboard"))

    return render_template(
        "admin_login.html",
        error=error
    )


# =========================================================
# ADMIN DASHBOARD
# =========================================================

@routes.route("/admin/dashboard")
def admin_dashboard():

    if "admin_id" not in session:

        return redirect(url_for("routes.admin_login"))

    tickets = Ticket.query.all()

    tickets_data = []

    for ticket in tickets:

        tickets_data.append({
            "id": ticket.id,
            "ticket_id": ticket.ticket_id,
            "title": ticket.title,
            "description": ticket.description,
            "status": str(ticket.status),
            "priority": str(ticket.priority),
            "created_at": ticket.created_at.strftime("%d %b %Y %I:%M %p"),
            "user_name": ticket.user.name,
            "user_email": ticket.user.email
        })

    return render_template(
        "admin_dashboard.html",
        tickets_data=json.dumps(tickets_data)
    )


# =========================================================
# UPDATE STATUS
# =========================================================

@routes.route("/admin/update-status/<int:id>", methods=["POST"])
def update_ticket_status(id):

    if "admin_id" not in session:

        return redirect(url_for("routes.admin_login"))

    ticket = Ticket.query.get_or_404(id)

    new_status = request.form.get("status")

    valid_statuses = [
        "Open",
        "In Progress",
        "Closed"
    ]

    if new_status in valid_statuses:

        ticket.status = new_status

        db.session.commit()

    return redirect(url_for("routes.admin_dashboard"))


# =========================================================
# ADMIN LOGOUT
# =========================================================

@routes.route("/admin/logout")
def admin_logout():

    session.clear()

    return redirect(url_for("routes.admin_login"))