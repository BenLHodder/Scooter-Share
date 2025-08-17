from flask import request, jsonify
from db_driver.faultlog_db_handler import FaultLogHandler

class FaultLogAPI:
    def __init__(self, app, db_info_file):
        self.fault_log_handler = FaultLogHandler(db_info_file)
        self._setup_routes(app)

    def _setup_routes(self, app):
        # Register routes
        app.add_url_rule('/fault/update_scooter_fault', 'update_scooter_fault', self.update_scooter_fault, methods=['PUT'])
        app.add_url_rule('/fault/resolve_scooter_fault/<int:fault_id>', 'resolve_scooter_fault', self.resolve_scooter_fault, methods=['PUT'])
        app.add_url_rule('/fault/open_faults', 'get_open_faults', self.get_open_faults, methods=['GET'])
        app.add_url_rule('/fault/scooter/<int:scooter_id>', 'get_fault_by_scooter', self.get_fault_by_scooter, methods=['GET'])
        app.add_url_rule('/fault/<int:fault_id>', 'get_fault_by_id', self.get_fault_by_id, methods=['GET'])

    def update_scooter_fault(self):
        data = request.json
        self.fault_log_handler.update_scooter_fault(
            scooter_id=data['scooter_id'],
            fault_notes=data['fault_notes']
        )
        return jsonify({"message": "Scooter fault updated successfully."}), 200

    def resolve_scooter_fault(self, fault_id):
        data = request.json
        self.fault_log_handler.resolve_scooter_fault(
            fault_id=fault_id,
            resolution_notes=data['resolution_notes']
        )
        return jsonify({"message": "Scooter fault resolved successfully."}), 200

    def get_open_faults(self):
        """
        API endpoint to retrieve all open faults.
        
        Returns:
            Response: JSON response containing a list of open faults.
        """
        result = self.fault_log_handler.get_open_faults()
        return jsonify(result if result else [])

    def get_fault_by_scooter(self, scooter_id):
        """
        API endpoint to retrieve the latest fault for a specific scooter.
        
        Args:
            scooter_id (int): The ID of the scooter.

        Returns:
            Response: JSON response containing the latest fault or a 404 error if not found.
        """
        result = self.fault_log_handler.get_fault_by_scooter(scooter_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "Fault not found for the specified scooter."}), 404

    def get_fault_by_id(self, fault_id):
        """
        API endpoint to retrieve a fault entry by its faultID.
        
        Args:
            fault_id (int): The ID of the fault.

        Returns:
            Response: JSON response containing fault details or a 404 error if not found.
        """
        result = self.fault_log_handler.get_fault_by_id(fault_id)
        if result:
            return jsonify(result)
        else:
            return jsonify({"message": "Fault not found."}), 404
