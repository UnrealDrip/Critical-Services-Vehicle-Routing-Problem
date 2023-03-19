import numpy as np
import math
import itertools

def getRequest(chromosome):
    chromosomeList = chromosome.iloc[0, ::2].values
    indices = np.arange(len(chromosomeList))
    indices = indices[~(indices % 2)]
    pickUps = indices
    dropOffs = pickUps + 1
    pairs = np.column_stack((pickUps, dropOffs))
    return pairs

def getAllPairs(requestDataFrame):
    n = len(requestDataFrame)
    pairs = np.empty((n*(n-1)//2, 4), dtype=requestDataFrame.dtype)
    idx = 0
    for i in range(n):
        for j in range(i+1, n):
            pairs[idx] = (requestDataFrame['pickUp'][i], requestDataFrame['dropOff'][i],
                          requestDataFrame['pickUp'][j], requestDataFrame['dropOff'][j])
            idx += 1
    return pairs

def getAllPairRoutes(allPairs):
    n = len(allPairs)
    allPairRoutes = np.empty((n*6, 5), dtype=allPairs.dtype)
    routeNum = 0

    for i in range(n):
        pickUp1, dropOff1, pickUp2, dropOff2 = allPairs[i]

        locations = np.array([pickUp1, dropOff1, pickUp2, dropOff2])
        routePermutations = itertools.permutations(locations)

        for route in routePermutations:
            if route.tolist().index(pickUp1) < route.tolist().index(dropOff1) and route.tolist().index(pickUp2) < route.tolist().index(dropOff2):
                allPairRoutes[routeNum] = (route[0], route[1], route[2], route[3], i)
                routeNum += 1

    allPairRoutes = allPairRoutes[:routeNum]
    # print(allPairRoutes)
    return allPairRoutes



def getAllVehicleRoutes(allPairRoutes, num_vehicles, num_requests, vehicleCapacity, vehicleFile, requestFile, chromosome):
    vehicleRoundsRequired = math.ceil((num_requests / vehicleCapacity) / num_vehicles)
    allVehicleRoutes = np.zeros((len(allPairRoutes) * num_vehicles, 5), dtype=int)
    bestLocationStart = np.zeros((len(allPairRoutes) * num_vehicles, 6), dtype=int)
    selectedBestLocationStart = np.zeros((len(allPairRoutes) * num_vehicles, 6), dtype=int)
    finalVehicleRoutes = np.zeros((len(allPairRoutes) * num_vehicles, 5), dtype=int)
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
    for i in range(len(allPairRoutes)):
        for j in range(num_vehicles):
            allVehicleRoutes[route_num, 0] = j
            allVehicleRoutes[route_num, 1] = allPairRoutes[i, 0]
            allVehicleRoutes[route_num, 2] = allPairRoutes[i, 1]
            allVehicleRoutes[route_num, 3] = allPairRoutes[i, 2]
            allVehicleRoutes[route_num, 4] = allPairRoutes[i, 3]
            route_num += 1

    for i in range(len(allVehicleRoutes)):
        distance = 0
        vehicleStartX, vehicleStartY = vehicle_lines[int(allVehicleRoutes[i, 0])].split(',')[1:3]
        Location1X, Location1Y = requests[int(allVehicleRoutes[i, 1])][0:2]
        Location2X, Location2Y = requests[int(allVehicleRoutes[i, 2])][0:2]
        Location3X, Location3Y = requests[int(allVehicleRoutes[i, 3])][0:2]
        Location4X, Location4Y = requests[int(allVehicleRoutes[i, 4])][0:2]

        distance += math.sqrt((int(vehicleStartX) - int(Location1X))**2 + (int(vehicleStartY) - int(Location1Y))**2)
        distance += math.sqrt((int(Location1X) - int(Location2X))**2 + (int(Location1Y) - int(Location2Y))**2)
        distance += math.sqrt((int(Location2X) - int(Location3X))**2 + (int(Location2Y) - int(Location3Y))**2)
        distance += math.sqrt((int(Location3X) - int(Location4X))**2 + (int(Location3Y) - int(Location4Y))**2)

        bestLocationStart[i, 0] = distance
        bestLocationStart[i, 1] = allVehicleRoutes[i, 0]
        bestLocationStart[i, 2] = allVehicleRoutes[i, 1]
        bestLocationStart[i, 3] = allVehicleRoutes[i, 2]

    print(bestLocationStart)
    return allVehicleRoutes, bestLocationStart, selectedBestLocationStart, finalVehicle
