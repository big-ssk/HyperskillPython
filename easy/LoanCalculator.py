from math import ceil, log


class LoanCalculator:

    def __init__(self):
        self.__loan_principal = None
        self.__number_of_periods = None
        self.__loan_interest = None
        self.__monthly_payment = None
        self.__total_payment = 0

    def set_loan_principal(self):
        self.__loan_principal = int(input("Enter the loan principal:\n"))

    def set_number_of_periods(self):
        self.__number_of_periods = int(input("Enter the number of periods:\n"))

    def set_loan_interest(self):
        self.__loan_interest = float(input("Enter the loan interest:\n")) / (12 * 100)

    def set_monthly_payment(self):
        self.__monthly_payment = float(input("Enter the monthly payment:\n"))

    def main(self):
        choice = input('What do you want to calculate?\n'
                       'type "n" - for number of monthly payments,\n'
                       'type "a" for annuity monthly payment amount,\n'
                       'type "p" - for loan principal:\n')

        if choice == 'n':
            self.set_loan_principal()
            self.set_monthly_payment()
            self.set_loan_interest()
            self.calculate_number_of_monthly_payments(self.__loan_principal, self.__monthly_payment,
                                                      self.__loan_interest)
        elif choice == 'a':
            self.set_loan_principal()
            self.set_number_of_periods()
            self.set_loan_interest()
            self.calculate_annuity_monthly_payment_amount(self.__loan_principal, self.__number_of_periods,
                                                          self.__loan_interest)
        else:
            self.set_monthly_payment()
            self.set_number_of_periods()
            self.set_loan_interest()
            self.calculate_loan_principal(self.__monthly_payment, self.__number_of_periods, self.__loan_interest)

    def calculate_loan_principal(self, payment, periods, rate):
        principal = payment / ((rate * (1 + rate) ** periods) / ((1 + rate) ** periods - 1))
        print(f"Your loan principal = {principal}!")

    def calculate_number_of_monthly_payments(self, principal, payment, rate):
        months = ceil(log((payment / (payment - rate * principal)), rate + 1))
        years, months = divmod(months, 12)
        if years and months:
            print(f"It will take {years} {'year' if years == 1 else 'years'} and "
                  f"{months} {'month' if months == 1 else 'months'} to repay this loan!")
        elif not years:
            print(f"It will take {months} {'month' if months == 1 else 'months'} to repay the loan")
        else:
            print(f"It will take {years} {'year' if years == 1 else 'years'} to repay this loan!")

    def calculate_annuity_monthly_payment_amount(self, principal, periods, rate):
        payment = ceil(principal * ((rate * (1 + rate) ** periods) / (((1 + rate) ** periods) - 1)))
        print(f"Your monthly payment = {payment}!")

    def calculate_differentiated_payment(self, principal, periods, rate):
        total = 0
        for month in range(1, periods + 1):
            payment = ceil(principal / periods + rate * (principal - (principal * (month - 1)) / periods))
            total += payment
            print(payment)
        print(total - principal)


loan_calculator = LoanCalculator()
loan_calculator.main()
