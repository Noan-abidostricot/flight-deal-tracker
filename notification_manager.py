import os
import smtplib
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.email = os.environ["EMAIL"]
        self.password = os.environ["PASSWORD"]

    def send_email(self, emails, message):
        msg = MIMEText(message, "plain", "utf-8")
        msg["Subject"] = "Flight Deal Alert!"
        msg["From"] = self.email

        with smtplib.SMTP("127.0.0.1", port=1025) as connection:
            connection.login(self.email, self.password)

            for email in emails:
                del msg["To"]
                msg["To"] = email
                connection.sendmail(self.email, email, msg.as_string())
