from classes import *
import random
import math

popList = []
market = []
basePrices = [3, 5, 10, 30]
prices = [3, 5, 10, 30]  # Needs updating if adding new good
itemNames = ["Grain", "Wood", "Iron", "Computer"]  # Needs updating if adding new good
jobList = ["Farmer", "Lumberjack", "Blacksmith", "Engineer"]
consumptionTax = 0.05
govBalance = 0
interestRate = 0.12

for p in range(100):
    popList.append(Pop(p, 15, random.choice(jobList)))

# Attempts to sell an item
# Note: it doesn't add anything to the market, sendToMarket does that
# Returns true if they have the item and sold it
# Returns false if they do not have the item and didn't sell it
def sell(seller, item, value):
    index = findInList(seller.inventory, item)
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
    index = findInList(seller.inventory, item)
    if index != -1:
        if str(item): # Double checks to make sure the good is a Good object not a string
            item = Good(item, seller)

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

    index = findInList(market, item)
    if index == -1:
        # print(f"{item} not on the market")
        return False

    if buyer.balance >= value or force:
        buyer.inventory.append(item)

        if not force: # Voluntary purchase, so has consumption taxes
            buyer.balance -= value * (1 + consumptionTax)
            govBalance += value * consumptionTax
        else: # Involuntary buy back due to not being sold, pretend never on the market, so no tax
            buyer.balance -= value
            govBalance += value

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
    while person.needs:
        index = findInList(person.inventory, person.needs[i])
        if index != -1:
            person.inventory.pop(index)
            person.needs.pop(i)
        else:
            person.doesNotHave.append(person.needs[i])
            person.needs.pop(i)

    for j in range(len(person.inventory)):
        sendToMarket(person, person.inventory[j])
    random.shuffle(market)  # Randomly shuffles items so no one item has priority


# Attempts to buy needed goods, if they can't it skips to the next thing they need
def buyNeededGoods(person):
    i = 0
    while i < len(person.doesNotHave):
        if buy(person, person.doesNotHave[i], findValue(person.doesNotHave[i])):
            person.doesNotHave.pop(i)
        else:
            i += 1

    if not person.doesNotHave and person.status < 3:
        person.doesNotHave = ["Grain", "Grain", "Wood", "Wood", "Iron", "Iron", "Iron", "Computer", "Computer"]
        person.status += 1
        buyNeededGoods(person)

    while person.doesNotHave and person.status > 0:
        removeGoods = ["Grain", "Grain", "Wood", "Wood", "Iron", "Iron", "Iron", "Computer", "Computer"]
        person.status -= 1
        for goods in removeGoods:
            index = findInList(person.doesNotHave, goods)
            if person.doesNotHave and index >= 0:
                person.doesNotHave.pop(index)
            elif person.doesNotHave:
                break

# Tries to find a value in a list
# Returns the index it was found at
# Returns -1 if it was not found
def findInList(list, value):
    for i in range(len(list)):
        if list[i] == value:
            return i

    return -1


# Finds the price of an item on the market
# Returns the price found on the market
def findValue(good):
    for i in range(len(prices)):
        if itemNames[i] == good:
            return prices[i]

    return -1


# Generates the supply of each item on the market
# Returns a list in the order of itemNames
def calcSupply(market):
    supplyList = [0] * len(itemNames)
    for i in range(len(market)):
        supplyList[findInList(itemNames, market[i])] += 1

    return supplyList


# Generates the demand of each item on the market
# Loops over a 2D list (each list being a pops needs aka demand) to figure out the demand
# Returns a list in the order of itemNames
def calcDemand(iDemands):
    demandList = [0] * len(itemNames)
    for i in range(len(iDemands)):
        for j in range(len(iDemands[i])):
            demandList[findInList(itemNames, iDemands[i][j])] += 1

    return demandList


# Updates prices based on demand
def updatePrices(supplyList, demandList):
    for i in range(len(supplyList)):
        if supplyList[i] == 0:
            prices[i] = 999
        elif demandList[i] == 0:
            prices[i] = 0
        elif supplyList[i] > demandList[i]:
            prices[i] = basePrices[i] / min(supplyList[i] / demandList[i], 4)
        else:
            prices[i] = basePrices[i] * 1 + min((demandList[i] - supplyList[i]) / supplyList[i], 3)

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
        for i in range(3):
            person.inventory.append(Good("Iron", person))

    if person.job == "Engineer":
        for i in range(2):
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
    incomeList = []
    classList = [0] * 12

    for pop in popList:
        GDP += round(pop.income, 2)
        moneySupply += round(pop.balance, 2)
        totalDebt += pop.debt
        incomeList.append(pop.income)
        classList[pop.status] += 1

    incomeList.sort()
    gdpCapita = round(GDP / len(popList), 2)
    avBal = round(moneySupply / len(popList), 2)
    avDebt = round(totalDebt / len(popList), 2)

    print(classList)

    print(f"GDP ${GDP}")
    print(f"Money Supply ${moneySupply}")

    print(f"\nGDP per capita ${gdpCapita}")
    print(f"Poorest person ${incomeList[0]}")
    print(f"Richest Person ${incomeList[len(incomeList) - 1]}")

    print(f"\nAverage Balance ${avBal}")
    print(f"Government Balance ${govBalance}")

    print(f"\nTotal debt ${totalDebt}")
    print(f"Average debt balance ${avDebt}")
    print()

    # for i in range(len(jobCount)):
    #     if jobCount[i] > 0:
    #         print(f"{jobList[i]}: {jobCount[i]} jobs, Average Income: ${round(jobIncomes[i] / jobCount[i], 2)}")
    #     else:
    #         print(f"No one works as a {jobList[i]}")

    print()
    swapJobs(popList, gdpCapita, avBal)


# Gives a chance a pop will switch jobs based on how well they're doing financially
# Returns nothing
def swapJobs(popList, gdpCapita, avBal):
    jobWeights = []
    for i in range(len(jobList)):
        jobWeights.append(prices[i] / basePrices[i])

    for i in range(len(popList)):
        incomeHappy = popList[i].income / gdpCapita
        balHappy = popList[i].income / avBal
        happiness = (incomeHappy + balHappy) / 2

        if popList[i].doesNotHave:
            happiness -= 2

        if happiness < random.random() * 5 and random.random() < 0.4:
            popList[i].job = random.choices(jobList, weights=jobWeights, k=1)[0]


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

    buyBackMarketGoods(popList)  # Forces them to take back any goods not sold
    marketUpdate(supplyList, demandList)  # Prints prices of goods in the economy
    popStats(popList)  # Prints stats about the economy
    resetNeeds(popList)  # Resets everyones needs


# Forcefully buys back goods that were not sold on the market
def buyBackMarketGoods(popList):
    global market

    while market:  # Tests if it isn't empty
        owner = market[0].owner
        index = findInList(popList, owner)
        popList[index].inventory.append(market[0])
        if not buy(popList[index], market[0], findValue(market[0]), force=True):
            print("Failure")


# Gives pops back their needs
def resetNeeds(popList):
    for i in range(len(popList)):
        popList[i].needs = ["Wood", "Wood", "Grain", "Grain", "Grain", "Iron", "Computer"]
        for i in range(popList[i].status):
            popList[i].needs += ["Grain", "Grain", "Wood", "Wood", "Iron", "Iron", "Iron", "Computer", "Computer"]

        popList[i].doesNotHave = []
        popList[i].income = 0

        if popList[i].debt > 0:
            popList[i].debt *= (1 + interestRate)

        if popList[i].balance < 0:
            popList[i].debt += math.ceil(popList[i].balance * -1)
            popList[i].balance += math.ceil(popList[i].balance * -1)

        if popList[i].balance > 0 and popList[i].debt > 0:
            popList[i].debt -= min(math.floor(popList[i].balance), popList[i].debt)
            popList[i].balance -= min(math.floor(popList[i].balance), popList[i].debt)


def main():
    for i in range(5):
        marketLoop(popList)


main()
