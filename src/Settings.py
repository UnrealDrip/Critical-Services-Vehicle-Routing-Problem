mode = "Mixed"
dataset_num = 1
data_file = f'V:\\Critical-Services-Routing\\src\\Data\\\\Fixed\\10\\{mode}10.-Generic-data.txt'
request_file = f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Request-data.txt'
chromosome_file = 'V:\Critical-Services-Routing\src\Data\Chromosome-data.txt'
num_hospitals = 30
num_vehicles = 100
num_requests = 10
pop_chromosomes = num_requests
emergency_ratio = 0.3
min_vehicle_capacity = 1
max_vehicle_capacity= 3
min_grid_size = 1
max_grid_size = 999
min_region1_grid_size = 400
max_region1_grid_size = 599
min_region2_grid_size = 250
max_region2_grid_size = 749
#min_region3_grid_size = 1
#max_region3_grid_size = 999
chromosome_length = num_requests*2+1
request_length =range(num_hospitals+num_vehicles+4,num_hospitals+num_vehicles+num_requests+4)
num_chromosomes = 10000
num_chromosome_start =10



