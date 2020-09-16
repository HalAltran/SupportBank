import supportBank.Account as Account

from decimal import Decimal
from datetime import datetime


class Transaction:
    def __init__(self, date: datetime, account_from: Account, account_to: Account, narrative: str, amount: Decimal):
        self.date = date
        self.account_from = account_from
        self.account_to = account_to
        self.narrative = narrative
        self.amount = amount

    def list_info(self):
        return "Date: %s. From %s. To %s. Narrative: %s. Amount: %s" % (self.list_values())

    def list_values(self):
        return self.date.strftime("%d/%m/%Y"), self.account_from.name, self.account_to.name, self.narrative, str(self.amount)
