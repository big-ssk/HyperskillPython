class SimpleChattyBot:

    def __init__(self, bot_name, year_of_creation):
        self.name = bot_name
        self.year_of_creation = year_of_creation

    def greet(self):
        print(f'Hello! My name is {self.name}.')
        print(f'I was created in {self.year_of_creation}.')

    def remind_name(self):
        print('Please, remind me your name.')
        name = input()
        print(f'What a great name you have, {name}!')

    def guess_age(self):
        print('Let me guess your age.')
        print('Enter remainders of dividing your age by 3, 5 and 7.')
        rem3 = int(input())
        rem5 = int(input())
        rem7 = int(input())
        age = (rem3 * 70 + rem5 * 21 + rem7 * 15) % 105
        print(f"Your age is {age}: that's a good time to start programming!")

    def count(self):
        print('Now I will prove to you that I can count to any number you want.')
        num = int(input())
        curr = 0
        while curr <= num:
            print(curr, '!')
            curr = curr + 1

    def test(self):
        print("Let's test your programming knowledge.")
        question = "Why do we use methods?\n"
        options = {1: "To repeat a statement multiple times.",
                   2: "To decompose a program into several small subroutines.",
                   3: "To determine the execution time of a program.",
                   4: "To interrupt the execution of a program."}
        for num, text in options.items():
            print(f'{num}. {text}')
        choice = int(input(question))
        while choice != 4:
            choice = int(input("Please, try again."))
        print('Completed, have a nice day!')

    def end(self):
        print('Congratulations, have a nice day!')

    def main(self):
        order_of_methods = ["greet", "remind_name", "guess_age", "count", "test", "end"]
        for method in order_of_methods:
            eval(f"self.{method}()")


bot = SimpleChattyBot('Aid', '2020')
bot.main()
