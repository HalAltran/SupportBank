import csv

from supportBank.CSVRow import CSVRow


class CSVData:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.rows = []
        self.headers = {}
        self.parse_csv()

    def parse_csv(self):
        with open(self.file_path) as csv_file:
            row_count = 0
            for row in csv.reader(csv_file, delimiter=","):
                if row_count == 0:
                    self.populate_headers(row)
                else:
                    self.rows.append(CSVRow(self.headers, row))
                row_count += 1

    def populate_headers(self, header_row):
        count = 0
        for entry in header_row:
            self.headers[entry] = count
            count += 1
