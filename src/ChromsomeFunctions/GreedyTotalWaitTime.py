import pandas as pd
import multiprocessing
import math
import random
import ChromosomeTools
import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings

mode = Settings.mode
num_requests = Settings.num_requests
num_vehicles = Settings.num_vehicles
pop_chromosomes = Settings.pop_chromosomes
num_chromosomes = Settings.num_chromosomes

run = 1
vehicleCapacity = 1
numStartChromosomes = 10
chromosomeFile = f'V:\\Critical-Services-Routing\\src\\Data\\Chromosome-Data\\DataSet-1\\{num_requests}\\DataSet1-{pop_chromosomes}.{run}-Chromosome-data.txt'
vehicleFile =f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}\\{num_requests}\\{mode}{num_requests}.1-Generic-data.txt'
requestFile = f'V:\\Critical-Services-Routing\\src\\Data\\{mode}-Data\\{mode}RequestLocation\\{num_requests}\\{mode}{num_requests}.1-Request-data.txt'

def main():
    randomChromosomesDataFrame = pd.DataFrame(ChromosomeTools.getRandomChromosomes(chromosomeFile,num_chromosomes,numStartChromosomes))
    request = ChromosomeTools.getRequest(randomChromosomesDataFrame.loc[[0]])
    allPairs = ChromosomeTools.getAllPairs(request)
    allPairRoutes = ChromosomeTools.getAllPairRoutes(allPairs)
    allVehicleRoutes = ChromosomeTools.getAllVehicleRoutes(allPairRoutes,num_vehicles,num_requests,vehicleCapacity,vehicleFile,requestFile,randomChromosomesDataFrame.loc[[0]])

if __name__ == '__main__':
    processes = []
    p1 = multiprocessing.Process(target=main)
    processes.append(p1)
    #p2 = multiprocessing.Process(target=requestFileMake, args=(run,))
    #processes.append(p2)
    #p3 = multiprocessing.Process(target=chromosomeFileMake, args=(run,))
    #processes.append(p3)
    for p in processes:
        p.start()
    for p in processes:
        p.join()