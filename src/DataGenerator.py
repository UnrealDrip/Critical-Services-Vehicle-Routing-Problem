import random

data_file = 'generated-data.txt'
num_hospitals = 15
num_vehicles = 100
num_requests = 1000
min_vehicle_capacity = 0
max_vehicle_capacity= 3
min_grid_size = 1
max_grid_size = 999

def writeFile():
    hospital_data = {}

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
        random_x = str(random.randint(min_grid_size, max_grid_size))
        random_y = str(random.randint(min_grid_size, max_grid_size))
        random_capacity = str(random.randint(min_vehicle_capacity,max_vehicle_capacity))
        random_hospital = random.choice(list(hospital_data.keys()))
        hospital_x = str(hospital_data[random_hospital]["x"])
        hospital_y = str(hospital_data[random_hospital]["y"])
        file.write(str(vehicle) + "," + random_x + "," + random_y + "," + hospital_x + "," + hospital_y + ","+ random_capacity+"\n")

    file.write("REQUESTS,{0}\n".format(num_requests))
    for request in range(num_requests):
        random_x = str(random.randint(min_grid_size, max_grid_size))
        random_y = str(random.randint(min_grid_size, max_grid_size))
        random_hospital = random.choice(list(hospital_data.keys()))
        hospital_x = str(hospital_data[random_hospital]["x"])
        hospital_y = str(hospital_data[random_hospital]["y"])
        file.write(str(request) + "," + random_x + "," + random_y + "," + hospital_x + "," + hospital_y +"\n")

    file.close()


def readFile():
    file = open (data_file,'r')
    line = file.readline().strip()
    print (line)
    file.close()
    values = line.split(",")
    print(values)

writeFile()
readFile()

