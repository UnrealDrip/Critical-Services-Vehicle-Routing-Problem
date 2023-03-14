import random
import multiprocessing
import os
import sys
sys.path.append("V:/Critical-Services-Routing/src/ChromsomeFunctions")
import Settings


mode = Settings.mode
emergency_ratio = Settings.emergency_ratio
#data_file = Settings.data_file
dataset_num = Settings.dataset_num
#request_file = Settings.request_file
num_hospitals = Settings.num_hospitals
num_vehicles = Settings.num_vehicles
#num_requests = Settings.num_requests
num_requests = [10,20,50,100,200,500,1000,2000,5000,10000]
min_vehicle_capacity = Settings.min_vehicle_capacity
max_vehicle_capacity= Settings.max_vehicle_capacity
min_grid_size = Settings.min_grid_size
max_grid_size = Settings.max_grid_size
request_length= Settings.request_length
pop_chromosomes = Settings.pop_chromosomes
num_chromosomes = Settings.num_chromosomes

def genericFileMake(run):
    print(run)
    hospital_data = {}
    data_file = f'V:\\Critical-Services-Routing\\src\\Data\\Fixed-Data\\Fixed\\{num_requests}\\{mode}{num_requests}.{run}-Generic-data.txt'
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
        random_hospital1 = random.choice(list(hospital_data.keys()))
        hospital_x1 = str(hospital_data[random_hospital1]["x"])
        hospital_y1 = str(hospital_data[random_hospital1]["y"])
        random_capacity = str(random.randint(min_vehicle_capacity,max_vehicle_capacity))
        random_hospital2 = random.choice(list(hospital_data.keys()))
        hospital_x2 = str(hospital_data[random_hospital2]["x"])
        hospital_y2 = str(hospital_data[random_hospital2]["y"])
        file.write(str(vehicle) + "," + hospital_x1 + "," + hospital_y1 + "," + hospital_x2 + "," + hospital_y2+ ","+ random_capacity+"\n")

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
    data_file = f'V:\\Critical-Services-Routing\\src\\Data\\Fixed-Data\\Fixed\\{num_requests}\\{mode}{num_requests}.{run}-Generic-data.txt'
    request_file = f'V:\\Critical-Services-Routing\\src\\Data\\Fixed-Data\\FixedRequestLocation\\{num_requests}\\{mode}{num_requests}.{run}-Request-data.txt'
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

def chromosomeFileMake(run,type):
    with open(f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests[type]}\\DataSet1-{num_requests[type]}.{run}-Chromosome-data.txt', 'w') as file:

        for i in range(num_chromosomes):
            random_numbers = random.sample(range(0, num_requests[type]), int(num_requests[type]))
            chromosome = []

            for j in range(int(num_requests[type])):
                chromosome.append(0)

            sorted_numbers = random_numbers

            sorted_numbers= sorted(random_numbers)
            random_numbers = random.sample(range(0, int(num_requests[type])), int(num_requests[type]))

            for k in range(int(num_requests[type]/2)):
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
    print(str(run)+"Lool"+str(num_requests[type]))

def renameFiles(run):
    oldFile = f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\{mode}-{pop_chromosomes}.{run}-Chromosome-data.txt'
    newFile = f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\DataSet1-{pop_chromosomes}.{run}-Chromosome-data.txt'
    os.rename(oldFile,newFile)


if __name__ == '__main__':
    processes = []
    for type in range(10):
        for run in range(dataset_num):
            #p1 = multiprocessing.Process(target=genericFileMake, args=(run,))
            #processes.append(p1)
            #p2 = multiprocessing.Process(target=requestFileMake, args=(run,))
            #processes.append(p2)
            p3 = multiprocessing.Process(target=chromosomeFileMake, args=(run,type,))
            processes.append(p3)
            #p4 = multiprocessing.Process(target=renameFiles, args=(run,))
            #processes.append(p4)
    for p in processes:
        p.start()
    for p in processes:
        p.join()

