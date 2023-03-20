import numpy as np
import random
import sys
sys.path.append("V:/Critical-Services-Routing/src/Settings")
import Settings
sys.path.append("V:\Critical-Services-Routing\src\ChromsomeFunctions")
import ChromosomeBreakerRandom
sys.path.append("V:/Critical-Services-Routing/src/FitnessFunctions")
import Fitness

numRun = Settings.numRun



def main():
    brokenChromosomes = []
    original_chromosomes = []
    brokenChromosomes,original_chromosomes = ChromosomeBreakerRandom.getChromosome()
    for i in range (1):
        pop_fitness = 0
        current_index = 0
        corresponding_index = 0
        percentGoOn = 0.2
        chromosome_probabilities = []
        calculatedChromosomes = Fitness.calculateTotalWaitTime(brokenChromosomes,original_chromosomes)
        bestPercentChromosome = []
        bestIndex = int(len(calculatedChromosomes) * percentGoOn)
        bestPercentChromosome = calculatedChromosomes[:bestIndex]
        copyBestPercentChromosome = calculatedChromosomes[:bestIndex]
        nextPopulation = calculatedChromosomes[:bestIndex]
        swapIndexSorted = []

        for j in range(len(bestPercentChromosome)):
            pop_fitness += 1/bestPercentChromosome[j][0]

        for j in range(len(bestPercentChromosome)):
            chromosome_probabilities.append((1/bestPercentChromosome[j][0])/pop_fitness)

        for j in range (len(calculatedChromosomes) - len(bestPercentChromosome)):
            swapIndex = []
            otherIndex = []
            randomPair = np.random.choice(len(bestPercentChromosome),2, p =chromosome_probabilities)
            #print(bestPercentChromosome[randomPair[0]][1])
            for k in range(len(bestPercentChromosome[randomPair[0]][1])):
                #print(randomPair)
                current_index = copyBestPercentChromosome[randomPair[0]][1][k]
                if current_index % 2 == 0:
                    if random.uniform(0,1) < 0.5:
                       #print(copyBestPercentChromosome[randomPair[0]][1])
                       #print(current_index)
                       #print(k)
                       corresponding_index = bestPercentChromosome[randomPair[0]][1].index(current_index+1)
                       swapIndex.append(current_index)
                       swapIndex.append(current_index+1)
                       copyBestPercentChromosome[randomPair[0]][1][corresponding_index] = -1
                       copyBestPercentChromosome[randomPair[0]][1][k] = -1

            #swapIndexSorted = [swapIndex[a] for a in sorted(range(len(bestPercentChromosome[randomPair[1]][1])), key=lambda k: bestPercentChromosome[randomPair[1]][1][k])]
            for k in range(len(bestPercentChromosome[randomPair[1]][1])):
                #print(k)
                current_index = copyBestPercentChromosome[randomPair[1]][1][k]
                print(copyBestPercentChromosome[randomPair[1]][1])
                if current_index in swapIndex:
                    otherIndex.append(current_index)

            print(otherIndex)
            swapIndexSorted = otherIndex
            print(swapIndex)

            count = 0
            for k in range(len(bestPercentChromosome[randomPair[0]][1])):
                current_index = copyBestPercentChromosome[randomPair[0]][1][k]
                if current_index == -1 :
                    #print(count)
                    count += 1
                    #print(len(otherIndex))
                    current_index = swapIndexSorted[0]
                    swapIndexSorted.pop(0)

            #print(bestPercentChromosome[randomPair[0]][1])
            #print(bestPercentChromosome[randomPair[1]][1])
            #print(copyBestPercentChromosome[randomPair[0]][1])
            nextPopulation.append(copyBestPercentChromosome[randomPair[0]][1])
            copyBestPercentChromosome[randomPair[0]] = bestPercentChromosome[randomPair[0]]


main()