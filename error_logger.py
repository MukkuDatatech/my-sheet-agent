import gspread
from oauth2client.service_account import ServiceAccountCredentials
import logging
import datetime

# Set up Google Sheets API credentials and scope
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_service_account.json', scope)
client = gspread.authorize(creds)

# Open the Google Sheet and select the error log tab
spreadsheet = client.open('Your Spreadsheet Name')
worksheet = spreadsheet.worksheet('Error Log')

# Configure logging
logging.basicConfig(level=logging.ERROR, format='%(asctime)s - %(levelname)s - %(message)s')


def log_error(error_message):
    # Log the error in the console
    logging.error(error_message)
    # Log the error in Google Sheets
    timestamp = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    worksheet.append_row([timestamp, error_message])

# Example usage
if __name__ == '__main__':
    try:
        # Simulate API call
        raise Exception('API failure example')
    except Exception as e:
        log_error(str(e))