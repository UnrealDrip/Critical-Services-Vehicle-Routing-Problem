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
    return brokenChromosomes

def breakChromosome(selected_chromosome,file_run):
    vehicle_rounds = int((len(selected_chromosome)/2)/num_vehicles)
    ##print(vehicle_rounds)
    all_vehicle_routes = []
    all_vehicle_end = []
    vehicles_required = 0
    requests_done = 0
    isPickup = False
    locationPair = -1

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

    #print(all_vehicle_end)
    #print(all_vehicle_routes)

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
            #Reset Values
            locationPair = -1
            #Check if all Requests have been done
            requests_done += 1
            if(requests_done>num_requests):
                break

            vehicle_route = all_vehicle_routes[vehicle]

            vehicle_index_route = []
            random_index_values = []
            temp_values = []
            random_numbers = Tools.get_nonconsecutive_random_numbers(len(selected_chromosome), vehicle_capacity)
            random_values = random_numbers

            #Convert Random Numbers to Indexes in Chromosome
            for current_index in range(len(random_numbers)):
                index = selected_chromosome[random_numbers[0]]
                random_index_values.append(index)
                random_numbers.pop(0)

            #Get Corresponding Indexes in Chromosome and Random Numbers
            for current_index in range(len(random_index_values)):
                index = random_index_values[current_index]
                corresponding_index = 0
                #Check Even or Odd and give corresponding index
                if (index % 2) == 0 :
                    corresponding_index = index + 1
                else:
                    corresponding_index = index - 1
                #Get Corresponding Random Index Value
                vehicle_index_route.append(index)
                vehicle_index_route.append(corresponding_index)

            #Make the Values in Ascending order to maintain chromosome order
            for current_index in range(len(vehicle_index_route)):
                index = vehicle_index_route[current_index]
                index_position = Tools.find_index(selected_chromosome,index)
                temp_values.append((index,index_position))

            sorted_values_byChromsome = sorted(temp_values, key=lambda x: x[1])
            #print(sorted_values)
            vehicle_index_route = []

            #Convert Sorted Indexes in Chromosome

            sorted_values_byIndexValue = sorted(temp_values, key=lambda x: x[0])
            for current_index in range(len(sorted_values_byIndexValue)):
                # If the current index is even,increase number
                if current_index % 2 == 0:
                    locationPair += 1

                sorted_values_byIndexValue[current_index] += (locationPair,)

                #Convert Sorted Indexes in Chromosome
                index = sorted_values_byChromsome[current_index][0]

                vehicle_index_route.append((index,locationPair))

            #print(vehicle_index_route)
            #Convert Indexes in Chromosome to Requests
            for current_index in range(len(vehicle_index_route)):
                index = vehicle_index_route[current_index][0]
                isPickup = False
                locationPair = current_index
                if (index % 2) == 0 :
                    isPickup = True
                converted = (int(requests[index][0]), int(requests[index][1]), isPickup,vehicle_index_route[current_index][1])
                vehicle_route.append(converted)

            #Add Vehicle Routes to All Vehicle Routes
            vehicle_route.append(all_vehicle_end[vehicle])
            ##print(vehicle_route)
            all_vehicle_routes[vehicle] = vehicle_route

    #print (all_vehicle_routes)
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