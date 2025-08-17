import unittest
from bs4 import BeautifulSoup
from app import ScooterWebApp


class DashboardTests(unittest.TestCase):
    def setUp(self):
        scooter_app = ScooterWebApp()
        self.app = scooter_app.get_app()
        self.client = self.app.test_client()
        self.app.config["TESTING"] = True
        self.app.config["WTF_CSRF_ENABLED"] = False

        # Set up a logged-in session for testing
        with self.client.session_transaction() as sess:
            sess["logged_in"] = True
            sess["first_name"] = "wrong"
            sess["email"] = "info"
            sess["role"] = "Admin"

    def test_flash_messages(self):
        """Test that flash messages are displayed correctly"""
        with self.client.session_transaction() as sess:
            sess["logged_in"] = False  # Simulate user is not logged in

        response = self.client.get("/home", follow_redirects=True)
        soup = BeautifulSoup(response.data, "html.parser")

        # Check for flash message div
        flash_message_div = soup.select_one(".message")
        self.assertIsNotNone(flash_message_div, "Flash message div not found")

        # Check flash message content
        message_text = flash_message_div.get_text(strip=True)
        self.assertIn(
            "Please log in first",
            message_text,
            "Flash message does not contain the expected text",
        )


if __name__ == "__main__":
    unittest.main()
