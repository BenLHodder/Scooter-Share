from flask import render_template, flash, url_for, redirect, session, request
from handler.scooter_socket import ScooterSocket
from handler.fault_log_socket import FaultLogSocket


def eng_dashboard_routes(app):
    """Routes for the engineer dashboard"""

    def check_engineer():
        """Check if the logged in user is a customer"""
        if not session.get("logged_in") or session.get("role") != "Engineer":
            flash("Please log in as an engineer first", "error")
            return redirect(url_for("login"))

    @app.route("/eng_dashboard")
    def eng_dashboard():
        # Check if the user is an engineer
        check = check_engineer()
        if check:
            return check  # Redirect to login if not engineer

        # Retrieve available scooters data
        scooter_socket = ScooterSocket()

        try:
            all_scooter_details = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html", scooters=[], funds=0.0)

        scooters = [
            {
                "make": scooter["make"],
                "colour": scooter["colour"],
                "latitude": scooter["latitude"],
                "longitude": scooter["longitude"],
                "power": scooter["batteryPercentage"],
                "status": scooter["status"],
            }
            for scooter in all_scooter_details
        ]

        # Render the engineer dashboard
        return render_template("eng_dashboard.html", scooters=scooters)

    @app.route("/eng-fault-log-requests")
    def eng_fault_log_requests():
        # Check if the user is an engineer
        check = check_engineer()
        if check:
            return check  # Redirect to login if not engineer

        # Retrieve all the fault log requests
        fault_log_socket = FaultLogSocket()
        # Retrieve all the scooters associated to each fault
        scooter_socket = ScooterSocket()
        combined_requests = []
        try:
            fault_log_requests = fault_log_socket.get_open_scooter_faults()
            for request in fault_log_requests:
                scooter_details = scooter_socket.get_scooter_details(
                    request["scooterID"]
                )
                if scooter_details:
                    combined_request = {
                        "faultID": request["faultID"],
                        "scooterID": request["scooterID"],
                        "make": scooter_details["make"],
                        "colour": scooter_details["colour"],
                        "latitude": scooter_details["latitude"],
                        "longitude": scooter_details["longitude"],
                        "power": scooter_details["batteryPercentage"],
                        "faultNotes": request["faultNotes"],
                        "status": request["status"],
                        "resolution": request.get(
                            "resolution", None
                        ),  # Handle resolution if it might not exist
                    }
                    combined_requests.append(combined_request)
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            combined_requests = []

        return render_template(
            "eng_fault_log_requests.html", requests=combined_requests
        )

    @app.route("/report-repair/<int:fault_id>", methods=["GET", "POST"])
    def report_repair(fault_id):
        # Check if the user is an engineer
        check = check_engineer()
        if check:
            return check  # Redirect to login if not engineer

        if request.method == "POST":
            resolution_notes = request.form.get("resolution_notes")
            fault_log_socket = FaultLogSocket()
            fault_log_socket.resolve_scooter_fault(fault_id, resolution_notes)
            flash(f"Repair for fault {fault_id} reported successfully.", "success")
            return redirect(url_for("eng_fault_log_requests"))

        # Render the repair report page with the fault ID
        return render_template("report_repair.html", fault_id=fault_id)

    @app.route("/find-scooter-location/<int:scooter_id>")
    def find_scooter_location(scooter_id):
        # Check if the user is an engineer
        check = check_engineer()
        if check:
            return check  # Redirect to login if not engineer

        scooter_socket = ScooterSocket()
        scooter_details = scooter_socket.get_scooter_details(scooter_id)

        # Extract the latitude and longitude
        latitude = scooter_details["latitude"]
        longitude = scooter_details["longitude"]

        return render_template(
            "scooter_location.html",
            latitude=latitude,
            longitude=longitude,
            scooter_id=scooter_id,
        )
