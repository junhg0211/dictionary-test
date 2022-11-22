from datetime import date
import gspread


def parse_date(raw_date: str) -> date:
    if '. ' in raw_date:
        return date(*map(int, raw_date.split('. ')))

    if '-' in raw_date:
        return date(*map(int, raw_date.split('-')))


def main():
    spreadsheet_key = '1OxeNtB_Mpm172WkglsKj7ilQ20ymX0yJvLbyBuH-l5E'

    credential = gspread.service_account(filename='res/google_credentials.json')
    sheet = credential.open_by_key(spreadsheet_key).get_worksheet(0)

    today = date.today()

    rows = sheet.get_all_values()[1:]
    for i, row in enumerate(rows):
        if not row[0]:
            continue

        if today == parse_date(row[0]):
            print(i, *row[1:5])


if __name__ == '__main__':
    main()
