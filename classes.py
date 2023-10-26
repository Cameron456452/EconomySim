import random

class Pop:
    def __init__(self, name, balance=0, job="Unemployed"):
        self.balance = balance
        self.inventory = []
        self.name = name
        self.needs = ["Wood", "Wood", "Grain", "Grain", "Grain", "Iron", "Computer"]
        self.doesNotHave = []
        self.job = job
        self.income = 0
        self.debt = 0
        self.status = 0
        self.happiness = 0

        baseIdeology = random.gauss(random.choice([-4, 4]), 2)
        self.x = random.gauss(baseIdeology, 4)
        self.y = random.gauss(baseIdeology, 4)
        self.vote = None

    def __str__(self):
        return f"{self.name}: {self.job}, Balance: ${self.balance}"

# Uses govEconomy.py
class EconPop:
    def __init__(self, income=0):
        self.income = income
        self.paidTaxes = 0
        self.netWorth = 0
        self.consumption = 0
        self.happiness = 0
        self.oldIncomes = []

        baseIdeology = random.gauss(random.choice([-4, 4]), 2)
        self.x = random.gauss(baseIdeology, 4)
        self.y = random.gauss(baseIdeology, 4)

class Good:
    def __init__(self, name, owner):
        self.name = name
        self.owner = owner

    def __eq__(self, other):
        return self.name == other

class Party:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.votes = 0
        self.seats = 0

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name

class Politician:
    def __init__(self, party, name="Joe"):
        self.name = name
        self.party = party
        self.x = random.gauss(party.x, 0.8)
        self.y = random.gauss(party.y, 0.8)
        self.votes = 0
        self.job = "MP"

    def __str__(self):
        return f"{self.name}: {self.job} ({round(self.x, 1)}, {round(self.y, 1)})"

    def __eq__(self, other):
        return self.name == other.name

class Issue:
    def __init__(self, x, y, name="Issue"):
        self.x = x
        self.y = y
        self.name = name

    def __str__(self):
        return f"{self.x}, {self.y}"