import re
import logging

from decimal import Decimal
from supportBank import CSVData
from supportBank.Account import Account
from supportBank.Transaction import Transaction


class Bank:
    def __init__(self):
        self.accounts = {}
        self.bank_open = True
        logging.basicConfig(filename='../log/SupportBank.log', filemode='w', level=logging.DEBUG)
        self.error_count = 0

    def parse_csv_data(self, csv_data: CSVData):
        name_set = set()
        for row in csv_data.rows:
            name_set.add(row.get_entry("From"))
            name_set.add(row.get_entry("To"))
        for name in name_set:
            self.accounts[name] = Account(name)
        row_count = 2
        self.error_count = 0
        for row in csv_data.rows:
            self.create_transaction_from_row(row, row_count)
            row_count += 1
        logging.info("Bank has parsed CSV Data. " + str(self.error_count) + " rows were rejected.")

    def create_transaction_from_row(self, row, row_count):
        try:
            date = row.get_entry("Date")
            if not re.match(r"[\d]{2}/[\d]{2}/[\d]{4}", date):
                logging.warning("Row: " + str(row_count) + " contains a date error and could not be parsed. Dates must "
                                                           "be in the format dd/mm/yyyy.")
                self.error_count += 1
                return
        except:
            logging.warning("Row: " + str(row_count) + " contains a date error and could not be parsed. Dates must "
                                                       "be in the format dd/mm/yyyy.")
            self.error_count += 1
            return
        try:
            account_from = row.get_entry("From")
        except:
            logging.warning("Row: " + str(row_count) + " contains an error with the \"From\" column and could not be "
                                                       "parsed.")
            self.error_count += 1
            return
        try:
            account_to = row.get_entry("To")
        except:
            logging.warning("Row: " + str(row_count) + " contains an error with the \"To\" column and could not be "
                                                       "parsed.")
            self.error_count += 1
            return
        try:
            narrative = row.get_entry("Narrative")
        except:
            logging.warning("Row: " + str(row_count) + " contains an error with the \"Narrative\" column and could not "
                                                       "be parsed.")
            self.error_count += 1
            return
        try:
            amount = Decimal(row.get_entry("Amount"))
        except:
            logging.warning("Row: " + str(row_count) + " contains an invalid decimal and could not be parsed.")
            self.error_count += 1
            return
        self.create_transaction(date, account_from, account_to, narrative, amount)

    def add_account(self, account: Account):
        self.accounts[account.name] = {account}

    def create_transaction(self, date: str, name_from: str, name_to: str, narrative: str, amount: Decimal):
        account_from = self.accounts[name_from]
        account_to = self.accounts[name_to]
        transaction = Transaction(date, account_from, account_to, narrative, amount)
        account_from.add_transaction_from(transaction)
        account_to.add_transaction_to(transaction)

    def list_all(self):
        for name, account in self.accounts.items():
            print(account.list_all_format())

    def list_account(self, name: str):
        print(self.accounts[name].list_account())

    def do_user_command(self, command: str):
        logging.info("User performed the following command: \"" + command + "\"")
        if command == "List All":
            self.list_all()
        elif re.match(r"List \[[a-z A-Z]+\]", command):
            command = re.sub(r"List \[", "", command)
            name = re.sub(r"\]", "", command)
            if self.accounts.__contains__(name):
                self.list_account(name)
        elif command == "end":
            self.bank_open = False
            logging.info("Bank has closed for the day.")
