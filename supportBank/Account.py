import supportBank.Transaction as Transaction


class Account:
    def __init__(self, name: str):
        self.name = name
        self.balance = 0
        self.transactions = []

    def add_transaction_from(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.balance -= transaction.amount

    def add_transaction_to(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.balance += transaction.amount

    def list_all_format(self):
        return "Name: " + self.name + ". Balance: " + str(self.balance)

    def list_account(self):
        print(self.name + " transactions:")
        for transaction in self.transactions:
            print(transaction.list_info())

    def sort_transactions(self):
        self.transactions.sort(key=lambda transaction: transaction.date)
