import random
from classes import *
import math

Libertarian = Party("Libertarian", 6, -6)
Conservative = Party("Conservative Party", 3, 3)
MAGA = Party("One Nation", 5, 7)
Fascist = Party("Fascist Party", 10, 10)
Liberal = Party("Liberal Party", 0, 0)
SDP = Party("SDP", -3, -3)
Socialist = Party("Socialists", -7, -4)
Communist = Party("Communist", -10, -1)

# partyList = [Fascist, MAGA, Libertarian, Conservative, Liberal, SDP, Socialist, Communist]
partyList = [Party("Progressive Alliance", -6, 5), Party("Green Harmony", -3, -2),
             Party("Freedom First", 2, 2), Party("Liberty Coaliton", 6, -4)]
# partyList = [Party("Democrats", -4, -4), Party("Republicans", 4, 4)]
politicianList = []

# Voters decide who they are gonna vote for in the election
def voterDecision(popList):
    for pop in popList:
        index = 0
        minDistance = 1000
        for i in range(len(partyList)):
            distance = calcPolsDistance(pop, partyList[i])

            if distance < minDistance:
                index = i
                minDistance = distance

        pop.vote = partyList[index] # Might be useless
        partyList[index].votes += 1

# Calculates distance between 1 object and other based on x and y
# Returns distance but modified to be longer if in a different quadrant on the political compass
def calcPolsDistance(idealA, idealB, manualDistance=0):
    distance = math.sqrt((idealA.x - idealB.x) ** 2 + (idealA.y - idealB.y) ** 2)

    if (idealA.x >= 0 and idealB.x <= 0) or (idealA.x <= 0 and idealB.x >= 0):
        distance += 2

    if (idealA.y >= 0 and idealB.y <= 0) or (idealA.y <= 0 and idealB.y >= 0):
        distance += 1

    distance += manualDistance

    return distance

# Allocates seats based on votes recieved, seats are stored in the party object
# Returns nothing
def allocate_seats(partyList, num_seats):
    while num_seats > 0:
        # Calculate the allocation quotient for each party
        allocation_quotients = [(party, party.votes / (party.seats + 1)) for party in partyList]

        # Find the party with the highest quotient
        max_party, max_quotient = max(allocation_quotients, key=lambda x: x[1])

        # Allocate a seat to the party with the highest quotient
        max_party.seats += 1
        num_seats -= 1

# Finds the party with the most votes and resolves ties
# Returns top party (Too lazy to change name of function)
def findTopTwoParties(partyList):
    n = len(partyList)
    sortedList = partyList[:]  # Create a copy of the original list

    for i in range(n):
        for j in range(0, n - i - 1):
            if sortedList[j].seats < sortedList[j + 1].seats:
                sortedList[j], sortedList[j + 1] = sortedList[j + 1], sortedList[j]

    if sortedList[0] == sortedList[1]:
        if random.random() < 0.5:
            temp = sortedList[0]
            sortedList[0] = sortedList[1]
            sortedList[1] = temp

    return sortedList[0], sortedList[1]

# Creates a coalition with the largest party always in charge
# Returns list of parties in coalition
def coalitionBuilding(partyList, totalSeats):
    partyA, partyB = findTopTwoParties(partyList)
    coalitionSeats = 0

    aList = []
    bList = []
    aSeats = 0
    bSeats = 0

    for party in partyList:
        aDist = calcPolsDistance(partyA, party)
        bDist = calcPolsDistance(partyB, party)

        if aDist > bDist:
           aList.append(party)
           aSeats += party.seats
        else:
            bList.append(party)
            bSeats += party.seats

        if aSeats > totalSeats*0.5 or bSeats > totalSeats*0.5:
            break

    if aSeats > totalSeats*0.5:
        coalitionList = aList
        coalitionSeats = aSeats
    elif bSeats > totalSeats*0.5:
        coalitionList = bList
        coalitionSeats = bSeats
    else:
        print("Hung parliament")
        coalitionList = []

    coalitionList = sorted(coalitionList, key=lambda member: member.seats, reverse=True)

    print("\nCoalition members")
    for member in coalitionList:
        print(member.name)
    print("Total seats", coalitionSeats)

    return coalitionList

# Creates politicians based off how many seats each party won
# Returns politican list
def createPoliticians(partyList):
    for party in partyList:
        for i in range(party.seats):
            politicianList.append(Politician(party, f"{party.name}-{i}"))

    return politicianList

# Creates possible candidates for an election
# Candidates is the # of candidates on the ballot
def getCandidates(politicianList, candidates):
    candidateList = []
    for i in range(candidates):
        option = random.choice(politicianList)
        attempts = 0
        while option.job != "MP" or (not sameParty(candidateList, option) and attempts < 100):
            option = random.choice(politicianList)
            attempts += 1

        candidateList.append(random.choice(politicianList))

    return candidateList

# Tests if a in a list of politicians, a politicians passed in party is not equal to any of them
# Returns True if there is someone in the same party
# False is not
def sameParty(candidateList, politician):
    for candidate in candidateList:
        if politician.party == candidate.party:
            return True

    return False

# Runs elections for various offices
def elections(candidateList, electorateList, title, round=1, replace=False):
    for voter in electorateList:
        distance = []
        for i in range(len(candidateList)):
            distance.append(calcPolsDistance(candidateList[i], voter))

        index = calcMinIndex(distance)
        candidateList[index].votes += 1

    sorted_candidates = sorted(candidateList, key=lambda politician: politician.votes, reverse=True)

    if sorted_candidates[0].votes == len(electorateList) * 0.5 and sorted_candidates[1].votes == len(electorateList) * 0.5:  # Resolves ties
        sorted_candidates[0].x += (random.random()*2-1)
        sorted_candidates[0].y += (random.random() * 2 - 1)
        sorted_candidates[1].x += (random.random() * 2 - 1)
        sorted_candidates[1].y += (random.random() * 2 - 1)
        print("Tie")

    if sorted_candidates[0].votes > len(electorateList)*0.5:
        winner = giveTitle(title, sorted_candidates[0], politicianList, replace)
        print(f"\n{title}: {sorted_candidates[0]} {sorted_candidates[0].votes}")
        print(f"Runner up: {sorted_candidates[1]} {sorted_candidates[1].votes}")
        resetVotes(candidateList)
        resetVotes(sorted_candidates)

        return winner

    else:
        candidateList = [sorted_candidates[0], sorted_candidates[1]]
        if len(sorted_candidates) > 2 and sorted_candidates[1].votes == sorted_candidates[2].votes and round < 3: # Includes 3rd place if 2nd and 3rd place tie
            candidateList.append(sorted_candidates[2])
            sorted_candidates[2].votes = 0

        resetVotes(candidateList)
        resetVotes(sorted_candidates)

        elections(candidateList, electorateList, title, round+1, replace)

# Resets votes for another round or election
def resetVotes(list):
    for item in list:
        item.votes = 0

# Gives a title to a politician if elected
# Returns the politician given the title
def giveTitle(title, winner, politicianList, replace):
    for politician in politicianList:
        if politician == winner:
            politician.job = title

            if replace:
                politicianList.append(Politician(politician.party, f"{politician.party}-S{random.random()}"))

            return politician

    return 0

# Creates a list of politicians on a side specified
# Returns side created
def createSideList(coalitionList, politicianList, majority):
    sideList = []
    for politician in politicianList:
        if politician.party in coalitionList:
            if majority:
                sideList.append(politician)
        else:
            if not majority:
                sideList.append(politician)

    return sideList

# Calculates the minimum value of a list, returns its index
def calcMinIndex(list):
    minimum = 999
    index = 0
    for i in range(len(list)):
        if minimum > list[i]:
            minimum = list[i]
            index = i

    return index

def inMajority(politician, coalitionList):
    for party in coalitionList:
        if politician.party == party:
            return True

    return False

def holdVote(politicianList, newIssue, statusQuo, coalitionList, majorityList, minorityList, canVeto=True):
    ayeList = []
    nayList = []
    presentList = []
    veto = False

    print(f"\nVote on {newIssue.name} {newIssue.x}, {newIssue.y}")
    print(f"Current status on {newIssue.name} {statusQuo}")

    for politician in politicianList:
        inFavor = round(calcPolsDistance(politician, newIssue), 1)
        against = round(calcPolsDistance(politician, statusQuo), 1)

        if inMajority(politician, coalitionList):
            inFavor -= 2 # Less means more likely to support
        else:
            inFavor += 1

        if politician.job != "President":
            if inFavor < against:
                ayeList.append(politician)
            elif inFavor > against:
                nayList.append(politician)
            else:
                presentList.append(politician)

        elif politician.job == "President" and canVeto:
            if inFavor <= against:
                print(f"President {politician.name} supports it")
                veto = False
            elif inFavor > against:
                print(f"President {politician.name} vetoed it")
                veto = True

        if not canVeto:
            veto = False

    if len(ayeList) > len(nayList):
        print("Ayes", len(ayeList))
        print("Nays", len(nayList))
        print("Present", len(presentList))
        whipCount(ayeList, nayList)

    if (len(ayeList) == len(majorityList)) and (len(nayList) == len(minorityList)):
        print("Party line vote in favor")

    if veto:
        if len(ayeList) > len(nayList) * 2:
            print("Bill passes")
            return True
        else:
            print("Bill has been vetoed")
            return False
    else:
        if len(ayeList) > len(nayList):
            print("Bill passes")
            return True
        else:
            print("Bill fails")
            return False

# Prints everyone in favor or against the bill
def whipCount(ayeList, nayList):
    print(', '.join([member.name for member in ayeList]))
    print(', '.join([member.name for member in nayList]))

# Creates a cabinet as well as a political compass spot for an issue that want to pass
def cabinetAllocation(coalitionList, majorityList):
    cabinetSpots = ["Prime Minister",
                    "Deputy Prime Minister",
                    "Defense Minister",
                    "Treasury Minister",
                    "Interior Minister",
                    "Justice Minister",
                    "Social Services Minister",
                    "Transportation Minister"]

    # PM spot
    potentialPerson = random.choice(majorityList)
    while coalitionList[0] != potentialPerson.party or potentialPerson.job != "MP":
        potentialPerson = random.choice(majorityList)

    potentialPerson.job = "Prime Minister"
    cabinetSpots.pop(0)

    while cabinetSpots:
        cabinetPerson = random.choice(majorityList)
        while cabinetPerson.job != "MP":
            cabinetPerson = random.choice(majorityList)

        cabinetPerson.job = cabinetSpots[0]
        cabinetSpots.pop(0)

    totalSeats = len(majorityList)
    x = 0
    y = 0
    for party in coalitionList:
        x += (party.x * (party.seats/totalSeats))
        y += (party.y * (party.seats / totalSeats))

    return Issue(round(x), round(y))

# Calculates opposition platform based on the individual members
# It's individual members due to a lack of parties being in opposition, more members (also just laziness)
def oppositionPlatform(minorityList):
    totalSeats = len(minorityList)
    x = 0
    y = 0
    for members in minorityList:
        x += members.x * (1/totalSeats)
        y += members.y * (1 / totalSeats)

    return Issue(round(x), round(y))

# Finds a person with a job
# Returns the person
def findPerson(politicianList, job):
    for politician in politicianList:
        if politician.job == job:
            return politician

    print(f"Couldn't find {job}")

# Resets the lists for another round
def reset(politicianList, coalitionList, majorityList, minorityList, partyList):
    politicianList.clear()
    coalitionList.clear()
    majorityList.clear()
    minorityList.clear()

    for party in partyList:
        party.seats = 0

# Calculates mean pop ideology
# Returns an issue object with the result
def meanPopIdeology(popList):
    meanX = 0
    meanY = 0
    happy = 0
    for pop in popList:
        meanX += pop.x
        meanY += pop.y
        happy += pop.happiness

    print(happy/len(popList))
    return Issue(meanX/len(popList), meanY/len(popList))

def ideologyReaction(statusQuo, govPlan, passes, popList):
    forBill = 0
    againstBill = 0

    for pop in popList:
        if calcPolsDistance(statusQuo, pop) > calcPolsDistance(govPlan, pop):
            supports = True
        else:
            supports = False

        percentShift = calcPolsDistance(statusQuo, pop)*0.006

        if govPlan.x < 0: # Left wing
            if supports:
                pop.x -= percentShift*10
            else:
                pop.x += percentShift * 10

        else:
            if supports:
                pop.x += percentShift*10
            else:
                pop.x -= percentShift * 20

        if govPlan.y < 0: # Libertarian
            if supports:
                pop.y -= percentShift*10
            else:
                pop.y += percentShift * 20
        else:
            if supports:
                pop.y += percentShift*10
            else:
                pop.y -= percentShift * 20

        if not supports:
            if random.random() < percentShift: # Flips sides
                pop.x = random.gauss(pop.x*-1, 3)
                pop.y = random.gauss(pop.y*-1, 3)

        if supports:
            forBill += 1
        else:
            againstBill += 1

        pop.x += round(random.random() - 0.5, 1)
        pop.y += round(random.random() - 0.5, 1)

    print(f"Supports {int(forBill/(forBill+againstBill)*100)}%")
    print(f"Against {int(againstBill/(forBill+againstBill)*100)}%")

    for party in partyList: # Randomly moves parties ideologically
        party.x += round(random.random()-0.5, 1)
        party.y += round(random.random()-0.5, 1)

# Runs a political cycle
# Returns nothing
def politicalVote(popList, statusQuo):
    totalSeats = 149
    voterDecision(popList)
    allocate_seats(partyList, totalSeats)

    print("Mean ideology:", meanPopIdeology(popList))
    for parties in partyList:
        print(f"{parties.name}: {parties.seats}")

    coalitionList = coalitionBuilding(partyList, totalSeats)
    politicianList = createPoliticians(partyList)
    majorityList = createSideList(coalitionList, politicianList, True)
    minorityList = createSideList(coalitionList, politicianList, False)

    elections(getCandidates(politicianList, 4), politicianList, "Speaker of the House")
    elections(getCandidates(politicianList, 4), popList, "President", 1, True)

    elections(getCandidates(majorityList, 4), majorityList, "Majority Leader")
    elections(getCandidates(minorityList, 4), minorityList, "Minority Leader")

    majLeader = findPerson(politicianList, "Majority Leader")
    minLeader = findPerson(politicianList, "Minority Leader")

    govPlan = cabinetAllocation(coalitionList, majorityList)
    oppositionPlan = oppositionPlatform(minorityList)

    print()
    for poltician in politicianList:
        if poltician.job != "MP":
            print(poltician)

    print("Confidence vote")
    holdVote(politicianList, Issue(govPlan.x, govPlan.y), Issue(minLeader.x, minLeader.y), coalitionList, majorityList, minorityList, False)

    print()
    passes = holdVote(politicianList, govPlan, statusQuo, coalitionList, majorityList, minorityList)
    while not passes and abs(govPlan.x - statusQuo.x) > 0.3:
        govPlan.x = round(govPlan.x*0.75 + statusQuo.x*0.25, 1)
        govPlan.y = round(govPlan.y*0.75 + statusQuo.y*0.25, 1)
        passes = holdVote(politicianList, govPlan, statusQuo, coalitionList, majorityList, minorityList)

    ideologyReaction(statusQuo, govPlan, passes, popList)

    if passes:
        statusQuo = govPlan

    reset(politicianList, coalitionList, majorityList, minorityList, partyList)
    print()

    return statusQuo, govPlan, oppositionPlan
