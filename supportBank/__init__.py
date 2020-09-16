from supportBank.Bank import Bank
from supportBank.DataImport import DataImport

if __name__ == "__main__":
    bank = Bank()
    bank.import_data(DataImport("../res/Transactions2014.csv"))
    bank.import_data(DataImport("../res/DodgyTransactions2015.csv"))
    bank.import_data(DataImport("../res/Transactions2013.json"))
    while bank.bank_open:
        user_command = input("Type command: ")
        bank.do_user_command(user_command)
    Bank.log_info("Bank has closed for the day.")
