import os
import json
import hashlib
from io import BytesIO
import qrcode
from flask import render_template, request, flash, redirect, url_for, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from handler.user_socket import UserSocket
from utils.utils import get_local_ip


# Specify the directory to save QR codes
QR_CODE_DIR = "static/qr-codes"


def register_routes(app):
    """Routes for the registration page"""

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            phone_no = request.form["phone_no"]
            email = request.form["email"]
            password = request.form["password"]
            confirm_password = request.form["confirm_password"]

            # Check if passwords match
            if password != confirm_password:
                flash("Passwords do not match", "error")
                return redirect(url_for("register"))

            # Hash and salt the password
            hashed_password = generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=16
            )

            # Determine user role based on email domain
            if email.endswith("@engineer.com"):
                # If engineer, set role and hash email (username)
                role = "Engineer"
                # Use hashlib to hash the email without salt
                hashed_email = hashlib.sha256(email.encode()).hexdigest()
            else:
                role = "Customer"

            # Send registration data to Master Pi
            user_socket = UserSocket()
            try:
                if role == "Engineer":
                    response = user_socket.register_user(
                        hashed_email,
                        hashed_password,
                        first_name,
                        last_name,
                        phone_no,
                        1000000.00,
                        role,
                    )
                else:
                    response = user_socket.register_user(
                        email, hashed_password, first_name, last_name, phone_no, 0.00, role
                    )
            except ConnectionRefusedError:
                flash("Server connection issue. Please try again later.", "error")
                return redirect(url_for("register"))

            if response.get("message") == "Customer registered successfully.":
                flash(
                    f"User registered successfully:\nName: {first_name} {last_name}\nEmail: {email}",
                    "success",
                )
                return redirect(url_for("login"))
            else:
                flash("Registration failed", "error")
                return redirect(url_for("register"))

        return render_template("register.html")


def login_routes(app):
    """Routes for the login page"""

    @app.route("/", methods=["GET", "POST"])
    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            # Determine if the user is an engineer
            if email.endswith("@engineer.com"):
                # Hash both email and password for engineers
                hashed_email = hashlib.sha256(email.encode()).hexdigest()
            else:
                hashed_email = email  # Email stays unhashed for customers

            # Send login data to Master Pi
            user_socket = UserSocket()
            try:
                # Use hashed_email for engineers and plain email for customers
                response = user_socket.login_user(hashed_email)
            except ConnectionRefusedError:
                flash("Server connection issue. Please try again later.", "error")
                return redirect(url_for("login"))

            if response.get("message") == "User not found.":
                flash("Invalid email or password", "error")
                return redirect(url_for("login"))

            # Password Hash Check
            if response.get("role") == "Engineer":
                if check_password_hash(response.get("password"), password):
                    session["logged_in"] = True
                    session["email"] = (
                        hashed_email  # Store hashed email in session for engineer
                    )
                    session["first_name"] = user_socket.retrieve_user(hashed_email).get(
                        "firstName"
                    )
                    session["role"] = "Engineer"
                    session["password"] = response.get("password")
                    return redirect(url_for("eng_dashboard"))
                else:
                    flash("Invalid email or password", "error")
                    return redirect(url_for("login"))
            elif response.get("role") == "Admin":
                flash("Admin's are not authorised to log in on this site", "error")
                return redirect(url_for("login"))
            elif response.get("role") == "Customer":
                if check_password_hash(response.get("password"), password):
                    session["logged_in"] = True
                    session["email"] = email
                    session["first_name"] = user_socket.retrieve_user(email).get(
                        "firstName"
                    )
                    session["role"] = "Customer"
                    session["password"] = response.get("password")
                    return redirect(url_for("home"))
                else:
                    flash("Invalid email or password", "error")
                    return redirect(url_for("login"))
            else:
                flash("Invalid email or password", "error")
                return redirect(url_for("login"))

        return render_template("login.html")

    @app.route("/generate-qr", methods=["GET"])
    def generate_qr():
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return redirect(url_for("login"))

        username = session.get("email")
        password = session.get("password")
        role = session.get("role")

        # Create JSON data
        data = {
            "username": username,
            "password": password,
            "role": role,
        }

        # Generate QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(json.dumps(data))
        qr.make(fit=True)

        # Create an image from the QR Code instance
        img = qr.make_image(fill_color="black", back_color="white")

        # Ensure the QR code directory exists
        os.makedirs(QR_CODE_DIR, exist_ok=True)

        # Save the QR code image to a file
        filename = f"{username}.png"
        file_path = os.path.join(QR_CODE_DIR, filename)
        img.save(file_path)
        print(f"QR Code saved to: {file_path}")

        # Redirect to the display page with the filename
        return redirect(url_for("display_qr", filename=filename))

    @app.route("/display-qr/<filename>")
    def display_qr(filename):
        role = session.get("role")
        return render_template("display_qr.html", qr_code_filename=filename, role=role)

    @app.route("/forgot-password", methods=["GET", "POST"])
    def forgot_password():
        if request.method == "POST":
            email = request.form["email"]

            if email.endswith("@engineer.com"):
                # Use hashlib to hash the email without salt for engineer
                hashed_email = hashlib.sha256(email.encode()).hexdigest()
            else:
                # Use plain email for customer
                hashed_email = email

            user_socket = UserSocket()

            # Check if the email exists in the database
            user = user_socket.retrieve_user(hashed_email)
            if user.get("message") != "Customer not found.":
                # Get local IP address
                local_ip = get_local_ip()

                # Generate the reset link
                reset_link = f"http://{local_ip}:8000/reset-password/{hashed_email}"

                # Send the email
                user_socket.user_forgot_password(hashed_email, reset_link)

                flash("A reset link has been sent to your email.", "success")
                return redirect(url_for("login"))
            else:
                flash("Email does not exist. Please register a new account", "error")

        return render_template("forgot_password.html")

    @app.route("/reset-password/<email>", methods=["GET", "POST"])
    def reset_password(email):
        if request.method == "POST":
            new_password = request.form["new_password"]
            confirm_password = request.form["confirm_password"]

            # Check if passwords match
            if new_password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect(url_for("reset_password", email=email))

            # Hash and salt the new password
            hashed_password = generate_password_hash(
                new_password, method="pbkdf2:sha256", salt_length=16
            )

            # Update the password in the database
            user_socket = UserSocket()
            curr_user_details = user_socket.retrieve_user(email)

            # Fill in the details for update_user_details
            response = user_socket.update_user_details(
                email=curr_user_details["email"],
                password=hashed_password,  # use the new hashed password
                first_name=curr_user_details["firstName"],
                last_name=curr_user_details["lastName"],
                phone_no=curr_user_details["phoneNo"],
                funds=curr_user_details["funds"],
                role=curr_user_details["role"],
            )

            if response.get("message") == "User details updated successfully.":
                flash("Your password has been updated successfully.", "success")
                return redirect(url_for("login"))
            else:
                flash("Failed to update password.", "error")
                return redirect(url_for("reset_password", email=email))

        return render_template("reset_password.html", email=email)
