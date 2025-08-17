from flask import request, jsonify
from db_driver.booking_db_handler import BookingHandler

class BookingAPI:
    def __init__(self, app, db_info_file):
        self.booking_handler = BookingHandler(db_info_file)
        self._setup_routes(app)
    
    def _setup_routes(self, app):
        # Register routes
        app.add_url_rule('/booking/<int:booking_id>', 'get_booking', self.get_booking, methods=['GET'])
        app.add_url_rule('/booking/add_booking', 'add_booking', self.add_booking, methods=['POST'])
        app.add_url_rule('/booking/cancel_booking/<int:booking_id>', 'cancel_booking', self.cancel_booking, methods=['DELETE'])
        app.add_url_rule('/booking/start_booking', 'start_booking', self.start_booking, methods=['PUT'])
        app.add_url_rule('/booking/end_booking', 'end_booking', self.end_booking, methods=['PUT'])
        app.add_url_rule('/booking/get_bookings/<email>', 'get_bookings_for_customer', self.get_bookings_for_customer, methods=['GET'])
        app.add_url_rule('/booking/get_booked_scooters_times', 'get_booked_scooters_times', self.get_booked_scooters_times, methods=['GET'])
        app.add_url_rule('/booking/complete/<int:booking_id>', 'set_booking_complete', self.set_booking_complete, methods=['PUT'])
        app.add_url_rule('/booking/update_cost/<int:booking_id>', 'update_booking_cost', self.update_booking_cost, methods=['PUT'])
        app.add_url_rule('/booking/active', 'get_all_active_bookings', self.get_all_active_bookings, methods=['GET'])
        app.add_url_rule('/booking/<int:booking_id>/set_googleID', 'set_booking_googleID', self.set_booking_googleID, methods=['PUT'])
        app.add_url_rule('/booking/scooter/<int:scooter_id>', 'get_all_bookings_for_scooter', self.get_all_bookings_for_scooter, methods=['GET'])

    def get_booking(self, booking_id):
        """
        API endpoint to retrieve a booking's details by its ID.

        Args:
            booking_id (int): The ID of the booking.

        Returns:
            Response: JSON response containing booking details or a 404 error if not found.
        """
        result = self.booking_handler.get_booking(booking_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "Booking not found."}), 404

    def add_booking(self):
        data = request.json
        try:
            # Call the add_booking method and capture the returned booking ID
            booking_id = self.booking_handler.add_booking(
                email=data['email'],
                scooter_id=data['scooter_id'],
                start_datetime=data['start_datetime'],
                end_datetime=data['end_datetime'],
                deposit_cost=data['deposit_cost'],
                cost=data['cost']
            )
            
            # Return a JSON response including the booking ID
            return jsonify({
                "message": "Booking added successfully.",
                "booking_id": booking_id
            }), 201  # 201 status code indicates resource created

        except Exception as e:
            # Handle potential errors, returning an appropriate error response
            return jsonify({
                "message": f"Failed to add booking: {str(e)}"
            }), 400  # 400 status code for client error

    def cancel_booking(self, booking_id):
        try:
            self.booking_handler.cancel_booking(booking_id)
            return jsonify({"message": "Booking canceled successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def start_booking(self):
        data = request.json
        self.booking_handler.start_booking(
            booking_id=data['booking_id'],
            actual_start_datetime=data['actual_start_datetime']
        )
        return jsonify({"message": "Booking started successfully."})

    def end_booking(self):
        data = request.json
        self.booking_handler.end_booking(
            booking_id=data['booking_id'],
            actual_end_datetime=data['actual_end_datetime']
        )
        return jsonify({"message": "Booking ended successfully."})
    
    def get_bookings_for_customer(self, email):
        try:
            bookings = self.booking_handler.get_all_bookings_for_customer(email)
            return jsonify({"bookings": bookings})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def get_booked_scooters_times(self):
        try:
            booked_scooters = self.booking_handler.get_all_booked_scooters_and_times()
            return jsonify({"all_booked_scooters": booked_scooters})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    def set_booking_complete(self, booking_id):
        """
        API endpoint to set a booking's status to 'Complete'.

        Args:
            booking_id (int): The ID of the booking to complete.

        Returns:
            Response: JSON response indicating success or a 400 error.
        """
        try:
            self.booking_handler.set_booking_complete(booking_id)  # New function
            return jsonify({"message": f"Booking {booking_id} marked as complete."})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    def update_booking_cost(self, booking_id):
        """
        API endpoint to update the cost of a booking.

        Args:
            booking_id (int): The ID of the booking to update.

        Returns:
            Response: JSON response indicating success or failure.
        """
        data = request.json
        new_cost = data.get('new_cost')

        if new_cost is None:
            return jsonify({"error": "New cost is required."}), 400
        
        try:
            self.booking_handler.update_booking_cost(booking_id, new_cost)
            return jsonify({"message": f"Booking {booking_id} cost updated to {new_cost}."})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
        
    def get_all_active_bookings(self):
        """
        API endpoint to retrieve all active bookings.

        Returns:
            Response: JSON response containing a list of active bookings or a 400 error if something goes wrong.
        """
        try:
            active_bookings = self.booking_handler.get_all_active_bookings()
            return jsonify({"active_bookings": active_bookings})
        except Exception as e:
            return jsonify({"error": str(e)}), 400

    def set_booking_googleID(self, booking_id):
        """
        API endpoint to set the Google ID for a booking.

        Args:
            booking_id (int): The ID of the booking to be updated.

        Returns:
            Response: JSON response indicating success or failure.
        """
        google_id = request.json

        if google_id is None:
            return jsonify({"error": "Google ID is required."}), 400
        
        try:
            self.booking_handler.set_booking_googleID(booking_id, google_id)
            return jsonify({"message": f"Google ID for booking {booking_id} set successfully."})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
        
    def get_all_bookings_for_scooter(self, scooter_id):
        """
        API endpoint to retrieve all bookings for a specific scooter.

        Args:
            scooter_id (int): The ID of the scooter.

        Returns:
            Response: JSON response containing the list of bookings or a 404 error if not found.
        """
        try:
            bookings = self.booking_handler.get_all_bookings_for_scooter(scooter_id)
            if bookings:
                return jsonify({"bookings": bookings}), 200
            else:
                return jsonify({"message": "No bookings found for this scooter."}), 404
        except Exception as e:
            return jsonify({"error": str(e)}), 400