import numpy as np
import math
import statistics
from classes import *
from politics import *

# Creates the income list the pops will all have
def createIncomeList(avIncome, desiredGini, population):
    incomes = np.random.lognormal(math.log(avIncome, math.e), 0, population)
    incomes.sort()

    gini = -1
    std = 1
    usedAvIncome = avIncome
    while round(gini, 3) != round(desiredGini, 3):
        incomes = np.random.lognormal(math.log(usedAvIncome, math.e), std, math.ceil(population*0.999))

        for i in range(math.floor(population * 0.001)):
            incomes = np.append(incomes, np.random.lognormal(math.log(usedAvIncome*50, math.e), std, 1))

        incomes.sort()

        area = 0
        incomeSum = sum(incomes)
        incomeSoFar = 0
        for i in range(population):
            incomeSoFar += incomes[i]
            area += (1/population)*(incomeSoFar/incomeSum)

        gini = area/0.5

        if round(gini, 3) == round(desiredGini, 3):
            pass
        elif desiredGini > gini:
            std -= desiredGini/10
        else:
            std += desiredGini/10

    divisor = statistics.mean(incomes) / avIncome
    for i in range(population):
        incomes[i] /= divisor

    return incomes

# Creates econ pops
# Returns a list of econ pops
def createEconPops(incomeList):
    popList = []

    for i in range(len(incomeList)):
        if random.random() > 0.5:
            popList.append(EconPop(incomeList[i]))
        else:
            popList.append(EconPop(0))

    return popList


# Has the pops pay their taxes
def payIncomeTaxes(popList, Issue):
    avIncome = 50000
    taxRates = [0.1, 0.12, 0.22, 0.24, 0.32, 0.35, 0.37]

    if Issue.x > 0:
        taxHike = Issue.x/10 + 1
    elif Issue.x < 0:
        taxHike = -0.1 * Issue.x + 1
    else:
        taxHike = 1

    for i in range(len(taxRates)):
        taxRates[i] *= taxHike

    taxMaxes = [avIncome*0.2, avIncome*0.8, avIncome*1.6, avIncome*3.2, avIncome*0.2, avIncome*0.4, avIncome*10, 9999999999]
    totalIncomeTax = 0
    payrollTax = 0.15

    for pop in popList:
        tax = 0.0
        remaining_income = pop.income

        for i in range(1, len(taxMaxes)):
            if remaining_income <= 0:
                break

            bracket_min = taxMaxes[i - 1]
            bracket_max = taxMaxes[i]

            taxable_income_in_bracket = min(remaining_income, (bracket_max - bracket_min))
            tax += taxable_income_in_bracket * taxRates[i - 1]
            remaining_income -= taxable_income_in_bracket

        pop.paidTaxes += min(pop.income*payrollTax, 160000*payrollTax)/2
        pop.income -= min(pop.income*payrollTax, 160000*payrollTax)/2

        pop.paidTaxes = tax
        pop.income -= tax
        totalIncomeTax += pop.paidTaxes

    return totalIncomeTax


# Calculates amount of money pops consume and invest
def consumption(popList):
    vatTax = 0.05
    vatTotal = 0

    for pop in popList:
        yearlyInvestment = min(max(0.00000233*pop.income - 0.0676, 0), 0.5)*pop.income
        networth = 0
        for i in range(20):
            networth *= 1.025
            networth += yearlyInvestment

        pop.netWorth = networth
        pop.consumption = pop.income - yearlyInvestment
        vatTotal += pop.consumption * vatTax
        pop.consumption *= (1-vatTax)

    return vatTotal

def distributeTaxes(popList, Issue):
    moneySpent = 0

    if Issue.x > 0:
        moneyMult = Issue.x/10 + 1
    elif Issue.x < 0:
        moneyMult = -0.1 * Issue.x + 1
    else:
        moneyMult = 1

    for pop in popList:
        if pop.income > 0:
            moneySpent += max(30000-pop.income, 0)/2 * moneyMult
            pop.income += max(30000-pop.income, 0)/2 * moneyMult
        else:
            moneySpent += 15000 * moneyMult
            pop.income += 15000 * moneyMult

    return moneySpent

# Sees if pops are better off than last year
def betterOff(popList):
    for pop in popList:
        pop.oldIncomes.append(pop.income)

        if len(pop.oldIncomes) != 1:
            pop.happiness = ((pop.oldIncomes[len(pop.oldIncomes)-1] - pop.oldIncomes[len(pop.oldIncomes)-2]) / pop.oldIncomes[len(pop.oldIncomes)-2]) * 10

# Changes pop ideology due to how happy they are
def popIdeologyChange(popList, govPlan, oppositionPlan):
    for pop in popList:
        diffX = govPlan.x - pop.x
        diffY = govPlan.y - pop.y
        magnitude = math.sqrt(diffX ** 2 + diffY ** 2)

        if pop.happiness > 0:
            pop.x += (pop.happiness * (diffX / magnitude))*0.1
            pop.y += (pop.happiness * (diffY / magnitude))*0.1
        elif pop.happiness < 0:
            anger = -pop.happiness  # Corrected calculation of anger
            diffX = oppositionPlan.x - pop.x
            diffY = oppositionPlan.y - pop.y
            magnitude = math.sqrt(diffX ** 2 + diffY ** 2)
            pop.x += (anger * (diffX / magnitude))*0.1
            pop.y += (anger * (diffY / magnitude))*0.1

            if random.random() < 0.1: # Extremism
                pop.x = random.gauss(7.5, 2.5)
                pop.y = random.gauss(7.5, 2.5)

                if random.random() < 0.5:
                    pop.x *= -1
                if random.random() < 0.5:
                    pop.y *= -1

        pop.x = random.gauss(pop.x, 1)
        pop.y = random.gauss(pop.y, 1)

def updateEconPops(incomeList, popList):
    for i in range(len(popList)):
        popList[i].income = incomeList[i]

def main():
    population = 331900000
    sample = population
    factor = 1

    while sample > 100000:
        factor *= 10
        sample = int(sample/10)

    statusQuo = Issue(0, 0)
    incomeList = createIncomeList(55000, 0.5, sample)
    popList = createEconPops(incomeList)

    randomPop = random.randint(1, len(popList))-1

    for i in range(10):
        if i % 2 == 0:
            statusQuo, govPlan, oppositionPlan = politicalVote(popList, statusQuo)

        print("GINI", max(0.0195*statusQuo.x + 0.56333, 0.3))
        incomeList = createIncomeList(55000, round(max(-0.0195*statusQuo.x + 0.56333, 0.3), 2), sample)
        moneySpent = distributeTaxes(popList, statusQuo)

        incomeTax = payIncomeTaxes(popList, statusQuo)
        consumeTax = consumption(popList)
        totalTaxes = incomeTax + consumeTax

        updateEconPops(incomeList, popList)
        betterOff(popList) # Broken due to popList resetting every year
        popIdeologyChange(popList, govPlan, oppositionPlan)

        print(f"Income ${totalTaxes*factor:,.2f}")
        print(f"Expenses ${moneySpent*factor:,.2f}")
        print(f"Net $ {(totalTaxes-moneySpent)*factor:,.2f}")

        print(f"Total taxes ${(incomeTax + consumeTax) * factor:,.2f}")

main()