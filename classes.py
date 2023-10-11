class Pop:
    def __init__(self, name, balance=0, job="Unemployed"):
        self.balance = balance
        self.inventory = []
        self.name = name
        self.needs = ["Wood", "Wood", "Grain", "Grain", "Grain", "Iron", "Computer"]
        self.doesNotHave = []
        self.job = job
        self.income = 0

    def __str__(self):
        return f"{self.name}: {self.occupation}, Balance: ${self.balance}"
