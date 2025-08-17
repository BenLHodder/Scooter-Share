from flask import render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from handler.customer_socket import CustomerSocket

def login_routes(app):
    """Routes for the login page"""

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            # Send login data to Master Pi
            customer_socket = CustomerSocket()
            try:
                response = customer_socket.login_customer(email)
            except ConnectionRefusedError:
                flash("Server connection issue. Please try again later.", "error")
                return redirect(url_for("login"))

            if response.get("message") == "User not found.":
                flash("Invalid email or password.", "error")
                return redirect(url_for("login"))

            if response.get("role") != "Admin":
                flash("Only admins can log in.", "error")
                return redirect(url_for("login"))
            
            if check_password_hash(response.get("password"), password):
                session["logged_in"] = True
                session["email"] = email
                session["first_name"] = customer_socket.retrieve_customer(email).get(
                    "firstName"
                )
                return redirect(url_for("home"))
            else:
                flash("Invalid email or password", "error")
                return redirect(url_for("login"))

        return render_template("login.html")
