import csv
import logging
import json
import os
import xml.etree.ElementTree as xml

from datetime import timedelta
from datetime import datetime
from decimal import Decimal


class DataImport:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.rows = []
        self.headers = {}
        self.error_count = 0
        logging.basicConfig(filename='../log/SupportBank.log', filemode='w', level=logging.DEBUG)
        self.file_ext = os.path.splitext(file_path)[1]
        logging.info("Bank is parsing %s Data from: \"%s\"." % (self.file_ext, self.file_path))
        if self.file_ext == ".csv":
            self.parse_csv()
        elif self.file_ext == ".xml":
            self.parse_xml()
        else:
            self.parse_json()
        logging.info("Bank has parsed %s Data from: \"%s\". %d rows were rejected." % (self.file_ext, self.file_path,
                                                                                       self.error_count))

    def parse_csv(self):
        with open(self.file_path) as csv_file:
            row_count = 0
            first_row = True
            self.error_count = 0
            for row in csv.reader(csv_file, delimiter=","):
                if first_row:
                    self.populate_headers(row)
                    first_row = False
                else:
                    self.create_row(row, row_count, "%d/%m/%Y")
                row_count += 1

    def create_row(self, row, row_count, date_format: str):
        data_row = {}
        entry_count = 0
        for entry in row:
            entry_header = self.headers[entry_count]
            try:
                if entry_header == "Date" and not isinstance(entry, datetime):
                    entry = datetime.strptime(entry, date_format)
                elif entry_header == "Amount":
                    entry = Decimal(entry)
                data_row[entry_header] = entry
                entry_count += 1
            except:
                logging.warning("Row: %d contains an invalid \"%s\" and could not be parsed." % (row_count,
                                                                                                 entry_header))
                self.error_count += 1
                return
        self.rows.append(data_row)

    def populate_headers(self, header_row):
        count = 0
        for entry in header_row:
            self.headers[count] = entry
            count += 1

    def parse_json(self):
        with open(self.file_path) as json_file:
            json_data = json.load(json_file)
            self.headers = {0: "Date", 1: "From", 2: "To", 3: "Narrative", 4: "Amount"}
            row_count = 0
            for row in json_data:
                self.create_row([row["date"], row["fromAccount"], row["toAccount"], row["narrative"], row["amount"]],
                                row_count, "%Y-%m-%d")
                row_count += 1

    def parse_xml(self):
        xml_tree = xml.parse(self.file_path)
        transaction_list = xml_tree.getroot()
        self.headers = {0: "Date", 1: "From", 2: "To", 3: "Narrative", 4: "Amount"}
        row_count = 0
        for support_transaction in transaction_list:
            row_dict = {"Date": self.format_xml_date(support_transaction.attrib["Date"])}
            for attribute in support_transaction:
                if attribute.tag == "Description":
                    row_dict["Narrative"] = attribute.text
                elif attribute.tag == "Value":
                    row_dict["Amount"] = attribute.text
                elif attribute.tag == "Parties":
                    for member in attribute:
                        row_dict[member.tag] = member.text
            row_list = []
            for header in self.headers.values():
                row_list.append(row_dict[header])

            self.create_row(row_list, row_count, "%d/%m/%Y")
            row_count += 1

    @staticmethod
    def format_xml_date(xml_date):
        base_date = datetime.strptime("01/01/1900", "%d/%m/%Y")
        return base_date + timedelta(days=int(xml_date))
