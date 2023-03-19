import random
import math
import pandas as pd
#pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
import itertools

def getRandomChromosomes(chromosomeFile,num_chromosomes,chromosomesRequired):
    randomChromosomes = []
    try:
        with open(chromosomeFile, 'r') as file:
            contents = file.read()
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        contents = None

    lines = contents.split('\n')

    randomChromosomeLines = random.sample(range(0,num_chromosomes+1),chromosomesRequired)

    for line in range(chromosomesRequired):
        current_line = lines[randomChromosomeLines[line]].lstrip('[{').rstrip(']}')
        current_chromosome = list(map(int, current_line.split(',')))
        randomChromosomes.append(current_chromosome)

    return randomChromosomes

def getRequest(chromosome):
    requestDataFrame = pd.DataFrame(columns=['pickUp','dropOff'])
    finalDataFrame = pd.DataFrame(columns=['pickUp','dropOff'])
    chromosomeLength = chromosome.iloc[0].count()
    chromosomeList = chromosome.iloc[0].tolist()

    for i in range (len(chromosomeList)):
        if i % 2 != 0:
            chromosomeList.remove(i)

    for i in range(chromosomeLength):
        if i % 2 == 0 and i in chromosomeList :
            dataFrameIndex = chromosomeList.index(i)
            requestDataFrame.at[dataFrameIndex,'pickUp'] = i
            requestDataFrame.at[dataFrameIndex,'dropOff'] = i + 1

    return requestDataFrame

def getAllPairs(requestDataFrame):
    allPairs = pd.DataFrame(columns=['pickUp1','dropOff1','pickUp2','dropOff2'])
    pairNum = 0
    for i in range(len(requestDataFrame)):
        for j in range(i+1,len(requestDataFrame)):
            allPairs.at[pairNum,'pickUp1'] = requestDataFrame.at[i,'pickUp']
            allPairs.at[pairNum,'dropOff1'] = requestDataFrame.at[i,'dropOff']
            allPairs.at[pairNum,'pickUp2'] = requestDataFrame.at[j,'pickUp']
            allPairs.at[pairNum,'dropOff2'] = requestDataFrame.at[j,'dropOff']
            pairNum += 1
    #print(allPairs)
    return allPairs

def getAllPairRoutes (allPairs):
    allPairRoutes = pd.DataFrame(columns=['Location1','Location2','Location3','Location4','pairNum'])
    routeNum = 0
    for i in range (len(allPairs)):
        pickUp1 = allPairs.at[i,'pickUp1']
        dropOff1 = allPairs.at[i,'dropOff1']
        pickUp2 = allPairs.at[i,'pickUp2']
        dropOff2 = allPairs.at[i,'dropOff2']

        locations = [pickUp1,dropOff1,pickUp2,dropOff2]
        routePermutations = list([perm for perm in itertools.permutations(locations) if perm.index(pickUp1) < perm.index(dropOff1) and perm.index(pickUp2) < perm.index(dropOff2)])

        for j in range(len(routePermutations)):
            route = routePermutations[j]
            allPairRoutes.at[routeNum,'Location1'] = route[0]
            allPairRoutes.at[routeNum,'Location2'] = route[1]
            allPairRoutes.at[routeNum,'Location3'] = route[2]
            allPairRoutes.at[routeNum,'Location4'] = route[3]
            allPairRoutes.at[routeNum,'pairNum'] = i
            routeNum += 1
    #print(allPairRoutes)
    return allPairRoutes

def getAllVehicleRoutes(allPairRoutes,num_vehicles,num_requests,vehicleCapacity,vehicleFile,requestFile,chromosome):
    vehicleRoundsRequired = math.ceil((num_requests/vehicleCapacity)/num_vehicles)
    allVehicleRoutes = pd.DataFrame(columns=['VehicleNum','Location1','Location2','Location3','Location4'],dtype=int)
    bestLocationStart = pd.DataFrame(columns=['Distance','VehicleNum','Location1','Location2','Location3','Location4'],dtype=int)
    selectedBestLocationStart = pd.DataFrame(columns=['Distance','VehicleNum','Location1','Location2','Location3','Location4'],dtype=int)
    finalVehicleRoutes = pd.DataFrame(columns=['VehicleNum','Location1','Location2','Location3','Location4'],dtype=int)
    usedVehicles = []
    usedLocations = []
    freeLocations = []

    try:
        with open(requestFile, 'r') as file:
            contents = file.read()
            requests = eval(contents)
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        requests = None

    try:
        with open(vehicleFile, 'r') as file:
            vehicle_lines = file.readlines()[32:132]
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        vehicle_lines = None

    route_num = 0
    for i in range (len(allPairRoutes)):
        for j in range(num_vehicles):
            allVehicleRoutes.at[route_num, 'VehicleNum'] = j
            allVehicleRoutes.at[route_num, 'Location1'] = allPairRoutes.at[i, 'Location1']
            allVehicleRoutes.at[route_num, 'Location2'] = allPairRoutes.at[i, 'Location2']
            allVehicleRoutes.at[route_num, 'Location3'] = allPairRoutes.at[i, 'Location3']
            allVehicleRoutes.at[route_num, 'Location4'] = allPairRoutes.at[i, 'Location4']
            route_num += 1

    for i in range (len(allVehicleRoutes)):
        distance = 0
        vehicleStartX,vehicleStartY = vehicle_lines[int(allVehicleRoutes.at[i,'VehicleNum'])].split(',')[1:3]
        Location1X, Location1Y = requests[int(allVehicleRoutes.at[i,'Location1'])][0:2]
        Location2X,Location2Y = requests[int(allVehicleRoutes.at[i,'Location2'])][0:2]
        Location3X,Location3Y = requests[int(allVehicleRoutes.at[i,'Location3'])][0:2]
        Location4X,Location4Y = requests[int(allVehicleRoutes.at[i,'Location4'])][0:2]

        distance += math.sqrt((int(vehicleStartX) - int(Location1X))**2 + (int(vehicleStartY) - int(Location1Y))**2)
        distance += math.sqrt((int(Location1X) - int(Location2X))**2 + (int(Location1Y) - int(Location2Y))**2)
        distance += math.sqrt((int(Location2X) - int(Location3X))**2 + (int(Location2Y) - int(Location3Y))**2)
        distance += math.sqrt((int(Location3X) - int(Location4X))**2 + (int(Location3Y) - int(Location4Y))**2)

        bestLocationStart.at[i,'Distance'] = distance
        bestLocationStart.at[i,'VehicleNum'] = allVehicleRoutes.at[i,'VehicleNum']
        bestLocationStart.at[i,'Location1'] = allVehicleRoutes.at[i,'Location1']
        bestLocationStart.at[i,'Location2'] = allVehicleRoutes.at[i,'Location2']
        bestLocationStart.at[i,'Location3'] = allVehicleRoutes.at[i,'Location3']
        bestLocationStart.at[i,'Location4'] = allVehicleRoutes.at[i,'Location4']


    bestLocationStart.sort_values('Distance', inplace=True)
    bestLocationStart = bestLocationStart.reset_index(drop=True)

    numDone = 0
    indexDone = 0
    for i in range (len(bestLocationStart)):
        vehicle = int(bestLocationStart.at[i,'VehicleNum'])
        Location1 = int(bestLocationStart.at[i,'Location1'])
        Location2 = int(bestLocationStart.at[i,'Location2'])
        Location3 = int(bestLocationStart.at[i,'Location3'])
        Location4 = int(bestLocationStart.at[i,'Location4'])

        if vehicle not in usedVehicles and Location1 not in usedLocations and Location2 not in usedLocations and Location3 not in usedLocations and Location4 not in usedLocations:
            selectedBestLocationStart.at[indexDone,'Distance'] = bestLocationStart.at[i,'Distance']
            selectedBestLocationStart.at[indexDone,'VehicleNum'] = vehicle
            selectedBestLocationStart.at[indexDone,'Location1'] = Location1
            selectedBestLocationStart.at[indexDone,'Location2'] = Location2
            selectedBestLocationStart.at[indexDone,'Location3'] = Location3
            selectedBestLocationStart.at[indexDone,'Location4'] = Location4
            finalVehicleRoutes.at[indexDone,'VehicleNum'] = vehicle
            finalVehicleRoutes.at[indexDone,'Location1'] = Location1
            finalVehicleRoutes.at[indexDone,'Location2'] = Location2
            finalVehicleRoutes.at[indexDone,'Location3'] = Location3
            finalVehicleRoutes.at[indexDone,'Location4'] = Location4
            numDone += 2
            indexDone += 1
            usedVehicles.append(vehicle)
            usedLocations.append(Location1)
            usedLocations.append(Location2)
            usedLocations.append(Location3)
            usedLocations.append(Location4)
"""
    for i in range (vehicleRoundsRequired-1):

        num_locations = 0
        for col in finalVehicleRoutes.columns:
            if col.startswith("Location"):
                num_locations += 1

        for k in range (len(selectedBestLocationStart)):
            print(f"Round {i+2} of {vehicleRoundsRequired}")
            if numDone >= num_requests:
                break

            freeLocations = []
            for j in chromosome:
                if j not in usedLocations:
                    freeLocations.append(j)

            pairRoutes = getAllPairRoutes(getAllPairs(getRequest(freeLocations)))

            tempDataframe = pd.DataFrame(columns=['Distance','Location1','Location2','Location3','Location4'],dtype=int)
            startLocation = selectedBestLocationStart.at[k,f'Location{num_locations}']
            startLocationX, startLocationY = requests[startLocation][0:2]

            for l in range(len(pairRoutes)):
                print(f"Round {i+2} of {vehicleRoundsRequired}")
                distance = 0
                Location1 = pairRoutes.at[l, 'Location1']
                Location2 = pairRoutes.at[l, 'Location2']
                Location3 = pairRoutes.at[l, 'Location3']
                Location4 = pairRoutes.at[l, 'Location4']
                Location1X, Location1Y = requests[Location1][0:2]
                Location2X,Location2Y = requests[Location2][0:2]
                Location3X,Location3Y = requests[Location3][0:2]
                Location4X,Location4Y = requests[Location4][0:2]

                distance += math.sqrt((int(vehicleStartX) - int(Location1X))**2 + (int(vehicleStartY) - int(Location1Y))**2)
                distance += math.sqrt((int(Location1X) - int(Location2X))**2 + (int(Location1Y) - int(Location2Y))**2)
                distance += math.sqrt((int(Location2X) - int(Location3X))**2 + (int(Location2Y) - int(Location3Y))**2)
                distance += math.sqrt((int(Location3X) - int(Location4X))**2 + (int(Location3Y) - int(Location4Y))**2)

                tempDataframe.at[l, 'Distance'] = distance
                tempDataframe.at[l, 'Location1'] = Location1
                tempDataframe.at[l, 'Location2'] = Location2
                tempDataframe.at[l, 'Location3'] = Location3
                tempDataframe.at[l, 'Location4'] = Location4

            tempDataframe.sort_values('Distance', inplace=True)
            tempDataframe = tempDataframe.reset_index(drop=True)
            print(tempDataframe)

            LocationA = tempDataframe.at[0, 'Location1']
            LocationB = tempDataframe.at[0, 'Location2']
            LocationC = tempDataframe.at[0, 'Location3']
            LocationD = tempDataframe.at[0, 'Location4']

            finalVehicleRoutes.at[k, f'Location{1+num_locations}'] = LocationA
            finalVehicleRoutes.at[k, f'Location{2+num_locations}'] = LocationB
            finalVehicleRoutes.at[k, f'Location{3+num_locations}'] = LocationC
            finalVehicleRoutes.at[k, f'Location{4+num_locations}'] = LocationD

            usedLocations.append(LocationA)
            usedLocations.append(LocationB)
            usedLocations.append(LocationC)
            usedLocations.append(LocationD)

            numDone += 2


    print(finalVehicleRoutes)

    #(bestLocationStart)
"""
