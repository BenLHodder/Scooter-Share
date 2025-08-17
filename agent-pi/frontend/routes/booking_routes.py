from datetime import datetime, timedelta
import pytz
from flask import render_template, request, flash, redirect, url_for, session
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from handler.booking_socket import BookingSocket
from handler.scooter_socket import ScooterSocket
from handler.user_socket import UserSocket
from handler.transaction_socket import TransactionSocket
from handler.fault_log_socket import FaultLogSocket


def booking_routes(app):
    """Routes for booking scooters"""

    def check_customer():
        """Check if the logged in user is a customer"""
        if not session.get("logged_in") or session.get("role") != "Customer":
            flash("Please log in as an customer first", "error")
            return redirect(url_for("login"))

    @app.route("/book-scooter", methods=["GET", "POST"])
    def book_scooter():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        # Retrieve customer information including funds
        user_socket = UserSocket()
        customer_info = user_socket.retrieve_user(session["email"])
        funds = customer_info.get("funds", 0.0)

        # Define scooters and their costs per minute
        booking_socket = BookingSocket()
        scooter_socket = ScooterSocket()
        all_scooter_bookings = booking_socket.get_all_booked_scooter_times()

        available_scooter_ids = [
            scooter["scooterID"]
            for scooter in all_scooter_bookings["all_booked_scooters"]
        ]

        available_scooter_details = {}
        for scooter_id in available_scooter_ids:
            details = scooter_socket.get_scooter_details(scooter_id)
            if details["status"] == "Available" or details["status"] == "In Use" or details["status"] == "Booked":
                available_scooter_details[scooter_id] = details

        scooters = {}
        for id, details in available_scooter_details.items():
            name = f"Scooter {id}"
            cost = details["costMin"]
            scooters[name] = cost
            

        for booking in all_scooter_bookings["all_booked_scooters"]:
            booking["startDateTime"] = datetime.strptime(
                booking["startDateTime"], "%a, %d %b %Y %H:%M:%S GMT"
            ).isoformat()
            booking["endDateTime"] = datetime.strptime(
                booking["endDateTime"], "%a, %d %b %Y %H:%M:%S GMT"
            ).isoformat()

        if request.method == "POST":
            # Retrieve form data
            selected_scooter = request.form["scooter"]
            start_date = request.form["start_date"]
            start_time = request.form["start_time"]
            end_date = request.form.get("end_date")
            end_time = request.form.get("end_time")
            deposit_cost = float(request.form.get("deposit"))
            cost = float(request.form.get("cost"))

            # Check if customer has enough funds
            if cost > funds:
                flash(
                    "You do not have the necessary funds to make this booking.",
                    "error",
                )
                return redirect(url_for("book_scooter"))

            # Extract scooter ID
            scooter_id = extract_scooter_id(selected_scooter)

            # Combine date and time for start and end times
            start_dt = datetime.strptime(f"{start_date} {start_time}", "%Y-%m-%d %H:%M")
            if end_date and end_time:
                end_dt = datetime.strptime(f"{end_date} {end_time}", "%Y-%m-%d %H:%M")
            else:
                # Default end time is 10 minutes after the start time
                end_dt = start_dt + timedelta(minutes=10)

            # Validate that the start time is not in the past
            if start_dt < datetime.now():
                flash("Start time cannot be in the past.", "error")
                return redirect(url_for("book_scooter"))

            # Validate that the end time is at least 10 minutes after start time
            if end_dt < start_dt + timedelta(minutes=10):
                flash("End time must be at least 10 minutes after start time.", "error")
                return redirect(url_for("book_scooter"))

            # Validate that the booking does not already exist for that scooter
            for booking in all_scooter_bookings["all_booked_scooters"]:
                if booking["scooterID"] == scooter_id:
                    booked_start = datetime.strptime(
                        booking["startDateTime"], "%Y-%m-%dT%H:%M:%S"
                    )
                    booked_end = datetime.strptime(
                        booking["endDateTime"], "%Y-%m-%dT%H:%M:%S"
                    )
                    # Check if the new booking time overlaps with any existing booking
                    if start_dt < booked_end and end_dt > booked_start:
                        # Check if the existing booking status is "Complete"
                        if booking["status"] == "Active":
                            flash(
                                f"There is already a complete booking for scooter {scooter_id} between {booked_start} and {booked_end}.",
                                "error",
                            )
                            return redirect(url_for("book_scooter"))

            # Reformat dates
            start_dt_str = reformat_date(start_dt.strftime("%Y-%m-%d %H:%M:%S"))
            end_dt_str = reformat_date(end_dt.strftime("%Y-%m-%d %H:%M:%S"))

            booking_response = booking_socket.add_booking(
                session["email"],
                scooter_id,
                start_dt_str,
                end_dt_str,
                deposit_cost,
                cost,
            )

            if booking_response.get("message") == "Booking added successfully.":
                # Save most recent booking ID
                session["booking_id"] = booking_response.get("booking_id")

                # Deduct the deposit from customer's funds
                user_socket.update_customer_funds(
                    session["email"], funds - deposit_cost
                )

                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                transaction_socket = TransactionSocket()
                transaction_socket.add_new_transaction(
                    session["email"], -deposit_cost, current_datetime
                )

                # Prepare data for confirmation page
                confirmation_data = {
                    "scooter": selected_scooter,
                    "start_time": start_dt,
                    "end_time": end_dt,
                    "cost": cost,
                    "deposit": deposit_cost,
                }

                return redirect(url_for("booking_confirmation", **confirmation_data))

            flash("Booking Failed - Server Error", "error")
            return redirect(url_for("book_scooter"))

        # If GET request, render the booking page with the list of scooters and their costs
        return render_template(
            "book_scooter.html",
            scooters=scooters,
            booked_scooters=all_scooter_bookings["all_booked_scooters"],
        )

    @app.route("/view-bookings", methods=["GET", "POST"])
    def view_bookings():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        booking_socket = BookingSocket()

        all_customer_bookings = booking_socket.get_bookings_for_customer(
            session["email"]
        )
        bookings = all_customer_bookings["bookings"]

        # Get the current date and time in AEDT
        now_aedt = datetime.now(pytz.timezone("Australia/Sydney"))

        # Function to parse date strings and return timezone-aware datetime objects
        def parse_datetime(date_str):
            naive_dt = datetime.strptime(date_str, "%a, %d %b %Y %H:%M:%S GMT")
            
            # Localize to GMT first
            gmt_timezone = pytz.timezone("GMT")
            gmt_aware_dt = gmt_timezone.localize(naive_dt)

            # Convert to AEDT timezone
            aedt_timezone = pytz.timezone("Australia/Sydney")
            aedt_aware_dt = gmt_aware_dt.astimezone(aedt_timezone)
            
            return aedt_aware_dt

        # Filter future bookings with "Active" status
        future_bookings = [
            booking
            for booking in bookings
            if parse_datetime(booking["endDateTime"]) > now_aedt
            and booking["status"] == "Active"
        ]

        # Check which bookings can be cancelled
        for booking in future_bookings:
            start_dt = parse_datetime(booking["startDateTime"])
            booking["can_cancel"] = (
                start_dt > now_aedt
            )  # Can only cancel if start time hasn't passed

        if request.method == "POST":
            booking_id = int(request.form["bookingID"])
            google_id = None
            # Ensure booking can be canceled
            for booking in future_bookings:
                if booking["bookingID"] == booking_id and not booking["can_cancel"]:
                    flash(
                        "Cannot cancel this booking, as the start time has passed.",
                        "error",
                    )
                    return redirect(url_for("view_bookings"))

                if booking["bookingID"] == booking_id:
                    # Proceed with booking cancellation
                    google_id = booking.get("googleID")

                    response = booking_socket.cancel_booking(booking_id)

                    if google_id:
                        try:
                            # Initialise the Google Calendar service
                            scopes = "https://www.googleapis.com/auth/calendar"
                            store = file.Storage("frontend/resources/token.json")
                            creds = store.get()

                            if not creds or creds.invalid:
                                flow = client.flow_from_clientsecrets(
                                    "frontend/resources/credentials.json", scopes
                                )
                                creds = tools.run_flow(flow, store)

                            service = build(
                                "calendar", "v3", http=creds.authorize(Http())
                            )

                            # Call the delete method
                            service.events().delete(
                                calendarId="primary", eventId=google_id
                            ).execute()
                            flash(
                                f"Booking ID {booking_id} successfully cancelled and deleted from Google Calendar."
                            )
                        except Exception as e:
                            flash(
                                f"Failed to remove event from Google Calendar: {str(e)}",
                                "error",
                            )
                            return redirect(url_for("view_bookings"))

                    if response.get("message") == "Booking canceled successfully.":
                        # Refund logic
                        deposit_amount = booking.get(
                            "depositCost", 0.0
                        )  # Adjust according to your booking structure
                        user_socket = UserSocket()
                        customer_info = user_socket.retrieve_user(session["email"])
                        current_funds = customer_info.get("funds", 0.0)
                        new_funds = current_funds + deposit_amount

                        response = user_socket.update_customer_funds(
                            session["email"], new_funds
                        )

                        # Log the transaction for the refund
                        transaction_socket = TransactionSocket()
                        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        transaction_socket.add_new_transaction(
                            session["email"], deposit_amount, current_datetime
                        )
                        return redirect(url_for("view_bookings"))

                    flash("Booking cancel failed - Server Error", "error")
                    return redirect(url_for("view_bookings"))

        # Process booking duration for future bookings
        for booking in future_bookings:
            # Convert the times to AEDT
            start_dt = parse_datetime(booking["startDateTime"])
            end_dt = parse_datetime(booking["endDateTime"])
            
            # Format the AEDT times back into strings in the desired format
            booking["startDateTime"] = start_dt.strftime("%a, %d %b %Y %H:%M:%S")
            booking["endDateTime"] = end_dt.strftime("%a, %d %b %Y %H:%M:%S")
            
            # Calculate booking duration in minutes, rounded to 2 decimal places
            booking["duration"] = round((end_dt - start_dt).total_seconds() / 60, 2)

        return render_template("view_bookings.html", bookings=future_bookings)

    @app.route("/booking-confirmation")
    def booking_confirmation():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        scooter = request.args.get("scooter")
        start_time = request.args.get("start_time")
        end_time = request.args.get("end_time")
        cost = request.args.get("cost")
        deposit = request.args.get("deposit")

        return render_template(
            "booking_confirmation.html",
            scooter=scooter,
            start_time=start_time,
            end_time=end_time,
            cost=cost,
            deposit=deposit,
        )

    @app.route("/add-to-calendar", methods=["POST"])
    def add_to_calendar():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        scopes = "https://www.googleapis.com/auth/calendar"
        store = file.Storage("frontend/resources/token.json")
        creds = store.get()

        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(
                "frontend/resources/credentials.json", scopes
            )
            creds = tools.run_flow(flow, store)

        service = build("calendar", "v3", http=creds.authorize(Http()))

        scooter = request.form["scooter"]
        start_time = request.form["start_time"]
        end_time = request.form["end_time"]

        # Parse the existing time strings
        start_dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S")

        # Format to ISO 8601
        start_time_iso = start_dt.strftime("%Y-%m-%dT%H:%M:%S+11:00")
        end_time_iso = end_dt.strftime("%Y-%m-%dT%H:%M:%S+11:00")

        # Prepare the event data
        event = {
            "summary": f"Scooter Booking: {scooter}",
            "description": "Scooter booking confirmation",
            "start": {
                "dateTime": start_time_iso,
                "timeZone": "Australia/Sydney",
            },
            "end": {
                "dateTime": end_time_iso,
                "timeZone": "Australia/Sydney",
            },
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 60},
                    {"method": "popup", "minutes": 10},
                ],
            },
        }

        # Insert the event into Google Calendar
        try:
            event_result = (
                service.events().insert(calendarId="primary", body=event).execute()
            )
            booking_id = session["booking_id"]
            event_id = event_result["id"]
            booking_socket = BookingSocket()
            response = booking_socket.set_booking_google_id(booking_id, event_id)

            if (
                response.get("message")
                == f"Google ID for booking {booking_id} set successfully."
            ):
                flash("Event added to Google Calendar!", "success")
                return redirect(url_for("home"))
            elif response.get("error") == "Google ID is required.":
                flash(
                    "Failed to send Google ID to server - Google Event ID missing",
                    "error",
                )
                return redirect(
                    url_for(
                        "booking_confirmation",
                        scooter=scooter,
                        start_time=start_time,
                        end_time=end_time,
                        cost=request.form["cost"],
                        deposit=request.form["deposit"],
                    )
                )
            elif response.get("error") == "Booking not found.":
                flash(
                    "Booking does not exist in Server - Failed to update with Google Event IT",
                    "error",
                )
                return redirect(
                    url_for(
                        "booking_confirmation",
                        scooter=scooter,
                        start_time=start_time,
                        end_time=end_time,
                        cost=request.form["cost"],
                        deposit=request.form["deposit"],
                    )
                )
            else:
                flash(
                    "Server Error - Try again later",
                    "error",
                )
        except Exception as e:
            flash(f"Error adding event: {str(e)}", "error")

        return redirect(
            url_for(
                "booking_confirmation",
                scooter=scooter,
                start_time=start_time,
                end_time=end_time,
                cost=request.form["cost"],
                deposit=request.form["deposit"],
            )
        )

    @app.route("/top-up", methods=["GET", "POST"])
    def top_up():
        """Top-up page for customers to add funds to their account"""
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        if request.method == "POST":
            # Retrieve the amount to top up from the form
            try:
                amount = float(request.form["amount"])
                if amount <= 0:
                    flash("Please enter a valid amount.", "error")
                    return redirect(url_for("top_up"))

                # Update the customer's funds using the socket
                user_socket = UserSocket()
                customer_info = user_socket.retrieve_user(session["email"])
                current_funds = customer_info.get("funds", 0.0)
                new_funds = current_funds + amount

                response = user_socket.update_customer_funds(
                    session["email"], new_funds
                )

                socket_transaction = TransactionSocket()

                if response.get("message") == "Customer funds updated successfully.":
                    # Get the current date and time and format it as a string
                    current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Add a transaction for the topup
                    socket_transaction.add_new_transaction(
                        session["email"],
                        amount,
                        current_datetime,
                    )
                    return redirect(url_for("home"))

                flash("Top-up failed - Server Error", "error")
                return redirect(url_for("top_up"))
            except ValueError:
                flash("Invalid amount. Please enter a numeric value.", "error")
                return redirect(url_for("top_up"))

        # Render the top-up page if it's a GET request
        return render_template("top_up.html")

    @app.route("/transaction-history", methods=["GET"])
    def transaction_history():
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        transaction_socket = TransactionSocket()
        response = transaction_socket.get_all_customer_transactions(session["email"])

        transactions = response.get("transactions", [])

        # Define the time zones
        gmt_tz = pytz.timezone("GMT")
        aest_tz = pytz.timezone("Australia/Sydney")  # AEST is UTC+10

        # Format the transaction dates
        for transaction in transactions:
            # Parse the datetime in GMT
            datetime_obj = datetime.strptime(
                transaction["datetime"], "%a, %d %b %Y %H:%M:%S GMT"
            )
            # Localize to GMT
            gmt_datetime = gmt_tz.localize(datetime_obj)
            # Convert to AEST
            aest_datetime = gmt_datetime.astimezone(aest_tz)

            # Format the datetime for display
            transaction["datetime"] = aest_datetime.strftime("%a, %d %b %Y %H:%M:%S")
            transaction["absAmount"] = abs(transaction["transactionAmount"])

        return render_template("transaction_history.html", transactions=transactions)

    @app.route("/report-fault", methods=["GET", "POST"])
    def report_fault():
        """Page for customers to report faults with a scooter"""
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        scooter_socket = ScooterSocket()
        fault_log_socket = FaultLogSocket()
        all_scooter_details = scooter_socket.get_all_scooters()
        
        # Filter scooters based on status
        allowed_statuses = {"Available", "In Use", "Booked"}
        filtered_scooters = [
            scooter for scooter in all_scooter_details
            if scooter['status'] in allowed_statuses
        ]

        if request.method == "POST":
            selected_scooter_id = request.form["scooter_id"]
            fault_notes = request.form["fault_notes"]

            # Send fault notes to the database
            response = fault_log_socket.add_or_update_scooter_fault(
                selected_scooter_id, fault_notes
            )

            if response.get("message") == "Scooter fault updated successfully.":
                flash("Scooter Fault Reported Successfully")
                return redirect(url_for("home"))

            flash("Failed to report fault - Server Error", "error")
            return redirect(url_for("report_fault"))

        return render_template("report_fault.html", scooters=filtered_scooters)

    @app.route("/view-usage-history", methods=["GET"])
    def view_usage_history():
        """Displays the scooter usage history for the logged-in user"""
        # Check if the user is an customer
        check = check_customer()
        if check:
            return check  # Redirect to login if not customer

        # Retrieve usage history from the socket or database for this user
        booking_socket = BookingSocket()
        all_customer_bookings = booking_socket.get_bookings_for_customer(
            session["email"]
        )
        bookings = all_customer_bookings["bookings"]

        # Get the current date and time in AEST
        now_aest = datetime.now(pytz.timezone("Australia/Sydney"))

        # Function to parse date strings and return timezone-aware datetime objects
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

        # Filter past bookings with status "Complete" or "Cancelled"
        past_bookings = [
            booking
            for booking in bookings
            if (
                (end_dt := parse_datetime(booking["endDateTime"])) is not None and end_dt < now_aest
            ) or (
                (actual_end_dt := parse_datetime(booking["actualEndDateTime"])) is not None and actual_end_dt < now_aest
            ) or booking["status"] in ["Complete", "Cancelled"]
]

        # Process booking duration for past bookings
        for booking in past_bookings:
            start_dt = parse_datetime(booking["startDateTime"])
            end_dt = (
                parse_datetime(booking["endDateTime"])
                if booking["endDateTime"]
                else None
            )
            actual_start_dt = (
                parse_datetime(booking["actualStartDateTime"])
                if booking["actualStartDateTime"]
                else None
            )
            actual_end_dt = (
                parse_datetime(booking["actualEndDateTime"])
                if booking["actualEndDateTime"]
                else None
            )

            booking["startDateTime"] = start_dt.strftime("%a, %d %b %Y %H:%M:%S")
            booking["endDateTime"] = (
                end_dt.strftime("%a, %d %b %Y %H:%M:%S") if end_dt else "N/A"
            )

            # Add actual start and end times
            booking["actualStartDateTime"] = (
                actual_start_dt.strftime("%a, %d %b %Y %H:%M:%S")
                if actual_start_dt
                else "N/A"
            )
            booking["actualEndDateTime"] = (
                actual_end_dt.strftime("%a, %d %b %Y %H:%M:%S")
                if actual_end_dt
                else "N/A"
            )

            if end_dt:
                booking["duration"] = round((end_dt - start_dt).total_seconds() / 60, 2)

        # Render the usage history page
        return render_template("view_usage_history.html", history=past_bookings)


def reformat_date(date_str):
    """Reformat date to AEST for database insertion."""
    
    # Parse the input date string in the format "YYYY-MM-DD HH:MM:SS"
    dt_object = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")

    # Convert to AEST
    aest_timezone = pytz.timezone("Australia/Sydney")
    # dt_aest = dt_gmt.astimezone(aest_timezone)
    dt_aest = aest_timezone.localize(dt_object)

    # Return the datetime object as a string in ISO format for JSON serialization
    return dt_aest.isoformat()


def extract_scooter_id(scooter_str):
    """Extract the scooter ID from the string of the scooter"""

    # Extract the integer part from the string
    return int(scooter_str.split()[1])
