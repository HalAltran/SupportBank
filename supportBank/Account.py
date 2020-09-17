import supportBank.Transaction as Transaction

from decimal import Decimal


class Account:
    def __init__(self, name: str):
        self.name = name
        self.balance = Decimal("0.00")
        self.transactions = []

    def add_transaction_from(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.balance -= transaction.amount

    def add_transaction_to(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.balance += transaction.amount

    def list_all_format(self):
        minus = ""
        if self.balance < 0:
            minus = "- "
        return "Name: %s. Balance: %s£%s." % (self.name, minus, str(self.balance.copy_abs()))

    def print_account_transactions(self):
        print("%s's transactions:" % self.name)
        for transaction in self.transactions:
            transaction.print_info()

    def sort_transactions(self):
        self.transactions.sort(key=lambda transaction: transaction.date)
