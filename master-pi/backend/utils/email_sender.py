import smtplib
import json
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class EmailSender:
    @staticmethod
    def send_email(json_file, to_address, subject, body):
        try:
            # Read the configuration from the provided JSON file
            with open(json_file, 'r') as file:
                config = json.load(file)
            
            smtp_server = config['smtp_server']
            smtp_port = config['smtp_port']
            sender_email = config['sender_email']
            sender_password = config['sender_password']

            # Create a multipart message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ','.join(to_address)
            msg['Subject'] = subject
            
            print(msg['To'])

            # Attach the body text
            msg.attach(MIMEText(body, 'plain'))

            # Use SMTP_SSL if the port is 465
            if smtp_port == 465:
                server = smtplib.SMTP_SSL(smtp_server, smtp_port)
            elif smtp_port == 587:
                server = smtplib.SMTP(smtp_server, smtp_port)
                server.starttls()
            else:
                server = smtplib.SMTP(smtp_server, smtp_port)

            # Log in to the server
            server.login(sender_email, sender_password)
            
            # Send the email
            text = msg.as_string()
            server.sendmail(sender_email, to_address, text)
            server.quit()

            logging.info(f"Email sent successfully to {to_address}")
        except Exception as e:
            logging.error(f"Failed to send email to {to_address}. Error: {e}")