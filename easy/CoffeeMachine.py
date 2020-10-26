class CoffeeMachine:
    # read "coffee" as "cups"
    ingredients_per_cup = {1: {"water": 250, "milk": 0, "coffee beans": 16, "coffee": 1, "money": 4},
                           2: {"water": 350, "milk": 75, "coffee beans": 20, "coffee": 1, "money": 7},
                           3: {"water": 200, "milk": 100, "coffee beans": 12, "coffee": 1, "money": 6}}
    ingredient_units = {"water": "ml", "milk": "ml", "coffee beans": "grams", "coffee": "disposable cups"}
    ingredients_stored = {"water": 400, "milk": 540, "coffee beans": 120, "coffee": 9, "money": 550}

    def main(self):
        while True:
            action = input("Write action (buy, fill, take, remaining, exit):\n")
            eval(f"self.{action}()")
            print()

    def buy(self):
        choice = input("What do you want to buy? 1 - espresso, 2 - latte, 3 - cappuccino, back - to main menu:\n")
        if choice == "back":
            print()
            return self.main()
        choice = int(choice)
        for item, amount in self.ingredients_per_cup[choice].items():
            if item == "money":
                self.ingredients_stored[item] += amount
            elif self.ingredients_stored[item] >= self.ingredients_per_cup[choice][item]:
                self.ingredients_stored[item] -= amount
            else:
                print(f"Sorry, not enough {item}!")
                break
        else:
            print("I have enough resources, making you a coffee!")

    def take(self):
        print(f'I gave you ${self.ingredients_stored["money"]}')
        self.ingredients_stored["money"] = 0

    def fill(self):
        for ingredient, units in self.ingredient_units.items():
            amount = int(input(f"Write how many {units} of {ingredient} do you want to add:\n"))
            self.ingredients_stored[ingredient] += amount

    def exit(self):
        exit()

    def remaining(self):
        print("The coffee machine has:")
        for item, amount in self.ingredients_stored.items():
            if item == "coffee":
                item = "disposable cups"
            elif item == "money":
                amount = f"${amount}"
            print(f"{amount} of {item}")


coffee_machine = CoffeeMachine()
coffee_machine.main()
