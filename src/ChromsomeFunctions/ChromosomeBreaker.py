import Settings
import multiprocessing
import random

dataset_num = Settings.dataset_num
num_requests = Settings.num_requests
pop_chromosomes = Settings.pop_chromosomes
num_chromosome_start = Settings.num_chromosome_start
mode = Settings.mode
vehicle_capacity = 2
num_vehicles = Settings.num_vehicles
current_chromosome = []

def getChromosome (run) :
    with open(f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\DataSet1-{pop_chromosomes}.{run}-Chromosome-data.txt', 'r') as file:
        contents = file.read()
        lines = contents.split('\n')
        random_index = random.sample(range(0,pop_chromosomes+1),num_chromosome_start)
        brokenChromosomes = []
        for chromosome in range(num_chromosome_start):
            #print(random_index[0])
            selected_line = lines[random_index[0]].lstrip('[{').rstrip(']}')
            #print(selected_line)
            random_index.pop(0)
            current_chromosome = list(map(int, selected_line.split(',')))
            #print(current_chromosome)
            brokenChromosomes.append(breakChromosome(current_chromosome,run))

    return brokenChromosomes

def breakChromosome(selected_chromosome,file_run):
    vehicle_rounds = int((len(selected_chromosome)/2)/num_vehicles)
    #print(vehicle_rounds)
    all_vehicle_routes = []
    all_vehicle_end = []
    vehicles_required = 0
    with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}\\{num_requests}\\{mode}{num_requests}.{file_run}-Generic-data.txt','r') as file:
        vehicle_lines = file.readlines()[32:132]
        for vehicle in range(num_vehicles):
            vehicles_required += 1
            if(vehicles_required>num_requests):
                break
            vehicle_route = []
            vehicle_line = vehicle_lines[vehicle]

            vehicle_list = [int(x) for x in vehicle_line.split(',')]
            vehicle_start = (vehicle_list[1],vehicle_list[2])
            vehicle_end = (vehicle_list[3],vehicle_list[4])

            vehicle_route.append(vehicle_start)

            all_vehicle_routes.append(vehicle_route)
            all_vehicle_end.append(vehicle_end)

    #print(all_vehicle_end)
    #print(all_vehicle_routes)
    with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}RequestLocation\\{num_requests}\\{mode}{num_requests}.{file_run}-Request-data.txt','r') as file:
        contents = file.read()
        requests = eval(contents)
        requests_done = 0
        rounds = num_requests/(num_vehicles*vehicle_capacity)
        if(rounds<1):
            rounds = 1
        for round in range(int(rounds)):
            for vehicle in range(num_vehicles):
                requests_done += 1
                if(requests_done>num_requests):
                    break

                vehicle_route = all_vehicle_routes[vehicle]
                vehicle_index_route = []
                random_numbers = get_nonconsecutive_random_numbers(len(selected_chromosome), vehicle_capacity)
                random_index_values = []
                random_values = random_numbers
                for current_index in range(len(random_numbers)):
                    index = selected_chromosome[random_numbers[0]]
                    random_index_values.append(index)
                    random_numbers.pop(0)
                for current_index in range(len(random_index_values)):
                    index = random_index_values[current_index]
                    corresponding_index = 0
                    if (index % 2) == 0:
                        corresponding_index = index + 1
                    else:
                        corresponding_index = index - 1
                    correspondind_random_value = find_index(selected_chromosome,corresponding_index)
                    random_values.append(correspondind_random_value)

                random_values.sort()
                for current_index in range(len(random_values)):
                    index = selected_chromosome[random_values[0]]
                    random_values.pop(0)
                    vehicle_index_route.append(index)
                for current_index in range(len(vehicle_index_route)):
                    index = vehicle_index_route[current_index]
                    converted = (int(requests[index][0]), int(requests[index][1]))
                    vehicle_route.append(converted)

                vehicle_route.append(all_vehicle_end[vehicle])
                all_vehicle_routes[vehicle] = vehicle_route
    print (all_vehicle_routes)
    return all_vehicle_routes


def get_nonconsecutive_random_numbers(max_num, count):
    # Generate the first random number
    nums = [random.randint(0, max_num-1)]
    # Keep generating random numbers until we have enough
    while len(nums) < count:
        # Generate a new random number
        num = random.randint(0, max_num-1)
        # Check if it is consecutive with the last number
        if num != nums[-1] + 1:
            nums.append(num)
    return nums

def find_index(selected_list, value):
    try:
        index = selected_list.index(value)
    except ValueError:
        # Value not found in list
        index = -1  # or some other value to indicate not found
    return index


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