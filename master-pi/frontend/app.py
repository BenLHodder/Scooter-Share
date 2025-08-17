from flask import Flask
from handler.socket_manager import SocketManager
from routes.auth_routes import login_routes
from routes.dashboard_routes import dashboard_routes


class ScooterWebApp:
    """Scooter Web Application"""

    def __init__(self):
        # Initialise Flask app
        self.app = Flask(__name__)
        self.app.secret_key = "V7X1~8o>hW[)HySUye"  # Needed for flashing messages

        # Register routes
        self.setup_routes()

    def setup_routes(self):
        """Setup Routes for the application"""
        login_routes(self.app)
        dashboard_routes(self.app)

    def get_app(self):
        """Return the Flask app instance"""
        return self.app

    def run(self, debug, host, port):
        """Run the app on the given host and port"""
        self.app.run(debug=debug, host=host, port=port)
