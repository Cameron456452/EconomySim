from classes import *

John = Pop("John", 0, "Lumberjack")
Smith = Pop("Smith", 0, "Farmer")
Bob = Pop("Bob", 0, "Blacksmith")
Jill = Pop("Jill", 200, "Blacksmith")

popList = [John, Smith, Bob, Jill]
market = []
prices = [3, 5, 10, 30] # Needs updating if adding new good
itemNames = ["Grain", "Wood", "Iron", "Computer"] # Needs updating if adding new good

John.inventory = ["Wood", "Wood", "Wood", "Wood", "Wood", "Wood", "Wood", "Wood", "Wood"]
Smith.inventory = ["Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain", "Grain"]
Bob.inventory = ["Iron", "Iron", "Iron", "Iron", "Iron", "Iron", "Iron", "Iron", "Iron", "Iron", "Iron", "Computer", "Computer", "Computer"]

# Attempts to sell an item
# Returns true if they have the item and sold it
# Returns false if they do not have the item and didn't sell it
def sell(seller, item, value):
    index = doesPersonHave(seller, item)
    if index != -1:
        seller.inventory.pop(index)
        seller.balance += value
        # print(f"{seller.name} sold {item}")
        # market.append(item)
        return True
    else:
        print("Does not have the item")
        return False

# Similar to sell, but doesn't give the money for the transaction, just merely adds it to market
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
def buy(buyer, item, value):
    index = findMarketItem(item)
    if index == -1:
        # print(f"{item} not on the market")
        return False

    if buyer.balance >= value:
        buyer.inventory.append(item)
        buyer.balance -= value
        market.pop(index)
        # print(f"{buyer.name} bought {item}")
        return True
    else:
        print(f"{buyer.name} does not have the funds to buy {item}")
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

        if demandList[i] == 0:
            prices[i] = 0

        elif supplyList[i] > demandList[i]:
            prices[i] /= (supplyList[i]/demandList[i])
        else:
            prices[i] *= 1 + ((demandList[i] - supplyList[i])/supplyList[i])

        prices[i] = round(prices[1], 2)

def main():
    iDemands = [] # Individual Demands
    for i in range(len(popList)):
        consume(popList[i]) # Consumes what they have
        iDemands.append(popList[i].doesNotHave) # Appends needs onto another list

    supplyList = calcSupply(market) # Generates supply list
    demandList = calcDemand(iDemands) # Generates demand list
    updatePrices(supplyList, demandList) # Updates prices based on supply and demand

    for i in range(len(popList)):
        j = 0
        while (len(popList[i].inventory)) > 0: # Sells entire inventory
            sell(popList[i], popList[i].inventory[j], findValue(popList[i].inventory[j]))

    for i in range(len(popList)): # Buys goods needed
        buyNeededGoods(popList[i])

    for i in range(len(popList)): # Prints final balances
        print(f"{popList[i].name} Balance ${popList[i].balance}")

main()