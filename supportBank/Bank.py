from decimal import Decimal
from supportBank import CSVData
from supportBank.Account import Account
from supportBank.Transaction import Transaction


class Bank:
    def __init__(self):
        self.accounts = {}

    def parse_csv_data(self, csv_data: CSVData):
        name_set = set()
        for row in csv_data.rows:
            name_set.add(row.get_entry("From"))
            name_set.add(row.get_entry("To"))
        for name in name_set:
            self.accounts[name] = Account(name)
        for row in csv_data.rows:
            self.create_transaction(row.get_entry("Date"), row.get_entry("From"), row.get_entry("To"),
                                    row.get_entry("Narrative"), Decimal(row.get_entry("Amount")))

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
