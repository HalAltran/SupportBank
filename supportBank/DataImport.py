import csv
import logging
import json
import os
import decimal

from datetime import timedelta
from datetime import datetime
from decimal import Decimal
from xml.etree import ElementTree

from supportBank import Bank


class DataImport:
    def __init__(self, file_path: str):
        self.file_path = "../input/%s" % file_path
        self.rows = []
        self.headers = Bank.COLUMN_HEADERS
        self.error_count = 0
        logging.basicConfig(filename='../log/SupportBank.log', filemode='w', level=logging.DEBUG)
        self.file_ext = os.path.splitext(file_path)[1]
        self.parse_data()

    def parse_data(self):
        logging.info("Bank is parsing %s Data from: \"%s\"." % (self.file_ext, self.file_path))
        extension_to_parsing_command_map = {".csv": self.parse_csv, ".xml": self.parse_xml, ".json": self.parse_json}
        extension_to_parsing_command_map[self.file_ext]
        parse_function = extension_to_parsing_command_map.get(self.file_ext)
        parse_function()
        logging.info("Bank has parsed %s Data from: \"%s\". %d rows were rejected." % (self.file_ext, self.file_path,
                                                                                       self.error_count))

    def parse_csv(self):
        with open(self.file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=",")
            next(csv_reader)
            row_count = 1
            self.error_count = 0
            for row in csv_reader:
                self.create_row(row, row_count, "%d/%m/%Y")
                row_count += 1

    def create_row(self, row, row_count, date_format):
        data_row = {}
        entry_count = 0
        for entry in row:
            entry_header = self.headers[entry_count]
            try:
                if entry_header == Bank.DATE_COLUMN_HEADER and not isinstance(entry, datetime):
                    entry = datetime.strptime(entry, date_format)
                elif entry_header == Bank.AMOUNT_COLUMN_HEADER:
                    entry = Decimal(entry) + Decimal("0.00")
                data_row[entry_header] = entry
                entry_count += 1
            except (decimal.DecimalException, ValueError):
                log_data = (row_count, entry_header, entry)
                logging.warning("Row: %d contains an invalid \"%s: %s\" and could not be parsed." % log_data)
                self.error_count += 1
                return
        self.rows.append(data_row)

    def parse_json(self):
        with open(self.file_path) as json_file:
            json_data = json.load(json_file)
            self.error_count = 0
            row_count = 0
            for row in json_data:
                self.create_row([row["date"], row["fromAccount"], row["toAccount"], row["narrative"],
                                 str(row["amount"])], row_count, "%Y-%m-%d")
                row_count += 1

    def parse_xml(self):
        xml_tree = ElementTree.parse(self.file_path)
        transaction_list = xml_tree.getroot()
        self.error_count = 0
        row_count = 0
        for support_transaction in transaction_list:
            row_dict = self.get_xml_transaction_dict(support_transaction)
            row_list = self.get_row_list_from_row_dict(row_dict)
            self.create_row(row_list, row_count, "%d/%m/%Y")
            row_count += 1

    def get_xml_transaction_dict(self, support_transaction):
        transaction_dict = {Bank.DATE_COLUMN_HEADER: self.format_xml_date(support_transaction.attrib["Date"])}
        for attribute in support_transaction:
            if attribute.tag == "Description":
                transaction_dict[Bank.NARRATIVE_COLUMN_HEADER] = attribute.text
            elif attribute.tag == "Value":
                transaction_dict[Bank.AMOUNT_COLUMN_HEADER] = attribute.text
            elif attribute.tag == "Parties":
                for member in attribute:
                    transaction_dict[member.tag] = member.text
        return transaction_dict

    def get_row_list_from_row_dict(self, row_dict):
        row_list = []
        for header in self.headers.values():
            row_list.append(row_dict[header])
        return row_list

    @staticmethod
    def format_xml_date(xml_date):
        base_date = datetime.strptime("01/01/1900", "%d/%m/%Y")
        return base_date + timedelta(days=int(xml_date))
