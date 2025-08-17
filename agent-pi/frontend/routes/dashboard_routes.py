from datetime import datetime
import pytz
from flask import render_template, flash, redirect, url_for, session, request
from handler.scooter_socket import ScooterSocket
from handler.user_socket import UserSocket
from handler.booking_socket import BookingSocket


def dashboard_routes(app):
    """Routes for the home/dashboard page"""

    def check_customer():
        """Check if the logged in user is a customer"""
        if not session.get("logged_in") or session.get("role") != "Customer":
            flash("Please log in as an customer first", "error")
            return redirect(url_for("login"))

    @app.route("/home", methods=["GET"])
    def home():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        # Retrieve available scooters data
        scooter_socket = ScooterSocket()

        try:
            all_scooter_details = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html", scooters=[], funds=0.0)

        # Retrieve customer information including funds
        user_socket = UserSocket()
        customer_info = user_socket.retrieve_user(session["email"])

        funds = customer_info.get("funds", 0.0)

        # Filter scooters to only include those with specified statuses
        available_statuses = ["Available", "Booked", "In Use"]
        scooters = [
            {
                "make": scooter["make"],
                "colour": scooter["colour"],
                "latitude": scooter["latitude"],
                "longitude": scooter["longitude"],
                "power": scooter["batteryPercentage"],
                "cost": scooter["costMin"],
            }
            for scooter in all_scooter_details
            if scooter["status"] in available_statuses
        ]

        # Render the dashboard page and pass scooters to the template
        return render_template("dashboard.html", scooters=scooters, funds=funds)

    @app.route("/logout", methods=["POST"])
    def logout():
        """Log the user out by clearing the session"""

        session.clear()
        flash("You have been logged out", "success")
        return redirect(url_for("login"))

    @app.route("/find-my-scooter", methods=["GET", "POST"])
    def find_my_scooter():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer
        
        def parse_datetime(date_str):
            if date_str is not None:
                naive_dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
                
                # Localize to GMT first
                gmt_timezone = pytz.timezone("GMT")
                gmt_aware_dt = gmt_timezone.localize(naive_dt)

                # Convert to AEDT timezone
                aedt_timezone = pytz.timezone("Australia/Sydney")
                aedt_aware_dt = gmt_aware_dt.astimezone(aedt_timezone)
            else:
                aedt_aware_dt = None
            return aedt_aware_dt

        booking_socket = BookingSocket()
        bookings_data = booking_socket.get_bookings_for_customer(session["email"])
        bookings = bookings_data["bookings"]

        # Initialise next_booking to None
        next_booking = None
        soonest_start_time = None

        # Convert to AEST
        aest_tz = pytz.timezone("Australia/Sydney")
        current_time_aest = datetime.now(aest_tz)

        # Iterate over all bookings to find the soonest active booking
        for booking in bookings:
            if booking["status"] == "Active":                
                booking_start_aest = parse_datetime(booking["startDateTime"])
                booking_end_aest = parse_datetime(booking["endDateTime"])

                # Check if the booking is still active
                if (booking_start_aest > current_time_aest or booking_end_aest > current_time_aest):
                    # Check if this is the soonest booking
                    if (soonest_start_time is None or booking_start_aest < soonest_start_time):
                        soonest_start_time = booking_start_aest
                        next_booking = booking

        if next_booking:
            next_booking["startDateTime"] = soonest_start_time.strftime(
                "%A, %d %B %Y %I:%M %p"
            )
            
            booking_end_time = parse_datetime(next_booking["endDateTime"])
            next_booking["endDateTime"] = booking_end_time.strftime(
                "%A, %d %B %Y %I:%M %p"
            )

            # Calculate time until start in minutes
            time_until_start = (
                soonest_start_time - current_time_aest
            ).total_seconds() / 60
            within_time = time_until_start <= 10

            if request.method == "POST":
                scooter_socket = ScooterSocket()
                scooter_location = scooter_socket.find_my_scooter(
                    next_booking["scooterID"]
                )

                # Check for the response success
                if scooter_location.get("success"):
                    flash("Scooter Located", "success")
                else:
                    flash("Failed to locate the scooter", "error")

                # Assuming scooter_location contains details like latitude/longitude
                return render_template(
                    "find_my_scooter.html",
                    booking=next_booking,
                    within_time=True,
                    location=scooter_location,
                )

            # If it's a GET request, show the booking details
            return render_template(
                "find_my_scooter.html", booking=next_booking, within_time=within_time
            )

        return render_template("find_my_scooter.html", booking=None, within_time=False)
