from supportBank.Bank import Bank
from supportBank.CSVData import CSVData

if __name__ == "__main__":
    bank = Bank()
    csv_data = CSVData("../res/Transactions2014.csv")
    bank.parse_csv_data(csv_data)
    bank.do_user_command(input("Type command: "))
