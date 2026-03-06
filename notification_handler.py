import smtplib
from email.mime.text import MIMEText
import requests

class NotificationHandler:
    def __init__(self, slack_webhook_url, email_config):
        self.slack_webhook_url = slack_webhook_url
        self.email_config = email_config

    def send_slack_notification(self, message):
        payload = {'text': message}
        response = requests.post(self.slack_webhook_url, json=payload)
        return response.status_code

    def send_email_notification(self, subject, body):
        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = self.email_config['from_address']
        msg['To'] = self.email_config['to_address']

        with smtplib.SMTP(self.email_config['smtp_server'], self.email_config['smtp_port']) as server:
            server.starttls()
            server.login(self.email_config['from_address'], self.email_config['password'])
            server.send_message(msg)

# Usage example:
# notification_handler = NotificationHandler(slack_webhook_url='YOUR_SLACK_WEBHOOK_URL', email_config={
#     'smtp_server': 'smtp.example.com',
#     'smtp_port': 587,
#     'from_address': 'your_email@example.com',
#     'to_address': 'recipient@example.com',
#     'password': 'YOUR_PASSWORD'
# })
# notification_handler.send_slack_notification('Hello Slack!')
# notification_handler.send_email_notification('Hello', 'This is an email notification.')
