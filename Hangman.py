from random import choice
from string import ascii_lowercase


class Hangman:
    words = ('python', 'java', 'kotlin', 'javascript')

    messages = {"start": 'H A N G M A N' + "\n",
                "wrong_letter": "No such letter in the word",
                "dry": "You already typed this letter",
                "win": "You guessed the word!" + "\n" + "You survived!",
                "lose": "You lost!",
                "not_ascii": "It is not an ASCII lowercase letter",
                "wrong_length": "You should input a single letter"}

    def __init__(self):
        self.guessed_word = choice(self.words)
        self.masked_word = '-' * len(self.guessed_word)
        self.letters = set(self.guessed_word)
        self.tried_letters = set()
        self.tries = 8
        print(Hangman.messages.get("start"))

    def main(self):
        user_choice = input('Type "play" to play the game, "exit" to quit: ')
        if user_choice == "play":
            self.run()

    def is_correct_input(self, guess):
        if guess and len(guess) > 1:
            print(self.messages.get("wrong_length"))
            return False
        elif guess not in ascii_lowercase:
            print(self.messages.get("not_ascii"))
            return False
        elif self.already_guessed(guess):
            print(self.messages.get("dry"))
            return False
        return True

    def output(self):
        print()
        print(self.masked_word)

    def letter_exists(self, guess):
        if guess in self.guessed_word:
            return True
        return False

    def already_guessed(self, guess):
        if guess in self.tried_letters:
            return True
        return False

    def unmask_letter(self, guess):
        self.letters.discard(guess)
        self.masked_word = ''.join([i if i not in self.letters else '-' for i in self.guessed_word])

    def is_solved(self):
        if '-' in self.masked_word:
            return False
        return True

    def run(self):
        while self.tries > 0:
            self.output()
            guess = input("Input a letter: ")
            if not self.is_correct_input(guess):
                continue
            self.tried_letters.add(guess)
            if self.letter_exists(guess):
                self.unmask_letter(guess)
            else:
                print(self.messages.get("wrong_letter"))
                self.tries -= 1
        if self.is_solved():
            print(self.messages.get("win"))
        else:
            print(self.messages.get("lose"))


game = Hangman()
game.main()
