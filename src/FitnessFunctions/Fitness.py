import math

def calculateTotalWaitTime(brokenChromosomes,original_chromosomes):
    calculatedChromosomes = []
    for i in range(len(brokenChromosomes)):
        chromosomeWaitTime = 0
        chromosomeAverageWaitTime = 0
        for vehicle_route in brokenChromosomes[i]:
            #Wait Time is the Distance between the first location and the location where the vehicle is waiting
            totalVehicleWaitTime = 0
            for location in vehicle_route:
                #Check if location is a pickup location
                if location[2]== True:
                    #Quick Maths
                    location_x1,location_y1=vehicle_route[0][0],vehicle_route[0][1]
                    location_x2,location_y2=int(location[0]),int(location[1])
                    waitTime = math.sqrt((location_x2-location_x1)**2 + (location_y2-location_y1)**2)
                    totalVehicleWaitTime += waitTime
            #print("Vehicle :"+str(vehicle_route)+" Total Wait Time :"+str(totalVehicleWaitTime))
            chromosomeWaitTime += totalVehicleWaitTime

        chromosomeAverageWaitTime += chromosomeWaitTime/len(brokenChromosomes[i])
        #print("Average Wait Time :"+str(chromosomeAverageWaitTime))
        calculatedChromosomes.append((chromosomeAverageWaitTime,original_chromosomes[i]))
    sortedCalculatedChromosomes = sorted(calculatedChromosomes,key = lambda x: x[0])
    return sortedCalculatedChromosomes

def calculateMaximumWaitTime(brokenChromosomes):
    for chromosome in brokenChromosomes:
        maximumChromosomeWaitTime = 0
        vehicleWaitTimes = []
        for vehicle_route in chromosome:
            #Wait Time is the Distance between the first location and the location where the vehicle is waiting
            totalVehicleWaitTime = 0
            for location in vehicle_route:
                #Check if location is a pickup location
                if location[2]== True:
                    #Quick Maths
                    location_x1,location_y1=vehicle_route[0][0],vehicle_route[0][1]
                    location_x2,location_y2=int(location[0]),int(location[1])
                    waitTime = math.sqrt((location_x2-location_x1)**2 + (location_y2-location_y1)**2)
                    totalVehicleWaitTime += waitTime
                    #print("Vehicle :"+str(vehicle_route)+" Total Wait Time :"+str(totalVehicleWaitTime))
            vehicleWaitTimes.append(totalVehicleWaitTime)
        maximumChromosomeWaitTime = max(vehicleWaitTimes)
        print("Maximum Wait Time :"+str(maximumChromosomeWaitTime))

def calculateTotalArrivalTime(brokenChromosomes):
    for chromosome in brokenChromosomes:
        chromosomeArrivalTime = 0
        chromosomeAverageArrivalTime = 0
        for vehicle_route in chromosome:
            totalVehicleArrivalTime = 0
            for location in vehicle_route:
                if location[2] == True and location[3] != -1:
                    location_pair_1 = location[3]
                    location_x1,location_y1=vehicle_route[0][0],vehicle_route[0][1]
                    for i in range(len(vehicle_route)):
                        if vehicle_route[i][3] == location_pair_1:
                            location_x2,location_y2=int(vehicle_route[i][0]),int(vehicle_route[i][1])
                            arrivalTime = math.sqrt((location_x2-location_x1)**2 + (location_y2-location_y1)**2)
                            totalVehicleArrivalTime += arrivalTime
            chromosomeArrivalTime += totalVehicleArrivalTime
        chromosomeAverageArrivalTime += chromosomeArrivalTime/len(chromosome)
        print ("Average Arrival Time :"+str(chromosomeAverageArrivalTime))

def calculateMaximumArrivalTime(brokenChromosomes):
    for chromosome in brokenChromosomes:
        maximumChromosomeArrivalTime = 0
        chromosomeArrivalTimes =[]
        for vehicle_route in chromosome:
            totalVehicleArrivalTime = 0
            for location in vehicle_route:
                if location[2] == True and location[3] != -1:
                    location_pair_1 = location[3]
                    location_x1,location_y1=vehicle_route[0][0],vehicle_route[0][1]
                    for i in range(len(vehicle_route)):
                        if vehicle_route[i][3] == location_pair_1:
                            location_x2,location_y2=int(vehicle_route[i][0]),int(vehicle_route[i][1])
                            arrivalTime = math.sqrt((location_x2-location_x1)**2 + (location_y2-location_y1)**2)
                            totalVehicleArrivalTime += arrivalTime
            chromosomeArrivalTimes.append(totalVehicleArrivalTime)
        maximumChromosomeArrivalTime = max(chromosomeArrivalTimes)
        print ("Maximum Arrival Time :"+str(maximumChromosomeArrivalTime))