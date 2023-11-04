import random
from classes import *
import math

Libertarian = Party("Libertarian", 6, -6)
Conservative = Party("Conservative Party", 3, 3)
MAGA = Party("One Nation", 5, 7)
Fascist = Party("Fascist Party", 10, 10, True)
Liberal = Party("Liberal Party", 2, -2)
SDP = Party("SDP", -3, -3)
Socialist = Party("Democratic Socialists", -7, -4)
Communist = Party("Communist", -10, -1, True)

partyList = [Fascist, MAGA, Libertarian, Conservative, Liberal, SDP, Socialist, Communist]
# partyList = [Party("Progressive Alliance", -6, 5), Party("Green Harmony", -3, -2),
#              Party("Freedom First", 2, 2), Party("Liberty Coaliton", 6, -4)]
# partyList = [Party("Democrats", -4, -4), Party("Republicans", 4, 4)]
# partyList = [Party("Fascist", 10, 10, True), Party("Tea Party", 8, 8, True), Party("MAGA", 6, 6), Party("Libertarian", 6, -6), Party("Conservatives", 4, 4),
#              Party("Liberal Conservatives", 2, 1), Party("Blue Dogs", -1, 1), Party("Liberal Democrats", 1, -3), Party("Liberals", -4, -4), Party("Progressives", -6, -6),
#              Party("Democratic Socialists", -7, -7), Party("Socialist", -9, -9, True), Party("Communist", -10, 10, True)]
politicianList = []
committees = ["Budget", "Defense, Veterans and Foreign Affairs", "Oversight, Ethics and Judiciary",
             "Agriculture, Resources and the Environment", "Social Services", "Banking and Business"]

threashold = 0
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

    for party in partyList:
        if party.votes < len(popList)*threashold:
            party.votes = 0

# Calculates distance between 1 object and other based on x and y
# Returns distance but modified to be longer if in a different quadrant on the political compass
def calcPolsDistance(idealA, idealB, manualDistance=0):
    distance = math.sqrt((idealA.x - idealB.x) ** 2 + (idealA.y - idealB.y) ** 2)

    if (idealA.x >= 0 and idealB.x <= 0) or (idealA.x <= 0 and idealB.x >= 0):
        distance += 3

    if (idealA.y >= 0 and idealB.y <= 0) or (idealA.y <= 0 and idealB.y >= 0):
        distance += 3

    if isinstance(idealB, Party) and isinstance(idealA, Party) and (idealA.pariah or idealB.pariah):
        distance *= 2

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

    for item in sortedList:
        if item.pariah:
            sortedList.remove(item)

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

    print("\nCoalition Candidates")
    print(partyA)
    print(partyB)

    aList = []
    bList = []
    aSeats = 0
    bSeats = 0

    for party in partyList:
        if not party.pariah:
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

    while aSeats < totalSeats*0.5 and bSeats < totalSeats*0.5:
        acceptedParty = random.choice(partyList)
        while not acceptedParty.pariah:
            acceptedParty = random.choice(partyList)

        print(f"{acceptedParty.name} now accepted")
        acceptedParty.pariah = False
        aDist = calcPolsDistance(partyA, acceptedParty)
        bDist = calcPolsDistance(partyB, acceptedParty)

        if aDist > bDist:
            aList.append(acceptedParty)
            aSeats += acceptedParty.seats
        else:
            bList.append(acceptedParty)
            bSeats += acceptedParty.seats

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
    if candidates == "Party":
        parties_selected = set()
        for politician in politicianList:
            if (politician.party.name not in parties_selected) and (random.random() < 1/8):
                candidateList.append(politician)
                parties_selected.add(politician.party.name)

        return candidateList

    for i in range(candidates):
        option = random.choice(politicianList)
        attempts = 0
        while option.job != "MP" or sameParty(candidateList, option):
            option = random.choice(politicianList)
            attempts += 1

        candidateList.append(random.choice(politicianList))

    return candidateList

def rcvVote(candidateList, electorateList):
    # Calculates initial vote
    for voter in electorateList:
        tempDistList = []
        for candidate in candidateList:
            tempDistList.append(calcPolsDistance(candidate, voter))

        # Combine the values and objects into pairs
        pairs = list(zip(tempDistList, candidateList))

        # Sort the pairs based on the values
        pairs.sort(key=lambda pair: pair[0])

        # Extract the sorted list of objects
        voter.vote = [pair[1] for pair in pairs]

def rcvTabulte(candidateList, electorateList):
    rcvVote(candidateList, electorateList)
    voteTotals = tallyVotes(candidateList, electorateList)

    if testWinner(voteTotals):
        pairs = list(zip(voteTotals, candidateList))
        pairs.sort(key=lambda pair: pair[0])
        finalTally = [pair[1] for pair in pairs]
        finalVotes = [pair[0] for pair in pairs]

        for i in range(len(finalTally)):
            print(f"{finalTally[i]}: {finalVotes[i]} votes")

        giveTitle("President", finalTally[len(finalTally) - 1], politicianList, True)
        return 0

    else:
        minValue = voteTotals[0]
        index = 0
        for i in range(len(voteTotals)):
            if minValue < voteTotals[i]:
                minValue = voteTotals[i]
                index = i

        loosingCandidate = candidateList[index]

    for voter in electorateList:
        for option in voter.vote:
            if loosingCandidate.name == option.name:
                voter.vote.remove(option)

    candidateList.remove(loosingCandidate)
    voteTotals = tallyVotes(candidateList, electorateList)

    if not testWinner(voteTotals):
        rcvTabulte(candidateList, electorateList)
    else:
        pairs = list(zip(voteTotals, candidateList))
        pairs.sort(key=lambda pair: pair[0])
        finalTally = [pair[1] for pair in pairs]
        finalVotes = [pair[0] for pair in pairs]

        for i in range(len(finalTally)):
            print(f"{finalTally[i]}: {finalVotes[i]} votes")

        giveTitle("President", finalTally[len(finalTally)-1], politicianList, True)

# Tallies vote for a RCV election
def tallyVotes(candidateList, electorateList):
    votes = [0] * len(candidateList)
    for voter in electorateList:
        for i in range (len(candidateList)):
            if voter.vote[0] == candidateList[i]:
                votes[i] += 1

    return votes

# Sees if a candidate has 50% of the votes
# Returns true if they won
# Returns false if no one won
def testWinner(voteTotals):
    for votes in voteTotals:
        if votes > sum(voteTotals)*0.5:
            return True

    return False

# Tests if a in a list of politicians, a politicians passed in party is not equal to any of them
# Returns True if there is someone in the same party
# False is not
def sameParty(candidateList, option):
    for candidate in candidateList:
        if option.party.name == candidate.party.name:
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
        for candidates in sorted_candidates:
            print(f"{candidates}: {candidates.votes} {candidates.votes/len(electorateList)*100}%")
        print()

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
        party.votes = 0

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

        if not supports:
            if govPlan.x > pop.x:
                pop.x -= 2
            else:
                pop.x += 2

            if govPlan.y > pop.y:
                pop.y -= 2
            else:
                pop.y += 2
        else:
            if govPlan.x < pop.x:
                pop.x -= 2
            else:
                pop.x += 2

            if govPlan.y < pop.y:
                pop.y -= 2
            else:
                pop.y += 2

        if supports:
            forBill += 1
        else:
            againstBill += 1

        pop.x += round(random.random() - 0.5, 1)
        pop.y += round(random.random() - 0.5, 1)

        pop.x = (pop.x*8.5)/10
        pop.y = (pop.y*8.5)/10

    print(f"Supports {int(forBill/(forBill+againstBill)*100)}%")
    print(f"Against {int(againstBill/(forBill+againstBill)*100)}%")

    for party in partyList: # Randomly moves parties ideologically
        party.x += round(random.random()-0.5, 1)
        party.y += round(random.random()-0.5, 1)

# Creates committees
def committeeCreation(majorityList, minorityList):
    majoritySeats = len(majorityList)
    minoritySeats = len(minorityList)
    totalSeats = majoritySeats+minoritySeats

    committeeSeats = round(13.2537 + 0.1075*totalSeats)
    majorityComm = math.ceil(majoritySeats/totalSeats * 1.03 * committeeSeats)
    minorityComm = int(committeeSeats - majorityComm)

    print("Total committee seats", committeeSeats)
    print("Majority committee seats", majorityComm)
    print("Minority committee seats", minorityComm)

    committeeList = [] * len(committees)

    for i in range(len(committees)):
        assignedMembers = 0
        while assignedMembers < majorityComm:
            appointee = random.choice(majorityList)
            if committees[i] not in appointee.committees:
                appointCommittee(appointee, committees[i])
                assignedMembers += 1
                committeeList[i].append(appointee)

        assignedMembers = 0
        while assignedMembers < minorityComm:
            appointee = random.choice(minorityList)
            if committees[i] not in appointee.committees:
                appointCommittee(appointee, committees[i])
                assignedMembers += 1
                committeeList[i].append(appointee)

    return committeeList

def appointCommittee(politician, committee):
    politician.committees.append(committee)

# Runs a political cycle
# Returns nothing
def politicalVote(popList, statusQuo):
    totalSeats = 149
    voterDecision(popList)
    allocate_seats(partyList, totalSeats)

    print("Mean ideology:", meanPopIdeology(popList))
    for parties in partyList:
        print(f"{parties.name}: {parties.seats}, {round(parties.votes/len(popList)*100, 1)}%")

    coalitionList = coalitionBuilding(partyList, totalSeats)
    politicianList = createPoliticians(partyList)
    majorityList = createSideList(coalitionList, politicianList, True)
    minorityList = createSideList(coalitionList, politicianList, False)

    elections(getCandidates(politicianList, "Party"), popList, "President", 1, True)
    # print("Presidential Election")
    # rcvTabulte(getCandidates(politicianList, "Party"), popList)

    elections(getCandidates(majorityList, "Party"), majorityList, "Majority Leader")
    elections(getCandidates(minorityList, "Party"), minorityList, "Minority Leader")
    elections(getCandidates(politicianList, "Party"), politicianList, "Speaker of the House")

    majLeader = findPerson(politicianList, "Majority Leader")
    minLeader = findPerson(politicianList, "Minority Leader")
    speaker = findPerson(politicianList, "Speaker of the House")

    committeeCreation(majorityList, minorityList)

    govPlan = cabinetAllocation(coalitionList, majorityList)
    oppositionPlan = oppositionPlatform(minorityList)

    with open('output.txt', 'w') as file:
        print("\nFront Benchers")
        for poltician in politicianList:
            if poltician.job != "MP":
                print(f"{poltician.name}: {poltician.job}", file=file)

        # Create a dictionary to store the counts of each political party
        party_counts = {}

        for committee in committees:
            print(f"\n{committee} Committee", file=file)
            for politician in politicianList:
                for assignment in politician.committees:
                    if assignment == committee:
                        print(f"{politician.name} ({politician.party})", file=file)

                        # Convert politician.party to a hashable key (assuming it's a string)
                        party_key = str(politician.party)

                        # Update the count for the political party using the hashable key
                        party_counts[party_key] = party_counts.get(party_key, 0) + 1

            # Print the counts of each political party
            print("\nParty Counts:", file=file)
            for party, count in party_counts.items():
                print(f"{party}: {count}", file=file)
            party_counts = {}

    print()

    print("Confidence vote")
    confidence = holdVote(politicianList, Issue(govPlan.x, govPlan.y), Issue(minLeader.x, minLeader.y), coalitionList, majorityList, minorityList, False)
    if not confidence:
        print("Snap election (Hung Parliament)")
        swingX = random.random()-0.5
        swingY = random.random()-0.5
        for pop in popList:
            pop.x += swingX
            pop.y += swingY
        reset(politicianList, coalitionList, majorityList, minorityList, partyList)

        politicalVote(popList, statusQuo)

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
