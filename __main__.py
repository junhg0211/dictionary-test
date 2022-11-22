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

    for row in rows:
        if not row[0]:
            continue

        if today == parse_date(row[0]):
            print(*row[1:5])
            continue

        if today in (parse_date(row[i]) for i in range(5, len(row), 2)):
            actual_rows.append(row)

    for i, row in enumerate(actual_rows):
        print(f'{i/len(actual_rows)*100:.3f}%, {i} / {len(actual_rows)}\n')

        for i in range(5, len(row), 2):
            hanzi_to_meaning = i % 4 == 1
            if parse_date(row[i]) == today and hanzi_to_meaning:
                input(f'{i}. {parse_date(row[0])}, {row[1]}: ')
                print(i, *row[1:5], sep='\t')
                continue

            if parse_date(row[i]) == today and not hanzi_to_meaning:
                input(f'{i}. {parse_date(row[0])}, {row[3]}: ')
                print(i, *row[1:5], sep='\t')
                continue


if __name__ == '__main__':
    main()
