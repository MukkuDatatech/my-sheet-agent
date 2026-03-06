import datetime
import base64
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

class GmailExtractor:
    def __init__(self):
        self.credentials = None

    def authenticate(self):
        # Authenticate the user
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        self.credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(self.credentials.to_json())

    def fetch_emails(self):
        # Fetch emails from the user's inbox
        service = build('gmail', 'v1', credentials=self.credentials)
        results = service.users().messages().list(userId='me', maxResults=10).execute()
        messages = results.get('messages', [])
        return messages

    def extract_email_details(self, message):
        # Extract details from an email message
        msg = self.get_message(message['id'])
        if msg and 'payload' in msg:
            headers = msg['payload']['headers']
            email_data = {header['name']: header['value'] for header in headers}
            return email_data
        return None

    def parse_email_body(self, message):
        # Parse the email body to extract information
        msg = self.get_message(message['id'])
        if msg and 'payload' in msg:
            data = msg['payload']['parts'][0]['body']['data']
            byte_code = base64.urlsafe_b64decode(data.encode('UTF-8'))
            return byte_code.decode('UTF-8')
        return None

    def extract_lead_information(self, email_body):
        # Custom logic to extract lead information from email body
        # Example: Find specific patterns, regex ...
        leads = []
        # Placeholder for actual logic
        return leads

    def process_new_leads(self):
        # Process new leads
        messages = self.fetch_emails()
        for message in messages:
            email_details = self.extract_email_details(message)
            email_body = self.parse_email_body(message)
            leads = self.extract_lead_information(email_body)
            # Add logic to store or process leads
            print(f'Processed leads: {leads}')

    def get_message(self, msg_id):
        service = build('gmail', 'v1', credentials=self.credentials)
        return service.users().messages().get(userId='me', id=msg_id, format='full').execute()

if __name__ == '__main__':
    extractor = GmailExtractor()
    extractor.authenticate()
    extractor.process_new_leads()