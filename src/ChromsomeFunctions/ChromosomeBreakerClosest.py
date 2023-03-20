import math
import random
import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings
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

def getChromosome () :
    givenChromosomes = []
    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\DataSet1-{pop_chromosomes}.1-Chromosome-data.txt', 'r') as file:
            contents = file.read()
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        contents = None

    lines = contents.split('\n')

    random_index = random.sample(range(0,pop_chromosomes+1),num_chromosome_start)

    #Get Random Chromosome from File
    for chromosome in range(num_chromosome_start):
        #Formatting the Line
        selected_line = lines[random_index[chromosome]].lstrip('[{').rstrip(']}')
        current_chromosome = list(map(int, selected_line.split(',')))
        givenChromosomes.append(current_chromosome)
    return givenChromosomes

def convertChromosomeXY(givenChromosomes):
    chromosomesXY = []
    requests = []
    pairNum = -1
    pairIndex = []
    try:
        with open(f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}RequestLocation\\{num_requests}\\{mode}{num_requests}.1-Request-data.txt', 'r') as file:
            contents = file.read()
            requests = eval(contents)
    except (FileNotFoundError) as e:
        print(f"Error: {e}")
        requests = None

    for chromosome in givenChromosomes:
        pairNum = -1
        chromosomeXY = []
        for index in chromosome:
            isPickup = False
            if(index % 2 == 0):
                pairNum += 1
                pairIndex.append((index,pairNum))
                isPickup = True
                corresponding_value = index + 1
                corresponding_index = chromosome.index(corresponding_value)
                chromosomeXY.append(((int(requests[index][0]),int(requests[index][1]),isPickup,pairNum),(int(requests[corresponding_value][0]),int(requests[corresponding_value][1]),not isPickup,pairNum)))
        chromosomesXY.append(chromosomeXY)
    #print(chromosomesXY)
    return chromosomesXY

def breakChromosome(chromosomesXY):
    for chromosome in chromosomesXY:
        print("Chromosome Lebgth",len(chromosome))
        chromosomePair = []
        distancePair = []
        usedPair = []
        finalPairList = []
        for i in range(len(chromosome)):
            for j in range(i+1,len(chromosome)):
                chromosomePair.append((chromosome[i], chromosome[j]))
        print(len(chromosomePair))
        for pair in chromosomePair:
            pickUp1x = pair[0][0][0]
            pickUp1y = pair[0][0][1]
            pickUp2x = pair[1][0][0]
            pickUp2y = pair[1][0][1]

            dropOff1x = pair[0][1][0]
            dropOff1y = pair[0][1][1]
            dropOff2x = pair[1][1][0]
            dropOff2y = pair[1][1][1]

            pickUpDistance = math.sqrt((pickUp1x - pickUp2x)**2 + (pickUp1y - pickUp2y)**2)
            dropOffDistance = math.sqrt((dropOff1x - dropOff2x)**2 + (dropOff1y - dropOff2y)**2)
            sumDistance = pickUpDistance + dropOffDistance
            distancePair.append((sumDistance, pair))

        distancePair.sort(key=lambda x: x[0])
        print(distancePair)

        for requestPair in range(int(len(chromosomePair))):
            print(requestPair)
            if distancePair[0][1][0][0][3] in usedPair or distancePair[0][1][1][0][3] in usedPair:
                print("used")
                distancePair.pop(0)
            else:
                finalPairList.append(distancePair[0])
                usedPair.append(distancePair[0][1][0][0][3])
                usedPair.append(distancePair[0][1][1][0][3])
                distancePair.pop(0)

        print(finalPairList)
        print(len(finalPairList))

def main():
    givenChromosomes = getChromosome(1)
    chromosomesXY = convertChromosomeXY(givenChromosomes)
    breakChromosome(chromosomesXY)

if __name__ == "__main__":
    main()