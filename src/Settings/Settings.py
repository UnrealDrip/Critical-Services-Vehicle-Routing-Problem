mode = "Mixed"

#All File Locations
#data_file = f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}\\{num_requests}\\{mode}{num_requests}.{run}-Generic-data.txt'
#request_file = f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}RequestLocation\\{num_requests}\\{mode}{num_requests}.{run}-Request-data.txt'
#chromosome_file = f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\DataSet1-{pop_chromosomes}.{run}-Chromosome-data.txt'

#How many datasets to generate or run
dataset_num = 1

#Main Grid
min_grid_size = 1
max_grid_size = 999

#Grid for Zone A
min_region1_grid_size = 400
max_region1_grid_size = 599

#Grid for Zone B
min_region2_grid_size = 250
max_region2_grid_size = 749

#X:Y Ratio for Patient Home to Hospital(emergency_ratio) and Hospital to Patient Home
emergency_ratio = 0.3

#Generator Settings
num_hospitals = 30
num_vehicles = 100
num_requests = 10

#Chromosome Settings
chromosome_length = num_requests*2+1
pop_chromosomes = num_requests
num_chromosomes = 10000

#Request Data Settings
request_length =range(num_hospitals+num_vehicles+4,num_hospitals+num_vehicles+num_requests+4)

#Needs to be removed
vehicle_capacity = 2
min_vehicle_capacity = 1
max_vehicle_capacity= 3

#Chromsome Sampling Settings
num_chromosome_start =10
vehicle_rounds = num_requests/(num_vehicles*vehicle_capacity)



