import datetime
import time

import xml.etree.ElementTree as ET
import requests
import httplib2
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials
import db_script


def parse_row(data: dict) -> dict:
    _id = data['values'][0]['userEnteredValue']['numberValue']
    order_num = data['values'][1]['userEnteredValue']['numberValue']
    cost_dollar = data['values'][2]['userEnteredValue']['numberValue']

    days = data['values'][3]['userEnteredValue']['numberValue']
    date_start = datetime.date(1900, 1, 1)
    date_delivery = datetime.timedelta(days=days - 2) + date_start

    res = {
        'id': _id,
        'order_num': order_num,
        'cost_dollar': cost_dollar,
        'date_delivery': date_delivery,
    }

    return res


def get_dollar_rate(date_delivery: datetime) -> float:
    url = f'https://www.cbr.ru/scripts/XML_daily.asp?date_req={date_delivery.day:02}/{date_delivery.month:02}/{date_delivery.year}'
    req = requests.get(url)
    structure = ET.fromstring(req.content)
    dollar = structure.find("./*[@ID='R01235']/Value")
    dollar_rate = float(dollar.text.replace(',', '.'))

    return dollar_rate


class Sheets:
    def __init__(self, _cred_file, _spreadsheet_id):
        self.cred_file = _cred_file
        self.spreadsheet_id = _spreadsheet_id
        self.service_sheets = self.get_service(_cred_file, 'sheets', 'v4')
        self.service_drive = self.get_service(_cred_file, 'drive', 'v3')

    @staticmethod
    def get_service(cred_file, service_name, service_version):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            cred_file,
            ['https://www.googleapis.com/auth/spreadsheets',
             'https://www.googleapis.com/auth/drive'])
        http_auth = credentials.authorize(httplib2.Http())
        service = apiclient.discovery.build(service_name, service_version, http=http_auth)

        return service

    def get_data_from_sheet(self):
        response = self.service_sheets.spreadsheets().get(
            spreadsheetId=self.spreadsheet_id,
            fields='sheets(data/rowData/values/userEnteredValue,properties(index,sheetId,title))'
        ).execute()
        data = response['sheets'][0]['data'][0]['rowData'][1:]

        if len(data) <= 1:
            return []

        info = list()
        for row in data:
            try:
                data = parse_row(row)
                dollar_rate = get_dollar_rate(data['date_delivery'])
                data['cost_ruble'] = dollar_rate * data['cost_dollar']
            except KeyError:
                continue
            info.append(data)

        return info

    def get_last_edit_time(self):
        files = self.service_drive.files()
        remote_file_hash = files.get(fileId=self.spreadsheet_id, fields="modifiedTime").execute()['modifiedTime']
        return remote_file_hash


def process():
    time.sleep(4)
    CREDENTIALS_FILE = 'credentials/creds.json'
    spreadsheet_id = '1IxOrx-AWiK0Xz-gi9K_ex8NyzW1To4MwV7AyBCbVVzU'

    sheet = Sheets(CREDENTIALS_FILE, spreadsheet_id)

    while True:
        with open('time_edit.txt', 'r') as f:
            edit_time = f.readline()

        real_edit_time = sheet.get_last_edit_time()
        if edit_time != sheet.get_last_edit_time():
            with open('time_edit.txt', 'w') as f:
                f.write(real_edit_time)
            db_script.drop_table()
            info = sheet.get_data_from_sheet()
            write_db(info)

        f.close()
        time.sleep(20)


def write_db(info):
    for item in info:
        db_script.add_record(item['id'], item['order_num'], item['cost_dollar'], item['date_delivery'], item['cost_ruble'])


if __name__ == '__main__':
    process()
