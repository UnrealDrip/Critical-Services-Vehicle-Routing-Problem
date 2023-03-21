import random
import pprint
import math
import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings

num_vehicles = Settings.num_vehicles

#Generates Non-Consecutive Random Numbers like 1,4,7,10
def get_nonconsecutive_random_numbers(max_num, count):
    run = True
    #Loop to run until non-consecutive numbers are generated
    while(run):
        random_numbers = random.sample(range(0, max_num-1), count)
        if(random_numbers[0]+3 <= random_numbers[1] or random_numbers[0]-3 >= random_numbers[1] ):
            return random_numbers

#Get Index of a Value from a List
def find_index(selected_list, value):
    try:
        index = selected_list.index(value)
    except ValueError:
        index = -1
        all_numbers = set(range(200))
        missing_numbers = all_numbers - set(selected_list)
        print(sorted(list(missing_numbers)))
        print("Value not found in List",value)
    return index

#Calculate Euclidean Distance using Formula : sqrt((x2-x1)^2 + (y2-y1)^2)
def calculateEuclideanDistance(brokenChromosomes):
    for chromosome in brokenChromosomes:
        check = 0
        chromosome_distance = 0
        for vehicle_route in chromosome:
            total_distance = 0
            pprint.pprint(len(vehicle_route))
            pprint.pprint(vehicle_route)
            for i in range(len(vehicle_route)):
                location_x1, location_y1 = vehicle_route[i][0], vehicle_route[i][1]

                ##Some Part is Corrupt or Something but this fixes it
                if not isinstance(location_x1, int):
                    #print(location_x1[0], location_y1[0])
                    location_x1 = location_x1[0]
                    #print(type(location_x1), type(location_y1))
                    location_x1= int(location_x1)
                if not isinstance(location_y1, int):
                    #print(type(location_x1), type(location_y1))
                    location_y1 =location_y1[0]
                    location_y1 = location_y1[0]
                    #if not isinstance(location_y2, tuple):
                    location_y1 = int(location_y1)

                if i == len(vehicle_route) - 1:
                    break
                location_x2, location_y2 = vehicle_route[i+1][0], vehicle_route[i+1][1]

                ##Some Part is Corrupt or Something but this fixes it
                if not isinstance(location_x2, int):
                    #print(location_x2[0], location_y2[0])
                    location_x2 = location_x2[0]
                    #print(type(location_x2), type(location_y2))
                    location_x2= int(location_x2)
                if not isinstance(location_y2, int):
                    #print(type(location_x2), type(location_y2))
                    location_y2 =location_y2[0]
                    location_y2 = location_y2[0]
                    #if not isinstance(location_y2, tuple):
                    location_y2 = int(location_y2)

                distance = math.sqrt((location_x2-location_x1)**2 + (location_y2-location_y1)**2)
                check += 1
                total_distance += distance

            chromosome_distance += total_distance
            #print(int(total_distance))
        print("Total Distance Average for Vehicle: ",check, int(chromosome_distance)/num_vehicles)


def averageDistanceCovered (brokenChromosomes):
    for chromosome in brokenChromosomes:
        total_distance = 0
        for vehicle in chromosome:
            vehicle_distance = 0
            current_index = -1
            for location in vehicle:
                current_index +=1
                location_x1,location_x2 = int(location[0]),int(location[1])
                if current_index+1 < len(vehicle):
                    next_location = vehicle[current_index+1]
                    next_location_x, next_location_y = next_location[0], next_location[1]
                    distance = math.sqrt((int(next_location_x)-location_x1)**2 + (int(next_location_y)-location_x2)**2)
                    vehicle_distance += distance
            total_distance += vehicle_distance
        print("Total Distance Average for Vehicle: ", int(total_distance)/num_vehicles)
