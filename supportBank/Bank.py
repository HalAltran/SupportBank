import re
import logging
import csv

from supportBank.DataImport import DataImport
from supportBank.Account import Account
from supportBank.Transaction import Transaction


class Bank:
    def __init__(self):
        self.accounts = {}
        self.bank_open = True
        logging.basicConfig(filename='../log/SupportBank.log', filemode='w', level=logging.DEBUG)

    def run(self):
        self.import_data(DataImport("../res/Transactions2014.csv"))
        self.import_data(DataImport("../res/DodgyTransactions2015.csv"))
        self.import_data(DataImport("../res/Transactions2013.json"))
        self.import_data(DataImport("../res/Transactions2012.xml"))
        while self.bank_open:
            user_command = input("Type command: ")
            self.do_user_command(user_command)

    def import_data(self, data: DataImport):
        for row in data.rows:
            self.create_account_if_name_does_not_exist(row["From"])
            self.create_account_if_name_does_not_exist(row["To"])
        row_count = 2
        for row in data.rows:
            self.create_transaction(row)
            row_count += 1
        self.sort_transactions()

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

    def sort_transactions(self):
        for account in self.accounts.values():
            account.sort_transactions()

    def get_all_transactions(self):
        transactions = set()
        for account in self.accounts.values():
            transactions.update(account.transactions)
        return sorted(transactions, key=lambda transaction: transaction.date)

    def do_user_command(self, command: str):
        logging.info("User performed the following command: \"%s\"" % command)
        if command == "List All":
            self.list_all()
        elif self.is_list_account_command(command):
            self.list_account(command)
        elif self.is_import_command(command):
            self.import_file(command)
        elif self.is_export_command(command):
            self.write_to_file(command)
        elif command == "end":
            self.close_bank()
        else:
            self.log_invalid_command(command)
            return

    @staticmethod
    def is_list_account_command(command):
        return re.match(r"List \[[a-z A-Z]+\]", command)

    @staticmethod
    def is_import_command(command):
        return re.match(r"Import File \[[\S]+\]", command)

    @staticmethod
    def is_export_command(command):
        return re.match(r"Export File \[[\S]+\]", command)

    def list_account(self, command):
        name = re.sub(r"List \[", "", command)
        name = re.sub(r"\]", "", name)
        if self.accounts.__contains__(name):
            self.accounts[name].print_account_transactions()
        else:
            logging.info("User attempted to list information for account: \"%s\" which does not exist" % name)
            print("Bank account for \"%s\" does not exist. Please enter a new command." % name)

    def import_file(self, command):
        file_path = re.sub(r"Import File \[", "", command)
        file_path = re.sub(r"\]", "", file_path)
        logging.info("Importing data from \"%s\"" % file_path)
        try:
            self.import_data(DataImport(file_path))
        except:
            logging.warning("Could not import data from \"%s\"" % file_path)
            print("Could not import data from \"%s\"" % file_path)
            return
        logging.info("Data imported from \"%s\" successfully." % file_path)
        print("Data imported successfully.")

    def write_to_file(self, command):
        file_path = re.sub(r"Export File \[", "", command)
        file_path = "../output/" + re.sub(r"\]", "", file_path)
        logging.info("Exporting data to \"%s\"" % file_path)
        transactions = self.get_all_transactions()
        try:
            with open(file_path, "w", newline='') as output_file:
                writer = csv.writer(output_file, delimiter=',')
                writer.writerow(["Date", "From", "To", "Narrative", "Amount"])
                for transaction in transactions:
                    writer.writerow(transaction.list_values())
        except:
            logging.warning("Could not export data to \"%s\"" % file_path)
            print("Could not export data to \"%s\"" % file_path)
            return
        logging.info("Data exported to \"%s\" successfully." % file_path)
        print("Data exported successfully.")

    @staticmethod
    def log_invalid_command(command):
        logging.warning("User attempted to perform command: \"%s\" which is not valid." % command)
        print("Please enter a valid command such as: \"List All\"; \"List [Account]\"; \"Import File [path]\"; "
              "\"Export File [path]\"; \"end\".")

    def close_bank(self):
        self.bank_open = False
        logging.info("Bank has closed for the day.")
