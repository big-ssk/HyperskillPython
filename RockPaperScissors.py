from random import choice


class RockPaperScissors:
    default_options = {"rock": "paper",
                       "paper": "scissors",
                       "scissors": "rock"}

    def __init__(self):
        self.username = None
        self.ratings = {}
        self.options = {}

    def main(self):
        self.initialize_game_settings()
        print("Okay, let's start")
        while True:
            user_choice = input()
            if self.is_correct_input(user_choice):
                pc_choice = choice(list(self.options.keys()))
                self.evaluate_results(user_choice, pc_choice)

    def initialize_game_settings(self):
        self.read_saved_ratings()
        self.set_username()
        self.ratings.setdefault(self.username, 0)
        self.set_options()

    def read_saved_ratings(self):
        with open('rating.txt') as file:
            for line in file:
                user, rating = line.split()
                self.ratings[user] = int(rating)

    def set_username(self):
        self.username = input("Enter your name: ")
        print("Hello,", self.username)

    def set_options(self):
        options = input()
        if not options:
            self.options = RockPaperScissors.default_options
        else:
            options = options.split(',')
            for item in options:
                item_index = options.index(item)
                tmp = options[item_index + 1:] + options[:item_index]
                self.options[item] = tmp[:len(tmp) // 2]

    def is_correct_input(self, user_choice):
        if user_choice == '!exit':
            exit("Bye!")
        elif user_choice == '!rating':
            print(self.ratings.get(self.username))
            return False
        elif not self.options.get(user_choice):
            print("Invalid input")
            return False
        return True

    def evaluate_results(self, user_choice, pc_choice):
        if user_choice == pc_choice:
            print(f"There is a draw ({pc_choice})")
            self.ratings[self.username] += 50
        elif pc_choice in self.options.get(user_choice):
            print(f"Sorry, but the computer chose {pc_choice}")
        else:
            print(f"Well done. The computer chose {pc_choice} and failed")
            self.ratings[self.username] += 100


game = RockPaperScissors()
game.main()
