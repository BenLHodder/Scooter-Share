from flask import request, jsonify
from db_driver.scooter_db_handler import ScooterHandler

class ScooterAPI:
    def __init__(self, app, db_info_file):
        self.scooter_handler = ScooterHandler(db_info_file)
        self._setup_routes(app)
        
    def _setup_routes(self, app):
        # Register routes
        app.add_url_rule('/scooter/<int:scooter_id>', 'get_scooter', self.get_scooter, methods=['GET'])
        app.add_url_rule('/scooter/update_scooter_status', 'update_scooter_status', self.update_scooter_status, methods=['PUT'])
        app.add_url_rule('/scooter/scooters', 'get_all_scooters', self.get_all_scooters, methods=['GET'])
        app.add_url_rule('/scooter/update_ip_address/<int:scooter_id>', 'update_scooter_ip_address', self.update_scooter_ip_address, methods=['PUT'])
        app.add_url_rule('/scooter/update_location/<int:scooter_id>', 'update_scooter_location', self.update_scooter_location, methods=['PUT'])
        app.add_url_rule('/scooter/update_details/<int:scooter_id>', 'update_scooter_details', self.update_scooter_details, methods=['PUT'])
                
    def get_scooter(self, scooter_id):
        """
        API endpoint to retrieve a scooter's details by its ID.

        Args:
            scooter_id (int): The ID of the scooter.

        Returns:
            Response: JSON response containing scooter details or a 404 error if not found.
        """
        result = self.scooter_handler.get_scooter(scooter_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "Scooter not found."}), 404

    def update_scooter_status(self):
        data = request.json
        self.scooter_handler.update_scooter_status(
            scooter_id=data['scooter_id'],
            new_status=data['status']
        )
        return jsonify({"message": "Scooter status updated successfully."})

    def get_all_scooters(self):
        """
        API endpoint to retrieve details for all scooters.

        Returns:
            Response: JSON response containing a list of scooters or an empty list if no scooters are found.
        """
        result = self.scooter_handler.get_all_scooters()
        return jsonify(result if result else [])
    
    def update_scooter_ip_address(self, scooter_id):
        """
        API endpoint to update the IP address for a scooter.

        Expected JSON payload:
        {
            "ip_address": str
        }
        """
        data = request.json
        self.scooter_handler.update_scooter_ip_address(
            scooter_id=scooter_id,
            new_ip_address=data['ip_address']
        )
        return jsonify({"message": "Scooter IP address updated successfully."})

    def update_scooter_location(self, scooter_id):
        """
        API endpoint to update the location (latitude and longitude) for a scooter.

        Expected JSON payload:
        {
            "latitude": float,
            "longitude": float
        }
        """
        data = request.json
        self.scooter_handler.update_scooter_location(
            scooter_id=scooter_id,
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        return jsonify({"message": "Scooter location updated successfully."})
    
    def update_scooter_details(self, scooter_id):
        """
        API endpoint to update all details for a scooter.

        Expected JSON payload:
        {
            "make": str,
            "colour": str,
            "latitude": float,
            "longitude": float,
            "cost_min": float,
            "battery_percentage": int,
            "status": str,
            "ip_address": str
        }
        """
        data = request.json
        self.scooter_handler.update_scooter_details(
            scooter_id=scooter_id,
            make=data['make'],
            colour=data['colour'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            cost_min=data['cost_min'],
            battery_percentage=data['battery_percentage'],
            status=data['status'],
            ip_address=data['ip_address']
        )
        return jsonify({"message": "Scooter details updated successfully."}), 200