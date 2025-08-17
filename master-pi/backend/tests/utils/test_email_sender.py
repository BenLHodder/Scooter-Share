import unittest
from unittest.mock import patch, MagicMock, mock_open
import smtplib
import logging
import json
from utils.email_sender import EmailSender

class TestEmailSender(unittest.TestCase):
    
    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open, read_data='{"smtp_server": "smtp.test.com", "smtp_port": 587, "sender_email": "test@test.com", "sender_password": "password"}')
    def test_send_email_success(self, mock_file, mock_smtp):
        """Test if send_email works correctly when no exception is raised."""
        # Mock the SMTP server and its methods
        mock_server = MagicMock()
        mock_smtp.return_value = mock_server
        
        with self.assertLogs(level='INFO') as log:
            EmailSender.send_email('test_config.json', 'recipient@test.com', 'Test Subject', 'Test Body')

            self.assertIn('INFO:root:Email sent successfully to recipient@test.com', log.output)
        
        mock_server.sendmail.assert_called_once()
        mock_file.assert_called_once_with('test_config.json', 'r')

    @patch('smtplib.SMTP')
    @patch('builtins.open', new_callable=mock_open, read_data='{"smtp_server": "smtp.test.com", "smtp_port": 587, "sender_email": "test@test.com", "sender_password": "password"}')
    def test_send_email_failure(self, mock_file, mock_smtp):
        """Test if send_email handles SMTPException properly."""
        # Simulate an SMTP failure
        mock_server = MagicMock()
        mock_server.sendmail.side_effect = smtplib.SMTPException("Failed to send")
        mock_smtp.return_value = mock_server

        with self.assertLogs(level='ERROR') as log:
            EmailSender.send_email('test_config.json', 'recipient@test.com', 'Test Subject', 'Test Body')

            self.assertIn('ERROR:root:Failed to send email to recipient@test.com. Error: Failed to send', log.output)
        
        mock_server.sendmail.assert_called_once()
        mock_file.assert_called_once_with('test_config.json', 'r')

if __name__ == '__main__':
    unittest.main()