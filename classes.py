class Pop:
    def __init__(self, name, balance=0, occupation="Unemployed"):
        self.balance = balance
        self.inventory = []
        self.name = name
        self.needs = ["Wood", "Wood", "Grain", "Grain", "Grain", "Iron"]
        self.doesNotHave = []
        self.occupation = occupation

    def __str__(self):
        return f"{self.name}: {self.occupation}, Balance: ${self.balance}"
