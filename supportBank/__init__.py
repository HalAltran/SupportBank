from supportBank.Bank import Bank
from supportBank.CSVData import CSVData

if __name__ == "__main__":
    bank = Bank()
    bank.parse_csv_data(CSVData("../res/Transactions2014.csv"))
    bank.parse_csv_data(CSVData("../res/DodgyTransactions2015.csv"))
    while bank.bank_open:
        user_command = input("Type command: ")
        bank.do_user_command(user_command)
    Bank.log_info("Bank has closed for the day.")
