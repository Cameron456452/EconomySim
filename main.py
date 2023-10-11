from classes import *
import random
import math
import time
import statistics

# John = Pop("John", 0, "Lumberjack")
# Smith = Pop("Smith", 0, "Farmer")
# Bob = Pop("Bob", 0, "Blacksmith")
# Jill = Pop("Jill", 200, "Engineer")

popList = []
market = []
basePrices = [3, 5, 10, 30]
prices = [3, 5, 10, 30] # Needs updating if adding new good
itemNames = ["Grain", "Wood", "Iron", "Computer"] # Needs updating if adding new good
jobList = ["Farmer", "Lumberjack", "Blacksmith", "Engineer"]
consumptionTax = 0
govBalance = 0
interestRate = 0.12

for i in range(100):
    popList.append(Pop(i, 15, random.choice(jobList)))

# Attempts to sell an item
# Returns true if they have the item and sold it
# Returns false if they do not have the item and didn't sell it
def sell(seller, item, value):
    index = doesPersonHave(seller, item)
    if index != -1:
        seller.inventory.pop(index)
        seller.balance += value
        seller.income += value
        return True
    else:
        print("Does not have the item")
        return False

# Similar to sell, but doesn't give the money for the transaction, just merely adds it to market
# As a note, this does not remove it from their inventory, sell does that. This just calculates demand
# And gets the market with the goods it has
def sendToMarket(seller, item):
    index = doesPersonHave(seller, item)
    if index != -1:
        market.append(item)
        return True
    else:
        print("Does not have the item")
        return False

# Attempts to buy an item from the market
# Returns true if successful
# Returns false if unable to buy the item
def buy(buyer, item, value, force=False):
    global govBalance

    index = findMarketItem(item)
    if index == -1:
        # print(f"{item} not on the market")
        return False

    if buyer.balance >= value or force:
        buyer.inventory.append(item)
        buyer.balance -= value*(1+consumptionTax)
        govBalance += value*consumptionTax
        market.pop(index)
        # print(f"{buyer.name} bought {item}")
        return True
    else:
        # print(f"{buyer.name} does not have the funds to buy {item}")
        return False

# Person tries to consume everything they need
# If they can't, then they add it to doesNotHave and tries to buy it later
def consume(person):
    i = 0
    while i < len(person.needs):
        index = doesPersonHave(person, person.needs[i])
        if index != -1:
            person.inventory.pop(index)
            person.needs.pop(i)
        else:
            person.doesNotHave.append(person.needs[i])
            i += 1

    for j in range(len(person.inventory)):
        sendToMarket(person, person.inventory[j])
    random.shuffle(market) # Randomly shuffles items so no one item has priority

# Attempts to buy needed goods, if they can't it skips to the next thing they need
def buyNeededGoods(person):
    i = 0
    while i < len(person.doesNotHave):
        if buy(person, person.doesNotHave[i], findValue(person.doesNotHave[i])):
            person.doesNotHave.pop(i)
        else:
            i += 1

# Sees if person has an item
# Returns the index in their inventory if they do
# Returns -1 if they do not have it
def doesPersonHave(person, item):
    for i in range(len(person.inventory)):
        if person.inventory[i] == item:
            return i

    return -1

# Finds the price of an item on the market
# Returns the price found on the market
def findValue(good):
    for i in range(len(prices)):
        if itemNames[i] == good:
            return prices[i]

    return -1

# Finds the item in the market
# Returns the index of where the item was found on the market
def findMarketItem(good):
    for i in range(len(market)):
        if market[i] == good:
            return i

    return -1

# Generates the supply of each item on the market
# Returns a list in the order of itemNames
def calcSupply(market):
    supplyList = [0] * len(itemNames)
    for i in range(len(market)):
        supplyList[findItemList(market[i])] += 1

    return supplyList

# Finds what index an item is on the list of items to be sold (itemNames)
# Returns the index found at. (-1 if it isn't there)
def findItemList(item):
    for i in range(len(itemNames)):
        if item == itemNames[i]:
            return i

# Generates the demand of each item on the market
# Loops over a 2D list (each list being a pops needs aka demand) to figure out the demand
# Returns a list in the order of itemNames
def calcDemand(iDemands):
    demandList = [0] * len(itemNames)
    for i in range(len(iDemands)):
        for j in range(len(iDemands[i])):
            demandList[findItemList(iDemands[i][j])] += 1

    return demandList

# Updates prices based on demand
def updatePrices(supplyList, demandList):
    for i in range(len(supplyList)):
        if supplyList[i] == 0:
            prices[i] = 999
        elif demandList[i] == 0:
            prices[i] = 0
        elif supplyList[i] > demandList[i]:
            prices[i] /= min(supplyList[i]/demandList[i], 4)
        else:
            prices[i] *= 1 + min((demandList[i] - supplyList[i])/supplyList[i], 0.75)

        prices[i] = round(prices[i], 2)

# Makes pops produce goods based on their job
# Returns nothing
def produce(person):
    if person.job == "Farmer":
        for i in range(5):
            person.inventory.append(Good("Grain", person))

    if person.job == "Lumberjack":
        for i in range(5):
            person.inventory.append(Good("Wood", person))

    if person.job == "Blacksmith":
        for i in range(5):
            person.inventory.append(Good("Iron", person))

    if person.job == "Engineer":
        for i in range(5):
            person.inventory.append(Good("Computer", person))

# Gives facts about the market
# Returns nothing
def marketUpdate(supplyList, demandList):
    for i in range(len(prices)):
        print(f"{itemNames[i]}: ${prices[i]} Supply: {supplyList[i]} Demand: {demandList[i]}")
    print()

# Generates facts about the population
# Returns nothing
def popStats(popList):
    GDP = 0
    moneySupply = 0
    totalDebt = 0
    jobCount = [0, 0, 0, 0]
    jobIncomes = [0, 0, 0, 0]

    for pop in popList:
        GDP += round(pop.income, 2)
        moneySupply += round(pop.balance, 2)
        totalDebt += pop.debt

        if pop.job == "Farmer":
            jobCount[0] += 1
            jobIncomes[0] += pop.income

        elif pop.job == "Lumberjack":
            jobCount[1] += 1
            jobIncomes[1] += pop.income

        elif pop.job == "Blacksmith":
            jobCount[2] += 1
            jobIncomes[2] += pop.income

        elif pop.job == "Engineer":
            jobCount[3] += 1
            jobIncomes[3] += pop.income

    gdpCapita = round(GDP/len(popList), 2)
    avBal = round(moneySupply / len(popList), 2)
    avDebt = round(totalDebt / len(popList), 2)

    print(f"GDP ${GDP}")
    print(f"Money Supply ${moneySupply}")
    print(f"GDP per capita ${gdpCapita}")
    print(f"Average Balance ${avBal}")
    print(f"Government Balance ${govBalance}")
    print(f"Total debt ${totalDebt}")
    print(f"Average debt balance ${avDebt}")
    print()

    for i in range(len(jobCount)):
        if jobCount[i] > 0:
            print(f"{jobList[i]}: {jobCount[i]} jobs, Average Income: ${round(jobIncomes[i]/jobCount[i], 2)}")
        else:
            print(f"No one works as a {jobList[i]}")

    print()
    swapJobs(popList, gdpCapita, avBal, jobIncomes)

# Gives a chance a pop will switch jobs based on how well they're doing financially
# Returns nothing
def swapJobs(popList, gdpCapita, avBal, jobIncomes):
    jobWeights = []
    for i in range(len(jobList)):
        jobWeights.append(prices[i] / basePrices[i])

    for i in range(len(popList)):
        incomeHappy = popList[i].income / gdpCapita
        balHappy = popList[i].income / avBal
        happiness = (incomeHappy + balHappy) / 2

        if happiness < random.random()*5 and random.random() < 0.4:
            popList[i].job = random.choices(jobList, weights=jobWeights, k=1)

# Does one iteration of a market cycle
# Returns nothing
def marketLoop(popList):
    for i in range(len(popList)):  # Produces goods
        produce(popList[i])

    iDemands = []  # Individual Demands
    for i in range(len(popList)):
        consume(popList[i])  # Consumes what they have
        iDemands.append(popList[i].doesNotHave)  # Appends needs onto another list

    supplyList = calcSupply(market)  # Generates supply list
    demandList = calcDemand(iDemands)  # Generates demand list
    updatePrices(supplyList, demandList)  # Updates prices based on supply and demand

    for i in range(len(popList)):
        j = 0
        while (len(popList[i].inventory)) > 0:  # Sells entire inventory
            sell(popList[i], popList[i].inventory[j], findValue(popList[i].inventory[j]))

    for i in range(len(popList)):  # Buys goods needed
        buyNeededGoods(popList[i])

    buyBackMarketGoods(popList)
    marketUpdate(supplyList, demandList)
    popStats(popList)
    resetNeeds(popList)

# Forcefully buys back goods that were not sold on the market
def buyBackMarketGoods(popList):
    global market

    while market: # Tests if it isn't empty
        owner = market[0].owner
        index = findPerson(popList, owner)
        popList[index].inventory.append(market[0])
        if not buy(popList[index], market[0], findValue(market[0]), force=True):
            print("Failure")

# Finds a person in popList
def findPerson(popList, name):
    for i in range(len(popList)):
        if popList[i] == name:
            return i

    return -1

# Gives pops back their needs
def resetNeeds(popList):
    for i in range(len(popList)):
        popList[i].needs = ["Wood", "Wood", "Grain", "Grain", "Grain", "Iron", "Computer"]
        popList[i].doesNotHave = []
        popList[i].income = 0

        if popList[i].debt > 0:
            popList[i].debt *= (1+interestRate)

        if popList[i].balance < 0:
            popList[i].debt += math.ceil(popList[i].balance*-1)
            popList[i].balance += math.ceil(popList[i].balance*-1)

        if popList[i].balance > 0 and popList[i].debt > 0:
            popList[i].debt -= min(math.floor(popList[i].balance), popList[i].debt)
            popList[i].balance -= min(math.floor(popList[i].balance), popList[i].debt)

def main():
    for i in range(5):
        marketLoop(popList)

main()