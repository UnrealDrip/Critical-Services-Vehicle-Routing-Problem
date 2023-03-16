import multiprocessing
import random
import math
import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings
sys.path.append("V:/Critical-Services-Routing/src/FitnessFunctions")
import Fitness
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

current_chromosome = []
brokenChromosomes = []


def getChromosome (run) :
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
        selected_line = lines[random_index[0]].lstrip('[{').rstrip(']}')
        random_index.pop(0)
        current_chromosome = list(map(int, selected_line.split(',')))

        #break chromosome into many routes
        brokenChromosomes.append(breakChromosome(current_chromosome,run))

    #Calculate Euclidean Distance for each route
    #calculateEuclideanDistance(brokenChromosomes)
    Fitness.calculateTotalWaitTime(brokenChromosomes)
    Fitness.calculateTotalArrivalTime(brokenChromosomes)
    Fitness.calculateMaximumWaitTime(brokenChromosomes)
    Fitness.calculateMaximumArrivalTime(brokenChromosomes)
    #Tools.averageDistanceCovered(brokenChromosomes)
    return brokenChromosomes

def breakChromosome(selected_chromosome,file_run):
    vehicle_rounds = int((len(selected_chromosome)/2)/num_vehicles)
    indices = {num: i for i, num in enumerate(selected_chromosome)}
    all_vehicle_routes = []
    all_vehicle_end = []
    pickUpList = []
    dropOffList = []
    current_number = 0
    vehicles_required = 0
    requests_done = 0
    isPickup = False
    locationPair = -1
    temp_values = selected_chromosome

    #Load Vehicle Data into Memory
    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}\\{num_requests}\\{mode}{num_requests}.{file_run}-Generic-data.txt', 'r') as file:
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
        vehicle_route = []
        vehicle_line = vehicle_lines[vehicle]
        vehicle_list = [int(x) for x in vehicle_line.split(',')]
        vehicle_start = (vehicle_list[1],vehicle_list[2],isPickup,locationPair)
        vehicle_end = (vehicle_list[3],vehicle_list[4],isPickup,locationPair)

        vehicle_route.append(vehicle_start)

        #Add Vehicle Start and End Locations to Lists
        all_vehicle_routes.append(vehicle_route)
        all_vehicle_end.append(vehicle_end)

    #Load Requests into Memory
    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}RequestLocation\\{num_requests}\\{mode}{num_requests}.{file_run}-Request-data.txt', 'r') as file:
            contents = file.read()
            requests = eval(contents)
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        requests = None


    #Check Number of Times Vehicle has to be Routed
    if(vehicle_rounds<1):
        vehicle_rounds = 1

    for vehicle_round in range(int(vehicle_rounds)):
        for vehicle in range(num_vehicles):
            #Check if all Requests have been done
            requests_done += 1
            if(requests_done>num_requests):
                break

            #Reset Values
            locationPair = -1
            vehicle_route = []
            vehicle_route = all_vehicle_routes[vehicle]
            vehicle_index_route = []

            for i in range (vehicle_capacity):
                even_numbers_indices = []
                odd_following_indices = []
                even_count = 0
                for i, num in enumerate(temp_values):
                    if num % 2 == 0 and even_count < 1:
                        even_numbers_indices.append(num)
                        vehicle_index_route.append(num)
                        even_count += 1
                        odd_following_indices.append(num+1)
                        vehicle_index_route.append(num+1)
                    elif even_count == 1:
                        break
                # Remove the used numbers from the list
                indices_to_delete = even_numbers_indices + odd_following_indices
                indices_to_delete.sort(reverse=True)
                for i in indices_to_delete:
                    del temp_values[temp_values.index(i)]

            # Sort the numbers to arrange list by their corresponding indices in the
            # selected_chromosome list using the indices dictionary
            sorted_vehicle_route = sorted(vehicle_index_route, key=lambda num: indices[num])

            for current_index in range(len(sorted_vehicle_route)):
                # If the current index is even,increase number
                isPickup = False
                if current_index % 2 == 0:
                    isPickup = True
                    locationPair += 1

                vehicle_route.append((requests[sorted_vehicle_route[current_index]][0],requests[sorted_vehicle_route[current_index]][1],isPickup,locationPair))


            all_vehicle_routes[vehicle].append(vehicle_route)

    requests_done = 0
    for vehicle in range(num_vehicles):
        requests_done += 1
        if(requests_done>num_requests):
            break
        all_vehicle_routes[vehicle].append(all_vehicle_end[vehicle])

    return all_vehicle_routes


if __name__ == '__main__':
    processes = []
    for run in range(dataset_num):
        p1 = multiprocessing.Process(target=getChromosome, args=(run,))
        processes.append(p1)
        #p2 = multiprocessing.Process(target=requestFileMake, args=(run,))
        #processes.append(p2)
        #p3 = multiprocessing.Process(target=chromosomeFileMake, args=(run,))
        #processes.append(p3)
    for p in processes:
        p.start()
    for p in processes:
        p.join()