import gspread
from oauth2client.service_account import ServiceAccountCredentials

class SheetsManager:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.client = self.authenticate()

    def authenticate(self):
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.credentials_file, scope)
        return gspread.authorize(credentials)

    def update_sheet(self, sheet_name, cell, value):
        sheet = self.client.open(sheet_name).sheet1
        sheet.update_acell(cell, value)

    def read_sheet(self, sheet_name):
        sheet = self.client.open(sheet_name).sheet1
        return sheet.get_all_records()