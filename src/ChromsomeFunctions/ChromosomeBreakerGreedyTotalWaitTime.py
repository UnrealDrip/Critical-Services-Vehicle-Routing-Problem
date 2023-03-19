import math
import random
import multiprocessing
import itertools

import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings
sys.path.append("V:/Critical-Services-Routing/src/Tools")
import Tools

dataset_num = Settings.dataset_num
num_requests = Settings.num_requests
pop_chromosomes = Settings.pop_chromosomes
num_chromosome_start = Settings.num_chromosome_start
mode = Settings.mode
vehicle_capacity = Settings.vehicle_capacity
num_vehicles = Settings.num_vehicles
vehicle_rounds = Settings.vehicle_rounds

def getChromosome (run) :
    givenChromosomes = []
    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\DataSet1-{pop_chromosomes}.{run}-Chromosome-data.txt', 'r') as file:
            contents = file.read()
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        contents = None

    lines = contents.split('\n')

    random_index = random.sample(range(0,pop_chromosomes+1),num_chromosome_start)

    #Get Random Chromosome from File
    for chromosome in range(num_chromosome_start):
        #Formatting the Line
        selected_line = lines[random_index[chromosome]].lstrip('[{').rstrip(']}')
        current_chromosome = list(map(int, selected_line.split(',')))
        givenChromosomes.append(current_chromosome)
    return givenChromosomes

def convertChromosomeXY(givenChromosomes):
    chromosomesXY = []
    requests = []
    pairNum = -1
    pairIndex = []
    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}RequestLocation\\{num_requests}\\{mode}{num_requests}.1-Request-data.txt', 'r') as file:
            contents = file.read()
            requests = eval(contents)
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        requests = None

    for chromosome in givenChromosomes:
        pairNum = -1
        chromosomeXY = []
        for index in chromosome:
            isPickup = False
            if(index % 2 == 0):
                pairNum += 1
                pairIndex.append((index,pairNum))
                isPickup = True
                corresponding_value = index + 1
                corresponding_index = chromosome.index(corresponding_value)
                chromosomeXY.append(((int(requests[index][0]),int(requests[index][1]),isPickup,pairNum),(int(requests[corresponding_value][0]),int(requests[corresponding_value][1]),not isPickup,pairNum)))
        chromosomesXY.append(chromosomeXY)
    return chromosomesXY

def breakChromosome(chromosomesXY):
    for chromosome in chromosomesXY:
        all_vehicle_routes = []
        all_vehicle_end = []
        pickUpList = []
        dropOffList = []
        current_number = 0
        vehicles_required = 0
        requests_done = 0
        isPickup = False
        locationPair = -1
        temp_values = chromosome

    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}\\{num_requests}\\{mode}{num_requests}.1-Generic-data.txt', 'r') as file:
            vehicle_lines = file.readlines()[32:132]
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        vehicle_lines = None

    #Get Start and End Locations for each Vehicle
    for vehicle in range(num_vehicles):
        #Check if number of vehicles
        vehicles_required += 1
        if(vehicles_required>num_requests):
            break
        #Setup Vehicle Route
        locationPair -= 1
        vehicle_route = []
        vehicle_line = vehicle_lines[vehicle]
        vehicle_list = [int(x) for x in vehicle_line.split(',')]
        vehicle_start = (vehicle_list[1],vehicle_list[2],isPickup,locationPair)
        vehicle_end = (vehicle_list[3],vehicle_list[4],isPickup,locationPair)

        vehicle_route.append(vehicle_start)

        #Add Vehicle Start and End Locations to Lists
        all_vehicle_routes.append(vehicle_route)
        all_vehicle_end.append(vehicle_end)

    vehicle_rounds = int((len(chromosome)/2)/num_vehicles)
    if(vehicle_rounds<1):
        vehicle_rounds = 1
    for chromosome in chromosomesXY:
        for round in range(vehicle_rounds):
            chromosomePair = []
            distancePair = []
            usedVehicle = []
            finalRouteList = []
            RouteCombinationsTime = []
            for i in range(len(chromosome)):
                for j in range(i+1,len(chromosome)):
                    chromosomePair.append((chromosome[i], chromosome[j]))
            for pair in chromosomePair:
                isPickup = True
                pickUp1x = pair[0][0][0]
                pickUp1y = pair[0][0][1]
                pickUp2x = pair[1][0][0]
                pickUp2y = pair[1][0][1]

                dropOff1x = pair[0][1][0]
                dropOff1y = pair[0][1][1]
                dropOff2x = pair[1][1][0]
                dropOff2y = pair[1][1][1]

                locations = [( pickUp1x, pickUp1y,isPickup,pair[0][0][3]), ( pickUp2x, pickUp2y,isPickup,pair [1][0][3]), (dropOff1x, dropOff1y,not isPickup,pair[0][0][3]), ( dropOff2x, dropOff2y,not isPickup,pair[1][0][3])]
                filtered_permutations = [perm for perm in itertools.permutations(locations) if perm.index(( pickUp1x, pickUp1y,isPickup,pair[0][0][3])) < perm.index(( dropOff1x, dropOff1y,not isPickup,pair[0][0][3])) and perm.index(( pickUp2x, pickUp2y,isPickup,pair[1][0][3])) < perm.index((dropOff2x, dropOff2y,not isPickup,pair[1][0][3]))]

                for route in filtered_permutations:
                    print (list(route))
                    vehicles_required = 0
                    for vehicle in range(num_vehicles):
                        vehicles_required += 1

                        if(vehicles_required>num_requests):
                            break

                        vehicle_route = all_vehicle_routes[vehicle][0]
                        for i in range(len(route)):
                            vehicle_route.append(route[i])

                        print(vehicle_route)
                        totalVehicleWaitTime = 0

                        for location in vehicle_route:
                            #Check if location is a pickup location
                            if location[2]== True:
                                #Quick Maths
                                location_x1,location_y1=vehicle_route[0][0],vehicle_route[0][1]
                                location_x2,location_y2=int(location[0]),int(location[1])
                                waitTime = math.sqrt((location_x2-location_x1)**2 + (location_y2-location_y1)**2)
                                totalVehicleWaitTime += waitTime

                        RouteCombinationsTime.append((totalVehicleWaitTime,vehicle_route))

            RouteCombinationsTime.sort(key=lambda x: x[0])
            #print(len(RouteCombinationsTime))
            vehicles_required = 0
            for vehicle in range(num_vehicles):
                #print(vehicles_required)
                vehicles_required += 1
                if(vehicles_required>num_requests):
                    break
                print (RouteCombinationsTime[0][1][0][3])
                print(usedVehicle)
                if memberCheck(int(RouteCombinationsTime[0][1][0][3]),usedVehicle):
                    print("ß")
                    print(usedVehicle)
                    RouteCombinationsTime.pop(0)
                else:
                    print(RouteCombinationsTime[0][1][0]+RouteCombinationsTime[0][1][1]+RouteCombinationsTime[0][1][2])
                    finalRouteList.append(RouteCombinationsTime[0])
                    usedVehicle.append(RouteCombinationsTime[0][1][0][3])
                    print(type(usedVehicle[0]))
                    RouteCombinationsTime.pop(0)
                    break

            print(finalRouteList)
            #print(len(finalRouteList))
def main():
    givenChromosomes = getChromosome(1)
    chromosomesXY = convertChromosomeXY(givenChromosomes)
    breakChromosome(chromosomesXY)

def memberCheck(num,usedVehicle):
    for i in usedVehicle:
        if i == num :
            return True

    return False


if __name__ == "__main__":
    processes = []
    for run in range(dataset_num):
        p1 = multiprocessing.Process(target=main)
        processes.append(p1)
        #p2 = multiprocessing.Process(target=requestFileMake, args=(run,))
        #processes.append(p2)
        #p3 = multiprocessing.Process(target=chromosomeFileMake, args=(run,))
        #processes.append(p3)
    for p in processes:
        p.start()
    for p in processes:
        p.join()