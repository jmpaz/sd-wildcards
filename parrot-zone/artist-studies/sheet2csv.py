#!/usr/bin/env python

import csv
import os

import googleapiclient as gac
import oauth2client as oac
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SPREADSHEET_ID = '14xTqtuV3BuKDNhLotB_d1aFlBGnDJOY0BRXJ8-86GpA'
RANGE_NAME = 'Artists!A3:M'


# Authenticate with credentials.json from your Google Cloud project
def auth():
    creds = None

    if os.path.exists('.creds/token.json'):
        creds = Credentials.from_authorized_user_file('.creds/token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists('.creds/credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file('.creds/credentials.json', SCOPES)
            else:
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                os.rename('credentials.json', '.creds/credentials.json')

            creds = flow.run_local_server(port=0)
        with open('.creds/token.json', 'w') as token:
            token.write(creds.to_json())

    return gac.discovery.build('sheets', 'v4', credentials=creds)

        
def write_csv(values):
    with open('artists.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in values:

            # Strip newlines, trailing commas and double spaces from each cell
            cleaned_row = [cell.replace('\n', ' ').rstrip(',').replace('  ', ' ') for cell in row]

            writer.writerow(cleaned_row)


def main():

    # Call the Sheets API
    service = auth()
    sheet = service.spreadsheets()

    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()

    values = result.get('values', [])

    if not values:
        print('No data found.')

    else:
        write_csv(values)

    
if __name__ == '__main__':
    main()