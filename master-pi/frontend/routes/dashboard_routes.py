from datetime import datetime
import pytz
from flask import render_template, flash, redirect, url_for, session, request
from werkzeug.security import generate_password_hash
from handler.scooter_socket import ScooterSocket
from handler.booking_socket import BookingSocket
from handler.customer_socket import CustomerSocket
from handler.visualisation_handler import VisualisationHandler



def dashboard_routes(app):
    """Routes for the home/dashboard page"""    
    def is_logged_in():
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return False
        return True

    @app.route("/home", methods=["GET"])
    def home():
        # Check if the user is logged in
        if not is_logged_in():
            return redirect(url_for("login")) 
        
        # Render the dashboard page and pass scooters to the template
        return render_template("dashboard.html")

    @app.route("/logout", methods=["POST"])
    def logout():
        """Log the user out by clearing the session"""

        session.clear()
        flash("You have been logged out", "success")
        return redirect(url_for("login"))
    
    @app.route("/view-all-scooters", methods=["GET", "POST"])
    def view_all_scooters():
        # Check if the user is logged in
        if not is_logged_in():
            return redirect(url_for("login"))
        
        # Retrieve available scooters data
        scooter_socket = ScooterSocket()
        try:
            all_scooter_details = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")
        
        scooters = [
            {
                "make": scooter["make"],
                "colour": scooter["colour"],
                "latitude": scooter["latitude"],
                "longitude": scooter["longitude"],
                "cost": scooter["costMin"],
                "power": scooter["batteryPercentage"],
                "status": scooter["status"],
                "ipAddress": scooter["ipAddress"],
            }
            for scooter in all_scooter_details
        ]
        
        return render_template("view_all_scooters.html", scooters=scooters)
    
    
    @app.route("/view-all-customers", methods=["GET", "POST"])
    def view_all_customers():
        # Check if the user is logged in
        if not is_logged_in():
            return redirect(url_for("login"))
        
        customer_socket = CustomerSocket()
        try:
            all_customer_details = customer_socket.get_all_customers()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")
        
        customers = get_all_customers()
        
        return render_template("view_all_customers.html", customers=customers)
    
    @app.route("/update-customer-info", methods=["GET", "POST"])
    def update_customer_info():
        # Check if the user is logged in
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return redirect(url_for("login"))

        customer_socket = CustomerSocket()

        try:
            all_customers = customer_socket.get_all_customers()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")

        selected_customer = None
        if request.method == "POST":
            # Handle the form submission to update customer info
            updated_data = {
                "first_name": request.form.get("first_name"),
                "last_name": request.form.get("last_name"),
                "phone_no": request.form.get("phone_no"),
                "email": request.form.get("email"),
                "password": hash_password(request.form.get("password")),
                "funds": request.form.get("funds"),
                "role": request.form.get("role"),
            }
            
            try:
                response = customer_socket.update_customer(updated_data)
                if response['message'] == "User details updated successfully.":
                    flash("Customer information updated successfully!", "success")
                else:
                    flash("Error updating customer information: " + str(response), "error")
                return redirect(url_for("update_customer_info"))
            except Exception as e:
                flash("Error updating customer information: " + str(e), "error")
        elif request.method == "GET":
            if "customer_email" in request.args:
                try:
                    customer_email = request.args.get("customer_email")
                    selected_customer = customer_socket.retrieve_customer(customer_email)
                except Exception as e:
                    flash("Error retrieving customer information: " + str(e), "error")

        return render_template("update_customer_info.html", customers=all_customers, selected_customer=selected_customer)
    
    @app.route("/update-scooter-info", methods=["GET", "POST"])
    def update_scooter_info():
        # Check if the user is logged in
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return redirect(url_for("login"))

        scooter_socket = ScooterSocket()

        try:
            all_scooters = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")

        selected_scooter = None
        if request.method == "POST":
            # Handle the form submission to update scooter info
            updated_data = {
                "scooter_id": request.form.get("scooter_id"),
                "make": request.form.get("make"),
                "colour": request.form.get("colour"),
                "latitude": request.form.get("latitude"),
                "longitude": request.form.get("longitude"),
                "cost_min": request.form.get("cost_min"),
                "battery_percentage": request.form.get("battery_percentage"),
                "status": request.form.get("status"),
                "ip_address": request.form.get("ip_address"),
            }
            print(updated_data)
            try:
                response = scooter_socket.update_scooter(updated_data)
                
                if response['message'] == "Scooter details updated successfully.":
                    flash("Scooter information updated successfully!", "success")
                else:
                    flash("Error updating scooter information: " + str(response), "error")
                return redirect(url_for("update_scooter_info"))
            except Exception as e:
                flash("Error updating scooter information: " + str(e), "error")
        elif request.method == "GET":
            if "scooter_id" in request.args:
                try:
                    scooter_id = request.args.get("scooter_id")
                    selected_scooter= scooter_socket.get_scooter_details(scooter_id)
                except Exception as e:
                    flash("Error retrieving scooter information: " + str(e), "error")

        return render_template("update_scooter_info.html", scooters=all_scooters, selected_scooter=selected_scooter)
    
    @app.route("/report-scooter-fault", methods=["GET", "POST"])
    def report_scooter_fault():
        # Check if the user is logged in
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return redirect(url_for("login"))

        scooter_socket = ScooterSocket()

        try:
            all_scooters = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")

        selected_scooter = None
        if request.method == "POST":
            try:
                response = scooter_socket.add_scooter_fault_notes(request.form.get("scooter_id"), request.form.get("fault_notes"))
                
                if response['message'] == "Scooter fault updated successfully.":
                    flash("Scooter fault reported successfully!", "success")
                else:
                    flash("Error reporting scooter fault: " + str(response), "error")
                return redirect(url_for("report_scooter_fault"))
            except Exception as e:
                flash("Error reporting scooter fault: " + str(e), "error")
        elif request.method == "GET":
            if "scooter_id" in request.args:
                try:
                    scooter_id = request.args.get("scooter_id")
                    selected_scooter= scooter_socket.get_scooter_details(scooter_id)
                except Exception as e:
                    flash("Error retrieving scooter information: " + str(e), "error")

        return render_template("report_scooter_fault.html", scooters=all_scooters, selected_scooter=selected_scooter)
    
    @app.route("/view-scooter-booking-history", methods=["GET", "POST"])
    def view_scooter_booking_history():
        # Check if the user is logged in
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return redirect(url_for("login"))

        scooter_socket = ScooterSocket()
        booking_socket = BookingSocket()

        try:
            all_scooters = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")

        selected_scooter = None
        bookings = []
        if request.method == "POST":
            if "scooter_id" in request.form:
                try:
                    scooter_id = request.form.get("scooter_id")
                    selected_scooter= scooter_socket.get_scooter_details(scooter_id)
                except Exception as e:
                    flash("Error retrieving scooter information: " + str(e), "error")
        elif request.method == "GET":
            if "scooter_id" in request.args:
                try:
                    scooter_id = request.args.get("scooter_id")
                    selected_scooter= scooter_socket.get_scooter_details(scooter_id)
                   
                    bookings = get_all_scooters_bookings(booking_socket, scooter_id)
                    
                    if bookings is None:
                        bookings = []
                        
                except Exception as e:
                    flash("Error retrieving scooter information: " + str(e), "error")

        return render_template("view_scooter_booking_history.html", scooters=all_scooters, selected_scooter=selected_scooter, scooter_bookings=bookings)

    @app.route("/view-scooter-usage-history", methods=["GET", "POST"])
    def view_scooter_usage_history():
        # Check if the user is logged in
        if not session.get("logged_in"):
            flash("Please log in first", "error")
            return redirect(url_for("login"))

        scooter_socket = ScooterSocket()
        booking_socket = BookingSocket()

        try:
            all_scooters = scooter_socket.get_all_scooters()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")

        selected_scooter = None
        bookings = []
        if request.method == "POST":
            if "scooter_id" in request.form:
                try:
                    scooter_id = request.form.get("scooter_id")
                    selected_scooter= scooter_socket.get_scooter_details(scooter_id)
                except Exception as e:
                    flash("Error retrieving scooter information: " + str(e), "error")
        elif request.method == "GET":
            if "scooter_id" in request.args:
                try:
                    scooter_id = request.args.get("scooter_id")
                    selected_scooter= scooter_socket.get_scooter_details(scooter_id)
                    
                    bookings = get_all_scooters_bookings(booking_socket, scooter_id)
                    
                    if bookings is None:
                        bookings = []
                        
                except Exception as e:
                    flash("Error retrieving scooter information: " + str(e), "error")

        return render_template("view_scooter_usage_history.html", scooters=all_scooters, selected_scooter=selected_scooter, scooter_bookings=bookings)
    
    @app.route("/generate-scooter-usage-visualisation", methods=["GET"])
    def generate_scooter_usage_visualisation():
        selected_option = ""
        booking_socket = BookingSocket()
        scooter_socket = ScooterSocket()
        vis = VisualisationHandler()
        
        if request.method == "GET":
            if "choice" in request.args:
                try:
                    selected_option = request.args.get("choice")

                    # Generate data based on the selected option
                    scooter_ids = get_all_scooter_ids(scooter_socket)
                    bookings = []
                    for scooter_id in scooter_ids:
                        bookings += get_all_scooters_bookings(booking_socket, scooter_id)

                    # Generate the visualization based on user input
                    vis.generate_visualisation(selected_option, bookings)

                except Exception as e:
                    flash(f"Error information: {str(e)}", "error")
                    app.logger.error(f"Error in generate_scooter_usage_visualisation: {str(e)}")
                    return render_template("generate_scooter_usage_visualisation.html", selected_option=selected_option, options=["day", "week"]), 500

        return render_template("generate_scooter_usage_visualisation.html", selected_option=selected_option, options=["day", "week"])

    
    def get_all_scooters_bookings(booking_socket, scooter_id):
        all_scooter_bookings = booking_socket.get_all_bookings_for_scooter(scooter_id)
        bookings = [
            {
                "booking_id": booking["bookingID"],
                "email": booking["email"],
                "scooter_id": booking["scooterID"],
                "start_datetime": booking["startDateTime"],
                "end_datetime": booking["endDateTime"],
                "actual_start_datetime": booking["actualStartDateTime"],
                "actual_end_datetime": booking["actualEndDateTime"],
                "cost": booking["cost"],
                "deposit_cost": booking["depositCost"],
                "google_id": booking["googleID"],
                "status": booking["status"],
            }
            for booking in all_scooter_bookings.get("bookings", [])
        ]
        
        return bookings
    
    def get_all_scooter_ids(scooter_socket):
        all_scooters = scooter_socket.get_all_scooters()
        scooter_ids = [scooter["scooterID"] for scooter in all_scooters]
        return scooter_ids
    
    def get_all_customers():
        """
        Get all customer details from the server
        
        Returns:
            list: A list of dictionaries, each containing the details of a customer.
        """
        customer_socket = CustomerSocket()
        try:
            all_customer_details = customer_socket.get_all_customers()
        except ConnectionRefusedError:
            flash("Server connection error - Server may be down", "error")
            return render_template("dashboard.html")
        
        customers = [
            {
                "email": customer["email"],
                "firstName": customer["firstName"],
                "lastName": customer["lastName"],
                "phoneNo": customer["phoneNo"],
                "funds": customer["funds"],
                "role": customer["role"],
                "password": customer["password"],
            }
            for customer in all_customer_details
        ]
        
        return customers
        
def hash_password(password):
    return generate_password_hash(
                password, method="pbkdf2:sha256", salt_length=16
            )
        
