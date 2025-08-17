import unittest
from unittest.mock import patch
from app import ScooterWebApp


class AuthTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        scooter_app = ScooterWebApp()
        scooter_app.app.config["TESTING"] = True  # Access the Flask app object
        cls.client = scooter_app.app.test_client()

    @patch("app.SocketManager")
    def test_register_password_mismatch(self, mock_socket):
        mock_socket.return_value = None

        response = self.client.post(
            "/register",
            data={
                "first_name": "Jane",
                "last_name": "Doe",
                "phone_no": "0987654321",
                "email": "jane.doe@example.com",
                "password": "securepassword",
                "confirm_password": "differentpassword",
            },
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Passwords do not match", response.data)


if __name__ == "__main__":
    unittest.main()
