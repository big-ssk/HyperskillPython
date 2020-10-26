from random import sample
import sqlite3

connection = sqlite3.connect('card.s3db')
cursor = connection.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS card"
               "(id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,"
               "number TEXT UNIQUE,"
               "pin TEXT,"
               "balance INTEGER DEFAULT 0);")


class SimpleBankingSystem:
    BIN = "400000"

    def main_menu(self):
        print("1. Create an account",
              "2. Log into account",
              "0. Exit", sep='\n')
        choice = input()
        if choice == "1":
            self.create_account()
        elif choice == "2":
            self.log_in()
        elif choice == "0":
            self.exit()

    def create_account(self):
        card_number = self.generate_card_number()
        pin = self.generate_pin()
        cursor.execute(f"INSERT INTO card (number, pin) VALUES ({card_number}, {pin});")
        connection.commit()
        print("\nYour card_number has been created",
              "Your card_number number:",
              f"{card_number}",
              "Your card_number PIN:",
              f"{pin}\n", sep='\n')

    def generate_card_number(self):
        while True:
            card_number = self.BIN + ''.join(map(str, (sample(range(10), 10))))
            if self.luhn_valid_card_number(card_number) and not self.card_number_exists(card_number):
                return card_number

    def luhn_valid_card_number(self, card_number):
        card_number = map(int, card_number)
        temp = [num * 2 if idx % 2 != 0 else num for idx, num in enumerate(card_number, 1)]
        if sum([num - 9 if num > 9 else num for num in temp]) % 10 == 0:
            return True
        return False

    def card_number_exists(self, card_number):
        cursor.execute('SELECT id FROM card;')
        cards = cursor.fetchall()
        if card_number in cards:
            return True
        return False

    def generate_pin(self):
        return ''.join(map(str, (sample(range(1, 10), 4))))

    def log_in(self):
        card_number = input("\nEnter your card number:\n")
        pin = input("Enter your PIN:\n")
        cursor.execute(f"SELECT number, pin FROM card WHERE number = {card_number};")
        data = cursor.fetchone()
        if (card_number, pin) != data:
            print("\nWrong card number or PIN!\n")
        else:
            print("\nYou have successfully logged in!\n")
            return self.account_menu(card_number)

    def get_balance(self, card_number):
        cursor.execute(f'SELECT balance FROM card WHERE number = {card_number};')
        balance = cursor.fetchone()
        return balance[0]

    def add_income(self, card_number):
        amount = int(input("\nEnter income:\n"))
        cursor.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {card_number};')
        connection.commit()

    def do_transfer(self, card_number, target_card, amount):
        cursor.execute(f'UPDATE card SET balance = balance - {amount} WHERE number = {card_number}')
        cursor.execute(f'UPDATE card SET balance = balance + {amount} WHERE number = {target_card}')
        connection.commit()

    def close_account(self, card_number):
        cursor.execute(f'DELETE FROM card WHERE number = {card_number};')
        connection.commit()

    def account_menu(self, card_number):
        while True:
            print("1. Balance",
                  "2. Add income",
                  "3. Do transfer",
                  "4. Close account",
                  "5. Log out",
                  "0. Exit", sep='\n')
            choice = input()
            if choice == "1":
                balance = self.get_balance(card_number)
                print(f"\nBalance: {balance}\n")
            elif choice == "2":
                self.add_income(card_number)
                print("Income was added!\n")
            elif choice == "3":
                print("\nTransfer")
                target_card = input("Enter card number:\n")
                if self.is_valid_target(card_number, target_card):
                    amount = int(input("Enter how much money you want to transfer:\n"))
                    if self.get_balance(card_number) >= amount:
                        self.do_transfer(card_number, target_card, amount)
                        print("Success!\n")
                    else:
                        print("Not enough money!")
            elif choice == "4":
                self.close_account(card_number)
                print("\nThe account has been closed!\n")
                return self.main()
            elif choice == "5":
                print("\nYou have successfully logged out!\n")
                return self.main()
            elif choice == "0":
                return self.exit()

    def is_valid_target(self, card_number, target_card):
        if card_number == target_card:
            print("You can't transfer money to the same account!")
            return False
        elif not self.luhn_valid_card_number(target_card):
            print("Probably you made a mistake in the card number. Please try again!")
            return False
        cursor.execute(f"SELECT number FROM card WHERE number = {target_card};")
        target_number = cursor.fetchone()
        if not target_number:
            print("Such a card does not exist.\n")
            return False
        return True

    def exit(self):
        exit("\nBye!")

    def main(self):
        while True:
            self.main_menu()


bank = SimpleBankingSystem()
bank.main()
connection.close()
