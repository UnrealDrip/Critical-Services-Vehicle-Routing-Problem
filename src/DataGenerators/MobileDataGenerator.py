import random
import Settings
import multiprocessing


mode = Settings.mode
emergency_ratio = Settings.emergency_ratio
#data_file = Settings.data_file
dataset_num = Settings.dataset_num
#request_file = Settings.request_file
num_hospitals = Settings.num_hospitals
num_vehicles = Settings.num_vehicles
num_requests = Settings.num_requests
min_vehicle_capacity = Settings.min_vehicle_capacity
max_vehicle_capacity= Settings.max_vehicle_capacity
min_grid_size = Settings.min_grid_size
max_grid_size = Settings.max_grid_size
request_length= Settings.request_length
pop_chromosomes = Settings.pop_chromosomes
num_chromosomes = Settings.num_chromosomes
min_region1_grid_size = Settings.min_region1_grid_size
max_region1_grid_size = Settings.max_region1_grid_size
min_region2_grid_size = Settings.min_region2_grid_size
max_region2_grid_size = Settings.max_region1_grid_size

def genericFileMake(run):
    print(run)
    hospital_data = {}
    data_file = f'V:\\Critical-Services-Routing\\src\\Data\\Mobile-Data\\Mobile\\{num_requests}\\{mode}{num_requests}.{run}-Generic-data.txt'
    file = open(data_file,'w+')

    file.write("HOSPITAL,{0}\n".format(num_hospitals))
    for hospital in range(num_hospitals):
        random_x = str(random.randint(min_grid_size, max_grid_size))
        random_y = str(random.randint(min_grid_size, max_grid_size))
        hospital_data[hospital] = {"x": random_x, "y": random_y}

    for hospital, data in hospital_data.items():
        file.write(str(hospital) + "," + str(data["x"]) + "," + str(data["y"]) + "\n")


    file.write("VEHICLES,{0}\n".format(num_vehicles))
    for vehicle in range(num_vehicles):
        distribution_ratio = random.randint(1, 6)
        random_capacity = str(random.randint(min_vehicle_capacity,max_vehicle_capacity))
        if(distribution_ratio<=3):
            random_x1 = str(random.randint(min_region1_grid_size, max_region1_grid_size))
            random_y1 = str(random.randint(min_region1_grid_size, max_region1_grid_size))
            random_x2 = str(random.randint(min_region1_grid_size, max_region1_grid_size))
            random_y2 = str(random.randint(min_region1_grid_size, max_region1_grid_size))
            file.write(str(vehicle) + "," + str(random_x1) + "," + str(random_y1) + "," + str(random_x2)+ "," +str(random_y2)+ ","+ str(random_capacity)+"\n")

        elif (distribution_ratio>=5):
            while True:
                random_x1 = random.randint(min_region2_grid_size, max_region2_grid_size)
                random_y1 = random.randint(min_region2_grid_size, max_region2_grid_size)
                random_x2 = random.randint(min_region2_grid_size, max_region2_grid_size)
                random_y2 = random.randint(min_region2_grid_size, max_region2_grid_size)
                if (random_x1 > max_region1_grid_size or random_x1 < min_region1_grid_size) and (random_y1 > max_region1_grid_size or random_y1 < min_region1_grid_size):
                    if (random_x2 > max_region1_grid_size or random_x2 < min_region1_grid_size) and (random_y2 > max_region1_grid_size or random_y2 < min_region1_grid_size):
                        break
            file.write(str(vehicle) + "," + str(random_x1) + "," + str(random_y1) + "," + str(random_x2)+ "," +str(random_y2)+ ","+ str(random_capacity)+"\n")
        elif(distribution_ratio==4):
            while True:
                random_x1 = random.randint(min_grid_size, max_grid_size)
                random_y1 = random.randint(min_grid_size, max_grid_size)
                random_x2 = random.randint(min_grid_size, max_grid_size)
                random_y2 = random.randint(min_grid_size, max_grid_size)
                if (random_x1 > max_region2_grid_size or random_x1 < min_region2_grid_size) and (random_y1 > max_region2_grid_size or random_y1 < min_region2_grid_size):
                    if (random_x2 > max_region2_grid_size or random_x2 < min_region2_grid_size) and (random_y2 > max_region2_grid_size or random_y2 < min_region2_grid_size):
                        break
            file.write(str(vehicle) + "," + str(random_x1) + "," + str(random_y1) + "," + str(random_x2)+ "," +str(random_y2)+ ","+ str(random_capacity)+"\n")

    file.write("REQUESTS,{0}\n".format(num_requests))
    for request in range(num_requests):
        random_x = str(random.randint(min_grid_size, max_grid_size))
        random_y = str(random.randint(min_grid_size, max_grid_size))
        random_hospital = random.choice(list(hospital_data.keys()))
        hospital_x = str(hospital_data[random_hospital]["x"])
        hospital_y = str(hospital_data[random_hospital]["y"])
        if random.random() <= emergency_ratio:
            file.write(str(request) + "," + random_x + "," + random_y + "," + hospital_x + "," + hospital_y +"\n")
        else:
            file.write(str(request) + "," + hospital_x + "," + hospital_y + "," + random_x + "," + random_y +"\n")

    file.close()

def requestFileMake(run):
    print(run)
    data_file = f'V:\\Critical-Services-Routing\\src\\Data\\Mobile-Data\\Mobile\\{num_requests}\\{mode}{num_requests}.{run}-Generic-data.txt'
    request_file = f'V:\\Critical-Services-Routing\\src\\Data\\Mobile-Data\\MobileRequestLocation\\{num_requests}\\{mode}{num_requests}.{run}-Request-data.txt'
    with open(request_file,'w') as request_database:
        with open(data_file,'r') as generic_file:
            request_list =[]
            for i, line in enumerate(generic_file):
                    if i+1 in request_length:
                        request_segments = line.strip().split(",")
                        request_list.append((request_segments[1],request_segments[2]))
                        request_list.append((request_segments[3],request_segments[4]))
                    elif i+1 > max(request_length):
                        break
            request_database.write(str(request_list))

def chromosomeFileMake(run):
    with open(f'V:\\Critical-Services-Routing\\src\\Data\\Mobile-Data\\ChromosomeMobilePool\\{num_requests}\\{mode}-{pop_chromosomes}.{run}-Chromosome-data.txt', 'w') as file:

        for i in range(num_chromosomes):
            random_numbers = random.sample(range(0, pop_chromosomes+1), int(pop_chromosomes/2))
            chromosome = []

            for j in range(int(pop_chromosomes)):
                chromosome.append(0)

            for a in range(int(pop_chromosomes/2)):
                if random_numbers[a]%2 == 0:
                    random_numbers.append(random_numbers[a]+1)
                else:
                    random_numbers.append(random_numbers[a]-1)

            sorted_numbers= sorted(random_numbers)
            random_numbers = random.sample(range(0, int(pop_chromosomes)), int(pop_chromosomes))


            for k in range(int(pop_chromosomes/2)):
                if random_numbers[0]>random_numbers[1]:
                    chromosome[random_numbers[0]]=sorted_numbers[1]
                    chromosome[random_numbers[1]]=sorted_numbers[0]
                if random_numbers[0]<random_numbers[1] :
                    chromosome[random_numbers[0]]=sorted_numbers[0]
                    chromosome[random_numbers[1]]=sorted_numbers[1]

                random_numbers.pop(0)
                random_numbers.pop(0)
                sorted_numbers.pop(0)
                sorted_numbers.pop(0)

            file.write(str(chromosome)+"\n")
    print(run)


if __name__ == '__main__':
    processes = []
    for run in range(dataset_num):
        p1 = multiprocessing.Process(target=genericFileMake, args=(run,))
        processes.append(p1)
        p2 = multiprocessing.Process(target=requestFileMake, args=(run,))
        processes.append(p2)
        p3 = multiprocessing.Process(target=chromosomeFileMake, args=(run,))
        processes.append(p3)
    for p in processes:
        p.start()
    for p in processes:
        p.join()


