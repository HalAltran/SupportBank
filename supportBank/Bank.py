import re
import logging

from supportBank.DataImport import DataImport
from supportBank.Account import Account
from supportBank.Transaction import Transaction


class Bank:
    def __init__(self):
        self.accounts = {}
        self.bank_open = True
        logging.basicConfig(filename='../log/SupportBank.log', filemode='w', level=logging.DEBUG)

    def import_data(self, data: DataImport):
        for row in data.rows:
            self.create_account_if_name_does_not_exist(row["From"])
            self.create_account_if_name_does_not_exist(row["To"])
        row_count = 2
        for row in data.rows:
            self.create_transaction(row)
            row_count += 1

    def create_account_if_name_does_not_exist(self, name):
        if not self.accounts.__contains__(name):
            self.accounts[name] = Account(name)

    def create_transaction(self, row):
        account_from = self.accounts[row["From"]]
        account_to = self.accounts[row["To"]]
        transaction = Transaction(row["Date"], account_from, account_to, row["Narrative"], row["Amount"])
        account_from.add_transaction_from(transaction)
        account_to.add_transaction_to(transaction)

    def add_account(self, account: Account):
        self.accounts[account.name] = {account}

    def list_all(self):
        for name, account in self.accounts.items():
            print(account.list_all_format())

    def list_account(self, name: str):
        print(self.accounts[name].list_account())

    def do_user_command(self, command: str):
        if command == "List All":
            self.list_all()
        elif re.match(r"List \[[a-z A-Z]+\]", command):
            name = re.sub(r"List \[", "", command)
            name = re.sub(r"\]", "", name)
            if self.accounts.__contains__(name):
                self.list_account(name)
            else:
                logging.info("User attempted to list information for account: \"%s\" which does not exist" % name)
                print("Bank account for \"%s\" does not exist. Please enter a new command." % name)
        elif command == "end":
            self.bank_open = False
        elif re.match(r"Import File \[[\S]+\]", command):
            file_path = re.sub(r"Import File \[", "", command)
            file_path = re.sub(r"\]", "", file_path)
            logging.info("Importing data from %s" % file_path)
            try:
                self.import_data(DataImport(file_path))
            except:
                logging.warning("Could not import data from %s" % file_path)
                print("Could not import data from %s" % file_path)
                return
            logging.info("Importing data from %s" % file_path)
            print("Data imported successfully.")
        else:
            logging.warning("User attempted to perform command: \"%s\" which is not valid." % command)
            print("Please enter a valid command such as: \"List All\"; \"List [Account]\"; \"end\".")
            return
        logging.info("User performed the following command: \"%s\"" % command)

    @staticmethod
    def log_info(text_to_log):
        logging.info(text_to_log)
