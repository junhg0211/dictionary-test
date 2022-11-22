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
    actual_rows = list()

    for i, row in enumerate(rows):
        if not row[0]:
            continue

        if today == parse_date(row[0]):
            print(i+2, *row[1:5])
            continue

        if today in (parse_date(row[i]) for i in range(5, len(row), 2)):
            actual_rows.append((i+2, row))

    for i, (row_number, row) in enumerate(actual_rows):
        print(f'{i/len(actual_rows)*100:.3f}%, {i} / {len(actual_rows)}\n')

        for j in range(5, len(row), 2):
            hanzi_to_meaning = j % 4 == 1
            if parse_date(row[j]) == today and hanzi_to_meaning:
                input(f'{row_number}. {parse_date(row[0])}, {row[1]}: ')
                print(row_number, *row[1:5], sep='\t')
                continue

            if parse_date(row[j]) == today and not hanzi_to_meaning:
                input(f'{row_number}. {parse_date(row[0])}, {row[3]}: ')
                print(row_number, *row[1:5], sep='\t')
                continue


if __name__ == '__main__':
    main()
